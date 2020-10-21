from django import forms
from django.forms import ModelForm, DateInput
from .models import Product,Contact
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .fields import ListTextWidget
class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ['user',  'views','subdistrict','subcategory', 'timeStamp','parent']
class ProductUpForm(ModelForm):
    class Meta:
        model = Product
        fields=('subdistrict','subcategory')
    def __init__(self, *args, **kwargs):
        _company_list = kwargs.pop('data_list', None)
        _subcategory_list = kwargs.pop('c_list', None)
        super(ProductUpForm, self).__init__(*args, **kwargs)
        self.fields['subdistrict'].widget = ListTextWidget(data_list=_company_list, name='subdistrict-list')
        self.fields['subcategory'].widget = ListTextWidget(data_list=_subcategory_list, name='subcategory-list')
class VariantForm(ModelForm):
    class Meta:
        model=Product
        fields=('name','specifications','price','available_quantity','image')
class ContactForm(ModelForm):
    class Meta:
        model=Contact
        fields='__all__'