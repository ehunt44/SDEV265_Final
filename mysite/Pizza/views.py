from json import loads, dumps
from django.shortcuts import render
from django.http import HttpResponse
from django.core import exceptions


from .models import Item, Location, Topping, Order, ItemOrderJoin

# handles base url requests
def index(request):
    return render(request, 'index.html', {})

# menu url
def menu(request):
    # pass item information to menu template, so it can be constructed
    ItemList = Item.objects.all()
    context = {"ItemList": ItemList}
    return render(request, 'menu.html', context)

# locations url
def locations(request):
    # pass location information to the location template
    Locations = Location.objects.all()
    context = {"Locations": Locations}
    return render(request, 'Locations.html', context)

# cart url
def cart(request):
    return render(request, 'Cart.html', {})

# checkout url
def checkout(request):
    return render(request, 'Checkout.html', {})

# handle orders placed from the website frontend
def order(request):
    try:
        # parse JSON order data
        data = loads(request.body)
    except:
        print("FAILED TO PARSE ORDER JSON")
        return genErr()

    # general data validation
    dataSize = len(data)
    try:
        if type(data) != list:
            return genErr()
        # data should include at least 1 item and the customer info
        elif dataSize < 2:
            return genErr()
        elif dataSize >= 1001:
            return HttpResponse(dumps("Error: Order must contain less than 1000 items"))
    except:
        print("GENERAL DATA VALIDATION EXCEPTION")
        return genErr()

    # cart data validation
    cartData = data[0:dataSize-1]  # cart data should be everything but the last item in the order data list
    # make sure cart data is in the correct format
    try:
        # check each item in cart data
        for item in cartData:
            # item should be a dict
            if type(item) != dict:
                return genErr()
            # item pk is an int
            elif type(item['pk']) != int:
                return genErr()
            # item toppings is a list
            elif type(item['toppingPks']) != list:
                return genErr()

            # check each topping for the item
            toppings = item['toppingPks']
            # too many topping pks
            if len(toppings) >= 999:
                return genErr()
            # make sure all topping pks are ints
            for toppingPk in toppings:
                if type(toppingPk) != int:
                    return genErr()
    except:
        print("CART VALIDATION EXCEPTION")
        return genErr()

    # customer data validation
    customerData = data[dataSize-1]  # should be the last item in the order data list
    # make sure customer data is in the correct format
    try:
        # address is a str
        if type(customerData['address']) != str:
            return genErr()
        # name is a str
        elif type(customerData['name']) != str:
            return genErr()
        # make sure name and address do not exceed the Order table field lengths
        elif len(customerData['address']) > Order._meta.get_field('customerAddress').max_length:
            print("ORDER ERROR: Customer address is too long")
            return HttpResponse(dumps("Error: The address is too long."))
        elif len(customerData['name']) > Order._meta.get_field('customerName').max_length:
            print("ORDER ERROR: Customer name is too long")
            return HttpResponse(dumps("Error: Your name is too long."))
    except:
        print("CUSTOMER DATA VALIDATION ERROR")
        return genErr()


    # now that the cart data is known to be in a valid format
    # condense duplicate cart items to a single item and a quantity
    betterData = []
    alreadyCounted = []
    for item in cartData:
        # don't count duplicates again
        if item in alreadyCounted:
            continue

        # get quantity of the item in the cart
        quantity = cartData.count(item)
        alreadyCounted.append(item)  # used to prevent duplicate items from getting counted again
        # create new item dict using previous item, but without reference
        newItem = dict(item)
        newItem['quantity'] = quantity  # add quantity info to new item dict
        betterData.append(newItem)  # append new item to better data

    # replace cart data with the condensed data
    cartData = betterData

    # verify all items and toppings exist in the database
    for item in cartData:
        try:
            # try to get item from DB using the order item's primary key
            Item.objects.get(pk=item['pk'])
        except exceptions.ObjectDoesNotExist:  # if item is not found
            print(f"ORDER ERROR: Unknown item id in order: {item['pk']}")
            return HttpResponse(dumps("Error: Unknown item in cart."))
        # check each topping for the item as well
        for toppingPk in item['toppingPks']:
            try:
                # try to get the topping using the PK
                Topping.objects.get(pk=toppingPk)
            except exceptions.ObjectDoesNotExist:  # if topping does not exist
                print(f"ORDER ERROR: Unknown topping id in order: {toppingPk}")
                return HttpResponse(dumps("Error: Unknown topping in cart."))

    # make sure toppings are valid for each item
    # (even if a topping is a valid topping, it may not be valid for a specific item)
    for item in cartData:
        for toppingPk in item['toppingPks']:
            try:
                # check if topping exists as an allowed topping for an item
                Item.objects.get(pk=item['pk']).toppings.get(pk=toppingPk)
            except exceptions.ObjectDoesNotExist:  # topping for item not found
                print(f"ORDER ERROR: {Item.objects.get(pk=item['pk']).name} cannot have the topping {Topping.objects.get(pk=toppingPk)}")
                return HttpResponse(dumps(f"Error: {Item.objects.get(pk=item['pk']).name} cannot have {Topping.objects.get(pk=toppingPk)} as a topping"))


    # finally, create the order
    try:
        # create order object
        o = Order(
            totalCost=calculateTotal(cartData),
            customerName=customerData['name'],
            customerAddress=customerData['address'],
            #dateTime= set to current time on order save
            location=Location.objects.get(pk=1)
            #items= many-to-many Item and Order
        )
        o.save()  # save order object

        # add items, quantities, and toppings to order using a join table
        for item in cartData:
            ioj = ItemOrderJoin(
                item=Item.objects.get(pk=item['pk']),
                order=o,  # order that the items and toppings will be related to
                itemQuantity=item['quantity']
                #toppings= many-to-many Topping and ItemOrderJoin
            )
            ioj.save()

            # add selected topping(s) to the item order join (using a join table between ItemOrderJoin and Topping)
            for toppingPk in item['toppingPks']:
                ioj.toppings.add(Topping.objects.get(pk=toppingPk))
            ioj.save()

    except:
        # this shouldn't happen
        print(f"ORDER ERROR: failed to create order somehow")
        return HttpResponse(dumps("Error: You broke it somehow, Congratulations!"))

    # respond with True, signaling the order was successful
    return HttpResponse(dumps(True))


# returns the total cost of the order
def calculateTotal(orderData):
    total = 0
    for item in orderData:
        temp = 0
        temp += Item.objects.get(pk=item['pk']).price
        for toppingPk in item['toppingPks']:
            temp += Topping.objects.get(pk=toppingPk).price
        temp *= item['quantity']  # cost of unique item and toppings combo, times the amount of it.
        total += temp

    return round(total, 2)

# generic error
def genErr():
    return HttpResponse(dumps("Something went wrong, try again later."))