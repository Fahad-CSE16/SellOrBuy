# Generated by Django 3.1.2 on 2020-10-12 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Session', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='blood_group',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='marital_status',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='religion',
        ),
    ]
