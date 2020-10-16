from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, AbstractUser
from PIL import Image
from multiselectfield import MultiSelectField
from django.utils.timezone import now

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Subcategory(models.Model):
    name=models.CharField( max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class District(models.Model):
    name=models.CharField( max_length=59)
    def __str__(self):
        return self.name
class Subdistrict(models.Model):
    name=models.CharField( max_length=59)
    district=models.ForeignKey(District,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    category= models.ForeignKey(Category, related_name="category_set", on_delete=models.CASCADE)
    subcategory=models.CharField(max_length=100)
    specifications=models.TextField()
    phone=models.CharField(max_length=17)
    district=models.ForeignKey(District,on_delete=models.CASCADE, related_name="district_set")
    subdistrict=models.CharField(max_length=100)
    price=models.FloatField()
    available_quantity= models.IntegerField()
    image = models.ImageField(default='default.jpg',upload_to='product/images')
    views = models.ManyToManyField(User, related_name='post_view')
    timeStamp = models.DateTimeField(default=now)
    def total_views(self):
        return self.views.count()
    def __str__(self):
        return self.user.username+ ": "+ self.name

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    paid=models.BooleanField(default=False)
    paid_amount=models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.address
class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product=models.ForeignKey(Product, related_name='items_set', on_delete=models.DO_NOTHING)
    price=models.FloatField()
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return str(self.price)
