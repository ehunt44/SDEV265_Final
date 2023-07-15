from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('locations/', views.locations, name='locations'),
    path('cart/', views.cart, name='cart'),
    path('checkout/order/', views.order, name="order"),
    path('checkout/', views.checkout, name='checkout'),
]
