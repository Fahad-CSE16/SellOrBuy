# Generated by Django 3.1.2 on 2020-10-17 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_auto_20201016_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Ordered', 'Ordered'), ('Shipped', 'Shipped'), ('Arrived', 'Arrived')], default='Ordered', max_length=100),
        ),
    ]