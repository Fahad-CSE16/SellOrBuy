from django.urls import path, include
from .views import *
from .api import api_add_to_cart, remove_from_cart,api_checkout,create_checkout_session
from Session.views import homeView
app_name = 'product'
urlpatterns = [
    path('createprod/', CreateProdView.as_view(), name='create'),
    path('vue/', index, name='index'),
    path('show/', productshow, name='show'),
    path('addsub/<int:pk>/', addsubdistrict, name='addsub'),
    path('prod/<int:id>/', prod_detail, name='detail'),


    path('api_add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api_checkout/', api_checkout, name='api_checkout'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('create_checkout/', create_checkout_session, name='create_checkout'),
    
    
    path('cart/', cart_detail, name='cart'),
    path('success/', success, name='success'),
    path('', homeView.as_view(), name='home'),

]
