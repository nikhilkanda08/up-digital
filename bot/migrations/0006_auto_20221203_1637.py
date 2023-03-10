# Generated by Django 3.2.15 on 2022-12-03 16:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20221127_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresult',
            name='titles',
            field=models.TextField(blank=True, null=True, verbose_name='Search Results Titles'),
        ),
        migrations.AddField(
            model_name='user',
            name='OTP',
            field=models.IntegerField(blank=True, null=True, verbose_name='Reset Password OTP'),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='Schedule',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 3, 16, 37, 22, 498548), verbose_name='Search Result schedule'),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='active_device',
            field=models.IntegerField(blank=True, choices=[(0, 'Tablet'), (1, 'Laptop'), (2, 'Mobile Phones')], null=True, verbose_name='Active Device'),
        ),
    ]