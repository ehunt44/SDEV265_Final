from django.contrib import admin
from .models import Item, Topping, Location, Order, ItemOrderJoin


class ItemOrderJoinInline(admin.StackedInline):
    model = ItemOrderJoin
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Order", {"fields": ["totalCost", "customerName", "customerAddress", "dateTime", "location"]}),
    ]
    inlines = [ItemOrderJoinInline]


# Register your models here.
admin.site.register(Item)
admin.site.register(Topping)
admin.site.register(Location)
admin.site.register(Order, OrderAdmin)
admin.site.register(ItemOrderJoin)
