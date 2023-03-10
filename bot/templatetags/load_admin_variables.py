import calendar
from bot.models import *
from decimal import Decimal
from django import template
from random import randrange
# from django.template.defaulttags import register

register = template.Library()

def remainingSearches(id,searches):
    total_per_day_search_allowed = round(Decimal((str(searches))), 2)
    
    total_per_day_search_data = Keywords.objects.filter(campaign__in = Campaign.objects.filter(user = User.objects.get(id=id))).aggregate(total=Sum('searches_per_day'))
    try:
        if total_per_day_search_data:
            total_per_day_search = round(Decimal((str(total_per_day_search_data['total']))), 2)
        else:
            total_per_day_search = 0.00
    except:
        total_per_day_search = 0.00

    num = round(Decimal((str(float(total_per_day_search_allowed) - float(total_per_day_search)))), 2)
    if num > 0:
        return num
    return 0

register.filter('remainingSearches', remainingSearches)