import json
from bot.models import *

def addCityStateCountry():
    # Python program to read

    # country json file
    # Opening JSON file
    f = open('bot/utils/data/json/countries.json')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    print(data)
    # Iterating through the json
    # list
    records = []
    for i in data['Data']:
        records.append(country(name=i['name'],value=i['value']))
        # print(i)
    print(records)
    country.objects.bulk_create(records)
    # Closing file
    f.close()

    # state json file
    # Opening JSON file
    states = open('bot/utils/data/json/states.json')
    
    # returns JSON object as 
    # a dictionary
    statesData = json.load(states)
    print(statesData)
    # Iterating through the json
    # list
    statesRecords = []
    for i in statesData['Data']:
        statesRecords.append(state(name=i['name'],value=i['value'],country=country.objects.get(id=i['country_id'])))
        # print(i)
    print(statesRecords)
    state.objects.bulk_create(statesRecords)
    # Closing file
    states.close()

    # country json file
    # Opening JSON file
    cities = open('bot/utils/data/json/cities.json')
    
    # returns JSON object as 
    # a dictionary
    cityData = json.load(cities)
    print(cityData)
    # Iterating through the json
    # list
    cityRecords = []
    for i in cityData['Data']:
        cityRecords.append(city(name=i['name'],value=i['value'],country=country.objects.get(id=i['country_id']),state=state.objects.get(id=i['state_id'])))
        # print(i)
    print(cityRecords)
    city.objects.bulk_create(cityRecords)
    # Closing file
    cities.close()
    