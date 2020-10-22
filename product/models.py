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
    parent=models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE,blank=True,null =True)
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
    def get_absolute_url(self):
        return '/prod/%s/' % (self.id)
    def get_rating(self):
        total=sum(int(review['stars']) for review in self.reviews.values())
        if self.reviews.count() > 0:
            return total/self.reviews.count()
        else:
            return 0
class Order(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Arrived', 'Arrived'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    phone=models.CharField(max_length=17, default='1')
    created_at=models.DateTimeField(auto_now_add=True)
    paid=models.BooleanField(default=False)
    paid_amount=models.FloatField(blank=True, null=True)
    shipped_date=models.DateTimeField(blank=True, null=True)
    status=models.CharField(choices=STATUS, max_length=100, default='Ordered')
    def __str__(self):
        return self.address
    def get_total_quantity(self):
        return sum(int(item.quantity) for item in self.items.all())
class OrderItem(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Arrived', 'Arrived'),
    )
    order=models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    owner=models.ForeignKey(User, related_name="ownerset", on_delete=models.DO_NOTHING,default=1)
    product=models.ForeignKey(Product, related_name='items_set', on_delete=models.CASCADE)
    price=models.FloatField()
    quantity=models.IntegerField(default=1)
    shipped_date=models.DateTimeField(blank=True, null=True)
    date_of_order=models.DateTimeField(default=now)
    status=models.CharField(choices=STATUS, max_length=100, default='Ordered')
    def __str__(self):
        return str(self.price)
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=17)
    address=models.CharField(max_length=100)
    details=models.TextField()
    def __str__(self):
        return self.name
class ProductReview(models.Model):
    product=models.ForeignKey(Product,related_name='reviews',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='reviews_user',on_delete=models.CASCADE)
    content=models.TextField()
    stars=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def get_rating(self):
        total=sum(int(review['stars']) for review in self.reviws.value())
        return total/self.reviews.conunt()