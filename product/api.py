from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .cart import Cart

from .models import Product
import json
from django.contrib import messages
from .utils import checkout
from .models import Order,OrderItem
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

# TOKEN  generator import
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def api_checkout(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True} 
    address = data['address']
    zipcode = data['zipcode']
    place = data['place']
    phone = data['phone']
    cart=Cart(request)
    user=request.user
    orderid=checkout(request, request.user,address,zipcode,place,phone)
    current_site = get_current_site(request)
    mail_subject = 'Confirm Your Order!'
    message = render_to_string('product/order_confirm_please.html', {
        'user': user,
        'domain': current_site.domain,
        'cart':cart,
        'orderid':orderid
        })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    order=Order.objects.get(pk=orderid)
    order.paid_amount=cart.get_total_cost()
    order.save()
    cart.clear()
    messages.success(request, 'Successfully Placed Your Order!, Please confirm from your profiles mail address!')
    return JsonResponse(jsonresponse)
from notifications.signals import notify

def confirm_order(request,orderid):
    order=Order.objects.get(pk=orderid)
    order.paid=True
    order.save()
    for i in order.items.all():
        user = request.user
        receiver=i.owner
        notify.send(user, recipient=receiver, level='success',  verb="has ordered for "+str(i.product.name)+" quantity " + str(
            i.quantity)+" in " + str(i.order.address) + f''' <a class =" btn btn-primary btn-sm " href="/ordered/">SEE</a> ''')
    messages.success(request, 'Successfully Confirmed Your Order!')
    return redirect('/')

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

import stripe
from django.conf import settings
def create_checkout_session(request):
    cart=Cart(request)

    stripe.api_key=settings.STRIPE_API_KEY_HIDDEN
    items=[]

    for item in cart:
        product=item['product']
        obj={
            'price_data':{
                'currency':'usd',
                'product_data':{
                    'name':product.name
                },
                'unit_amount':int(product.price*100)
            },
            'quantity':item['quantity']
        }
        items.append(obj)
    session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cart/'
    )
    return JsonResponse({'session' : session})