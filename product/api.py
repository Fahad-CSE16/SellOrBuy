from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .cart import Cart

from .models import Product
import json
from django.contrib import messages
from .utils import checkout
from .models import Order,OrderItem
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

def api_checkout(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True} 
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']
    orderid=checkout(request, request.user,address,zipcode,place)
    cart=Cart(request)
    paid=True
    if paid:
        order=Order.objects.get(pk=orderid)
        order.paid=True
        order.paid_amount=cart.get_total_cost()
        order.save()
        cart.clear()
    return JsonResponse(jsonresponse)

def api_add_to_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_id)
    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)
    return JsonResponse(jsonresponse)


def remove_from_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = str(data['product_id'])
    cart = Cart(request)
    cart.remove(product_id)
    return JsonResponse(jsonresponse)


def increment_qty(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = str(data['product_id'])
    cart = Cart(request)
