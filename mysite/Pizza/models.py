from django.db import models
from django.utils import timezone
from os import path


# Create your models here.

# Topping table
class Topping(models.Model):
    name = models.CharField(max_length=64, default="Default Topping")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    calories = models.IntegerField(default=0)
    def __str__(self):
        return self.name

# Item table
class Item(models.Model):
    name = models.CharField(max_length=128, default="Default Item")
    description = models.CharField(max_length=256, default="Default Description")
    image = models.FilePathField(path="Pizza/static/Pizza/Menu/", default="default.png")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    calories = models.IntegerField(default=0)
    toppings = models.ManyToManyField(Topping, db_table="ItemToppingJoin", blank=True)
    def __str__(self):
        return self.name

    # return filename of the item's image EX "pepperoni.png"
    def filename(self):
        return path.basename(self.image)

# Location table
class Location(models.Model):
    name = models.CharField(max_length=128, default="Default Location")
    address = models.CharField(max_length=128, default="Default Address")
    city = models.CharField(max_length=64, default="Default City")
    stateAbriv = models.CharField(max_length=2, default="AA")
    zip = models.CharField(max_length=5, default="12345")
    def __str__(self):
        return self.name

# Order table
class Order(models.Model):
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    customerName = models.CharField(max_length=128, default="Default Customer Name")
    customerAddress = models.CharField(max_length=128, default="Default Customer Address")
    dateTime = models.DateTimeField(default=timezone.now, blank=True)
    location = models.ForeignKey(Location, on_delete=models.RESTRICT)
    items = models.ManyToManyField(Item, through="ItemOrderJoin")
    def __str__(self):
        return str(self.pk)

# Join table between Item and Order
class ItemOrderJoin(models.Model):
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    itemQuantity = models.IntegerField(default=1)
    toppings = models.ManyToManyField(Topping, db_table="ItemToppingOrderJoin", blank=True)

    # to str method shows the order ID, item name and quantity, and each topping name.
    def __str__(self):
        toppingsStr = ""
        for top in self.toppings.all():
            toppingsStr += f"{top.name}, "
        toppingsStr = toppingsStr[0:len(toppingsStr)-2]
        return f"Order {str(self.order.pk)}: {self.itemQuantity} {self.item.name} {f'w/ {toppingsStr}' if len(toppingsStr) != 0 else ''}"