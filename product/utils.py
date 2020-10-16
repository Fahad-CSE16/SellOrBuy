import datetime
import os
from random import randint
from .cart import Cart
from .models import Order,OrderItem

def checkout(request, user,address,zipcode,place):
    order=Order(user=user,address=address,zipcode=zipcode,place=place)
    order.save()
    cart= Cart(request)
    for item in cart:
        OrderItem.objects.create(order=order,product=item['product'],price=item['price'], quantity=item['quantity'])
    return order.id