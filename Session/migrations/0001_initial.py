# Generated by Django 3.1.2 on 2020-10-11 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField(blank=True)),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('gender', models.CharField(choices=[('Male', 'MALE'), ('Female', 'FEMALE')], max_length=50)),
                ('address', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
                ('marital_status', models.CharField(choices=[('Married', 'Married'), ('Unmarried', 'Unmarried'), ('Divorced', 'Divorced'), ('Engaged', 'Engaged'), ('Separated', 'Separated')], max_length=50)),
                ('religion', models.CharField(max_length=50)),
                ('category', multiselectfield.db.fields.MultiSelectField(choices=[('Buyer', 'Buyer'), ('Seller', 'Seller')], max_length=100)),
                ('image', models.ImageField(default='default.jpg', upload_to='Session/images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
