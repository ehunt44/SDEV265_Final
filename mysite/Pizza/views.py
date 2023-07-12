from json import loads
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from .models import Item, Location, Topping

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def menu(request):
    ItemList = Item.objects.all()
    context = {"ItemList": ItemList}
    return render(request, 'menu.html', context)

def locations(request):
    Locations = Location.objects.all()
    context = {"Locations": Locations}
    return render(request, 'Locations.html', context)

def cart(request):
    return render(request, 'Cart.html', {})

def checkout(request):
    return render(request, 'Checkout.html', {})

def order(request):
    data = loads(request.body)
    cartData = data[0:len(data)-1]
    customerData = data[len(data)-1]
    #testing
    print(customerData["name"], customerData["address"])
    for item in cartData:
        print(item["name"])

    return HttpResponseRedirect(reverse('cart'))











def getAge():
    return 5

def add(request):
    age = getAge()
    name = "Bob"


    return render(request, 'add.html', {'name': name, 'age': age})