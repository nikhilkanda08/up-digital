# Generated by Django 3.2.15 on 2023-01-04 20:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0009_auto_20221211_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='business_name',
            field=models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Business Name'),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='Schedule',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 4, 20, 25, 41, 632625), verbose_name='Search Result schedule'),
        ),
    ]
