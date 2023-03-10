# Generated by Django 3.2.15 on 2022-11-20 11:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_auto_20221117_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresult',
            name='found_index',
            field=models.BooleanField(default=False, verbose_name='Website Found Index'),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='Schedule',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 20, 11, 24, 56, 40403), verbose_name='Search Result schedule'),
        ),
    ]