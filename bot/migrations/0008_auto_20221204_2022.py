# Generated by Django 3.2.15 on 2022-12-04 20:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_auto_20221204_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchresult',
            name='Schedule',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 4, 20, 22, 45, 668555), verbose_name='Search Result schedule'),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='direction_URL',
            field=models.TextField(blank=True, null=True, verbose_name='Direction URL'),
        ),
    ]
