from django.db import models

# Create your models here.
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, AbstractUser
from PIL import Image
from multiselectfield import MultiSelectField


class UserProfile(models.Model):
    GENRE_CHOICES = (
        ('Male', 'MALE'),
        ('Female', 'FEMALE'),
    )
    MARITAL_STATUS_CHOICES = (
        ('Married', 'Married'),
        ('Unmarried', 'Unmarried'),
        ('Divorced', 'Divorced'),
        ('Engaged', 'Engaged'),
        ('Separated', 'Separated'),
    )
    CATEGORY = (
        ('Buyer', 'Buyer'),
        ('Seller', 'Seller'),

    )
    BLOOD_GROUP = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),

    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='userprofile')
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=13)
    category = MultiSelectField(choices=CATEGORY,
                                max_choices=3, max_length=100)
    image = models.ImageField(default='default.jpg',
                              upload_to='Session/images')

    def __str__(self):
        return f'{self.user.username} Profile'
    AUTH_PROFILE_MODULE = 'app.UserProfile'

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
