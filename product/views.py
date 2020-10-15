from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import View
import time
from math import ceil
from .models import Product, Category, District, Subdistrict,Subcategory
from .forms import ProductForm,ProductUpForm
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
        return reverse_lazy('product:addsub',kwargs={'pk': id})
def addsubdistrict(request,pk):
    prod= Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductUpForm(request.POST, instance=prod)
        if form.is_valid():
            sub = form.cleaned_data['subdistrict']
            subcheck = Subdistrict.objects.filter(district=prod.district).filter(name=sub)
            if not subcheck:
                Subdistrict.objects.create(name=sub,district=prod.district)
            sub = form.cleaned_data['subcategory']
            subchecks = Subcategory.objects.filter(category=prod.category).filter(name=sub)
            if not subchecks:
                Subcategory.objects.create(name=sub,category=prod.category)
            form.save()
            messages.success(request, 'Post Created Successfully. ')
            return redirect('product:home')
        
    else:
        subdistrict=Subdistrict.objects.filter(district=prod.district)
        subcategory=Subcategory.objects.filter(category=prod.category)
        form = ProductUpForm(instance=prod,data_list=subdistrict,c_list=subcategory)
    context={
        'form': form,
    }
    return render(request, 'product/productcreate.html',context)

class EditProdView(generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/productcreate.html'
    def get_success_url(self):
        id = self.kwargs['pk']
        return reverse_lazy('product:home', kwargs={'pk': id})
def productshow(request):
    category=Category.objects.all().order_by('name')
    district= District.objects.all().order_by('name')
    if request.method == "POST":
        dis = request.POST['district_i']
        cat = request.POST['category_i']
        if dis or cat:
            queryset = (Q(district__name__icontains=dis)) & (Q(category__name__icontains=cat))
            results = Product.objects.filter(queryset).order_by('-timeStamp').distinct()
        else:
            results = []
        params={
            'results':results,
            'district':district,
            'category':category,
            'dis':dis,
            'cat':cat
        }

    else:
        prod= Product.objects.all()
        n=len(prod)
        nSlides = ceil(n/4)
        allProds = []
        catprods= Product.objects.values('category', 'id').order_by('-timeStamp')
        print(catprods)
        cats = { item ['category'] for item in catprods}
        for cat in cats:
            prod= Product.objects.filter(category = cat).order_by('-timeStamp')
            n = len(prod)
            nSlides = ceil(n / 4)
            allProds.append([prod, range(1, nSlides), nSlides])
        params = {
            'allProds': allProds,
            'category':category,
            'district':district,
            }
    return render(request, 'product/index.html',params)
import json
def index(request):
    product=Product.objects.all()
    product_list = list(product.values('user__username','name','district__name'))
    context = {}
    context["product"] = json.dumps(product_list)
    return render(request,'index.html',context)
def prod_detail(request, id):
    prod=Product.objects.get(id=id)
    
    return render(request,'product/detail.html',{'prod':prod})
from .cart import Cart

def cart_detail(request):
    cart= Cart(request)
    context={
        'cart':cart,
    }
    return render(request, 'product/cart.html',context)