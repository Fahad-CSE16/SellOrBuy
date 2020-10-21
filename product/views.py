from .cart import Cart
import json
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import View
import time
from math import ceil
from .models import Product, Category, District, Subdistrict, Subcategory,Order,OrderItem,ProductReview
from .forms import ProductForm, ProductUpForm, VariantForm,ContactForm
from notifications.signals import notify
from django.views import generic, View
from django.urls import reverse_lazy
from django.db.models import Q


class CreateProdView(generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/productcreate.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Successfully Created Your Product.')
        messages.success(self.request, ' Now Add Subdistrict and Subcategory!')
        return super().form_valid(form)

    def get_success_url(self):
        id = self.object.id
        # user = self.request.user
        # us = User.objects.all()
        # for i in us:
        #     try:
        #         j = i.tuitionclass
        #     except:
        #         j = None
        #     if j:
        #         if receiverchoose(j, self.object):
        #             receiver = i
        #             if receiver != user:
        #                 notify.send(user, recipient=receiver, level='success',  verb="is searching for a teacher for "+str(self.object.medium)+" for " + str(
        #                     self.object.class_in.all().first())+" for subject " + str(self.object.subject.all().first()) + f''' <a class =" btn btn-primary btn-sm " href="/posts/post/{self.object.sno}">go</a> ''')
        #  kwargs={'pk': id}
        return reverse_lazy('product:addsub', kwargs={'pk': id})


def addsubdistrict(request, pk):
    prod = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductUpForm(request.POST, instance=prod)
        if form.is_valid():
            sub = form.cleaned_data['subdistrict']
            subcheck = Subdistrict.objects.filter(
                district=prod.district).filter(name=sub)
            if not subcheck:
                Subdistrict.objects.create(name=sub, district=prod.district)
            sub = form.cleaned_data['subcategory']
            subchecks = Subcategory.objects.filter(
                category=prod.category).filter(name=sub)
            if not subchecks:
                Subcategory.objects.create(name=sub, category=prod.category)
            form.save()
            messages.success(request, 'Product Created Successfully. ')
            messages.success(request, 'Add More Varint! ')
            return redirect(f'/variant/{prod.id}/')

    else:
        subdistrict = Subdistrict.objects.filter(district=prod.district)
        subcategory = Subcategory.objects.filter(category=prod.category)
        form = ProductUpForm(
            instance=prod, data_list=subdistrict, c_list=subcategory)
    context = {
        'form': form,
    }
    return render(request, 'product/productcreate.html', context)


class EditProdView(generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/productcreate.html'

    def get_success_url(self):
        id = self.kwargs['pk']
        return reverse_lazy('product:addsub', kwargs={'pk': id})

def delete(request,pk):
    prod=Product.objects.filter(id=pk)
    prod.delete()
    return redirect('product:show')
def variantadd(request,id):
    if request.method=="POST":
        form=VariantForm(request.POST,request.FILES)
        parent=Product.objects.get(id=id)
        if form.is_valid():
            image=form.cleaned_data['image']
            print(image)
            obj=form.save(commit=False)
            obj.user=request.user
            obj.parent=parent
            obj.category=parent.category
            obj.subcategory=parent.subcategory
            obj.district=parent.district
            obj.subdistrict=parent.subdistrict
            obj.phone=parent.phone
            obj.save()
            messages.success(request, "Successfully added a varinat!")

    else:
        form=VariantForm()
    return render(request,'product/productcreate.html',{'form':form,'pass':True})


def search(request):
    if request.method == "POST":
        query = request.POST['q']
        print(query)
        if query:
            queryset = (Q(name__icontains=query)) | (
            Q(specifications__icontains=query)) | (Q(category__name__icontains=query)) | (Q(district__name__icontains=query)) | (Q(subcategory__icontains=query)) | (Q(subdistrict__icontains=query)) | (Q(parent__name__icontains=query))
            results = Product.objects.filter(queryset).order_by('-timeStamp').distinct()
        else:
            
            results = []
        # for re in results:
        #     print(re.name)
        context= {'query':query,'results':results}
    else:
        context= {}
    return render(request, 'product/search.html',context)

def productshow(request):
    cart = Cart(request)
    category = Category.objects.all().order_by('name')
    district = District.objects.all().order_by('name')
    if request.method == "POST":
        dis = request.POST['district_i']
        cat = request.POST['category_i']
        if dis or cat:
            queryset = (Q(district__name__icontains=dis)) & (
                Q(category__name__icontains=cat))
            results = Product.objects.filter(
                queryset).order_by('-timeStamp').distinct()
        else:
            results = []
        params = {
            'results': results,
            'district': district,
            'category': category,
            'dis': dis,
            'cat': cat,
            'cart': cart
        }

    else:
        prod = Product.objects.all()
        n = len(prod)
        nSlides = ceil(n/4)
        allProds = []
        catprods = Product.objects.values(
            'category', 'id').order_by('-timeStamp')
        # print(catprods)
        cats = {item['category'] for item in catprods}
        for cat in cats:
            prod = Product.objects.filter(category=cat).filter(parent=None).order_by('-timeStamp')
            for p in prod:
                if cart.has_product(p.id):
                    p.in_cart=True
                else:
                    p.in_cart=False
            n = len(prod)
            nSlides = ceil(n / 4)
            allProds.append([prod, range(1, nSlides), nSlides])
        params = {
            'allProds': allProds,
            'category': category,
            'district': district,
            'cart': cart
        }
    return render(request, 'product/index.html', params)


def index(request):
    product = Product.objects.all()
    product_list = list(product.values(
        'user__username', 'name', 'district__name'))
    context = {}
    context["product"] = json.dumps(product_list)
    return render(request, 'About.html', context)

import random
def prod_detail(request, id):
    prod = Product.objects.get(id=id)

    if request.method=='POST':
        stars=request.POST['stars']
        content=request.POST['content']
        ProductReview.objects.create(user=request.user,product=prod,stars=stars,content=content)

    cart = Cart(request)

    related_products=list(prod.category.category_set.filter(parent=None).exclude(id=prod.id))
    if len(related_products) >= 3:
        related_products=random.sample(related_products,3)
    if cart.has_product(prod.id):
        prod.in_cart=True
    else:
        prod.in_cart=False

    return render(request, 'product/detail.html', {'prod': prod, 'cart': cart,'related_products':related_products})
from django.conf import settings

def cart_detail(request):
    cart = Cart(request)
    pub_key=settings.STRIPE_API_KEY_PUBLISHABLE
    productsstring = ''
    for item in cart:
        product = item['product']
        url='/prod/%s/' % product.id
        b = "{'id':'%s', 'title':'%s','price':'%s','image':'%s','quantity':'%s', 'total_price':'%s','url':'%s','available_quantity':'%s'}," % (
            product.id, product.name, product.price, product.image.url, item['quantity'], item['total_price'],url,product.available_quantity)
        productsstring = productsstring + b
    context = {
        'cart': cart,
        'pub_key':pub_key,
        'productsstring': productsstring
    }
    return render(request, 'product/cart.html', context)
def success(request):
    return render(request, 'product/success.html')
def your_products(request):
    prod=Product.objects.filter(user=request.user).order_by('timeStamp')
    context={
        'prod':prod,
    }
    return render(request,'product/your_products.html',context)
def product_orders(request):
    
    items=OrderItem.objects.filter(owner=request.user).order_by('-date_of_order')
    

    context={
        'items':items
    }
    return render(request,'product/product_orders.html',context)
import datetime
# TOKEN  generator import
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
def items_shipped(request,id):
    item=OrderItem.objects.get(id=id)
    item.status="Shipped"
    item.shipped_date=datetime.datetime.now()
    item.save()
    orderid=item.order.id
    user=request.user
    current_site = get_current_site(request)
    mail_subject = 'Your product Has Shipped'
    message = render_to_string('product/order_shipped.html', {
        'user': user,
        'domain': current_site.domain,
        'orderid':orderid,
        'item':item,
        })
    to_email = item.order.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    print(item.order.user.email)

    messages.success(request,'Status CHanged to shipped!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def items_arrived(request,id):
    item=OrderItem.objects.get(id=id)
    item.status="Arrived"
    item.shipped_date=datetime.datetime.now()
    item.save()
    messages.success(request,'Status CHanged to Arrived!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def contact(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Successfully Submitted')
        return redirect('/')
    else:
        form=ContactForm()
    context={
        'form':form
    }

    return render(request,'product/contact_us.html',context)