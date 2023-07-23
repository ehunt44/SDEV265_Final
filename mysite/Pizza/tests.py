from django.test import TestCase
from .models import Topping, Item, Location, Order, ItemOrderJoin


# tests to ensure that the various Django models/database tables work as expected
class PizzaTestCase(TestCase):

    def setUp(self):
        self.topping1 = Topping.objects.create(name="Topping1", price=1.50, calories=100)
        self.topping2 = Topping.objects.create(name="Topping2", price=2.00, calories=150)

        self.item1 = Item.objects.create(name="Item1", price=10.00, calories=500)
        self.item2 = Item.objects.create(name="Item2", price=15.00, calories=700)

        self.location1 = Location.objects.create(name="Location1", address="Address1", city="City1", stateAbriv="ST", zip="12345")
        self.location2 = Location.objects.create(name="Location2", address="Address2", city="City2", stateAbriv="ST", zip="54321")

        self.order1 = Order.objects.create(totalCost=25.00, customerName="John Doe", customerAddress="Address1", location=self.location1)
        self.order2 = Order.objects.create(totalCost=30.00, customerName="Jane Smith", customerAddress="Address2", location=self.location2)

        self.item_order_join1 = ItemOrderJoin.objects.create(item=self.item1, order=self.order1, itemQuantity=2)
        self.item_order_join1.toppings.add(self.topping1, self.topping2)

        self.item_order_join2 = ItemOrderJoin.objects.create(item=self.item2, order=self.order2, itemQuantity=1)
        self.item_order_join2.toppings.add(self.topping1)

    def test_topping(self):
        self.assertEqual(str(self.topping1), "Topping1")
        self.assertEqual(str(self.topping2), "Topping2")

    def test_item(self):
        self.assertEqual(str(self.item1), "Item1")
        self.assertEqual(str(self.item2), "Item2")

    def test_location(self):
        self.assertEqual(str(self.location1), "Location1")
        self.assertEqual(str(self.location2), "Location2")

    def test_order(self):
        self.assertEqual(str(self.order1), str(self.order1.pk))
        self.assertEqual(str(self.order2), str(self.order2.pk))

    def test_item_orderjoin(self):
        expected_str1 = "Order {}: 2 Item1 w/ Topping1, Topping2".format(self.order1.pk)
        expected_str2 = "Order {}: 1 Item2 w/ Topping1".format(self.order2.pk)

        self.assertEqual(str(self.item_order_join1), expected_str1)
        self.assertEqual(str(self.item_order_join2), expected_str2)