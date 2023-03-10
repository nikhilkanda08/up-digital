import calendar
from bot.models import *
from random import randrange
from django.template.defaulttags import register

colors = ['rgb(71, 209, 243)','rgb(10, 224, 162)','rgb(130, 124, 248)','rgb(254, 138, 128)','rgb(255, 164, 92)']

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def month_name(month_number):
    month_number = int(month_number)
    return calendar.month_name[month_number]

@register.filter
def per_day_search_status(searches, ID):
    try:
        total_per_day_search_allowed = searches
        
        total_per_day_search_data = Keywords.objects.filter(campaign__in = Campaign.objects.filter(user = User.objects.get(id=ID))).aggregate(total=Sum('searches_per_day'))
        if total_per_day_search_data['total']:
            total_per_day_search = total_per_day_search_data['total']
        else:
            total_per_day_search = 0
        if total_per_day_search < total_per_day_search_allowed:
            return True
        else:
            return False
    except:
        return False

@register.simple_tag
def RGB_code():
    return colors[randrange(4)]

@register.filter
def keyword_status(keywordID):
    try:
        obj = SearchResult.objects.filter(Keywords = Keywords.objects.get(id=keywordID), found_index = True)

        if len(obj) > 0 :
            return True
        return False
    except:
        return False

@register.filter
def strToList(str):
    try:
        return list(str.split(","))
    except:
        return []

@register.filter
def nameByIndex(indexable, i):
    return indexable[i].keyword

@register.filter
def byIndex(indexable, i):
    return indexable[i]

@register.filter
def subtract(a, b):
    return a - b

@register.filter
def strToListLength(str):
    try:
        if str:
            return list(str.split(","))
        return []
    except:
        return []