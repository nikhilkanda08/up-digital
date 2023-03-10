import json
from bot.models import *

def addSearchPlan():
    # Python program to read

    # country json file
    # Opening JSON file
    f = open('bot/utils/data/json/searchPlan.json')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    print(data)
    # Iterating through the json
    # list
    records = []
    for i in data['Data']:
        records.append(SearchPlan(planID=i['id'],cost=i['cost'],total_pages=i['pages'],onsite_time=i['time'],daily_searches=i['dailySearches'],searche_cost=i['perSearchCost'],stripe_price_ID=i['stripeID']))
        print(i['id'])
    print(records)
    SearchPlan.objects.bulk_create(records)
    # Closing file
    f.close()

    