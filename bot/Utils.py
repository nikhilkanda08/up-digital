import calendar
from bot.models import *


def is_what_percent_of(num_a, num_b):
    try:
        return (num_a / num_b) * 100
    except:
        return 0

def month_name(month_number):
    month_number = int(month_number)
    return calendar.month_name[month_number]

def per_day_search_status(searches, ID):
    status = False
    count = 0
    try:
        total_per_day_search_allowed = searches
        total_per_day_search_data = Keywords.objects.filter(campaign__in = Campaign.objects.filter(user = User.objects.get(id=ID))).aggregate(total=Sum('searches_per_day'))
        if total_per_day_search_data['total']:
            total_per_day_search = total_per_day_search_data['total']
        else:
            total_per_day_search = 0

        if total_per_day_search < total_per_day_search_allowed:
            status = True
            count = float(total_per_day_search_allowed) - float(total_per_day_search)
        else:
            status = False
    except:
        print("error in per_day_search_status")

    return {"status":status,"count":round(count, 2)}

def get_number_to_number_percentage(current, previous):
    if current > previous:
        status = 'UP'
        if previous > 0:
            score = ((current - previous) / previous)
        else:
            score = 0
    elif current < previous:
        status = 'DOWN'
        if current > 0:
            score = ((previous - current) / current)
        else:
            score = 0
    else:
        status = 'UP'
        score = 0

    return status, score

def ListSkipAids(list_web,website_link,bussiness_name=None):
    try:
        list_link = list_web
        substring= 'www.googleadservices.com'
        final_list = []
        postion = None
        for item in list_link:
            if substring not in item:
                final_list.append(item.split(':~')[0].replace(',',''))
        if bussiness_name:
            for index,item in enumerate(final_list,1):
                print(index, item,bussiness_name)
                if bussiness_name in item:
                    postion = index
        else:
            for index,item in enumerate(final_list,1):
                if website_link in item:
                    postion = index
        return final_list,postion
    except Execption as e :
        print(e)
        return [],None