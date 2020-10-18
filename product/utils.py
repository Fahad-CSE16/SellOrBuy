import datetime
import os
from random import randint
from .cart import Cart
from .models import Order,OrderItem,Product

def checkout(request, user,address,zipcode,place):
    order=Order(user=user,address=address,zipcode=zipcode,place=place)
    order.save()
    cart= Cart(request)
    for item in cart:
        id=item['id']
        i=Product.objects.get(id=id)
        i.available_quantity=i.available_quantity-item['quantity']
        i.save()
        OrderItem.objects.create(order=order,product=item['product'],price=item['price'], quantity=item['quantity'])
    return order.id