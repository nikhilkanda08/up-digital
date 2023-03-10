import math
from bot.models import *
from bot.utils import keyword_search
from bot.utils.keyword_search_mobile import keyword_search_mobile
from bot.utils.keyword_search_web import keyword_search_web
from bot.utils.map_search_direction_mobile import map_search_direction_mobile
from bot.utils.map_search_direction_web import map_search_direction_web
from bot.utils.map_search_mobile import map_search_mobile
from bot.utils.map_search_web import map_search_web
from bot.Utils import ListSkipAids

def create_keyword_search_schedule():
    all_keywords = Keywords.objects.all()
    for keyword in all_keywords:
        today = datetime.today()
        print(keyword.searches_per_day)
        searchNumber = math.modf(float(keyword.searches_per_day))
        print(round(searchNumber[0], 2))
        print(searchNumber[1])
        searchNumberInteger = searchNumber[1]
        searchNumberDecimal = round(searchNumber[0], 2)
        perDaysSearches = searchNumberInteger
        days = 1
        if keyword.campaign.search_type == 'organic_search':
            # add search results records for integer value
            if searchNumberInteger > 0:
                IntegerResults = SearchResult.objects.filter(Q(campaign = keyword.campaign) & Q(Keywords = keyword) & Q(Schedule__date = today.date()))
                print(IntegerResults)
                if len(IntegerResults) < searchNumberInteger:
                    for x in range(int(searchNumberInteger) - len(IntegerResults)):
                        print(x) 
                        # Generate random datetime from datetime.datetime values
                        startDate = (today+ timedelta(days=1)).replace(hour=00, minute=00, second=00)
                        endDate = (today+ timedelta(days=1)).replace(hour=23, minute=59, second=59)
                        print(startDate)
                        print(endDate)
                        random_date_time = radar.random_datetime(
                            start = startDate,
                            stop = endDate
                        )
                        print()
                        print(random_date_time)
                        obj_status = SearchResult.objects.create(campaign = keyword.campaign, Keywords = keyword, website_title = keyword.campaign.title, Schedule = random_date_time,active_device = keyword.getDeviceType)

                        print(obj_status)
            if searchNumberDecimal > 0:
                daysForDecimal = math.ceil(math.ceil((1/searchNumberDecimal)*100)/100)
                integerDailySearches = math.floor((perDaysSearches * daysForDecimal))
                perDaysSearches = math.floor((perDaysSearches * daysForDecimal) + 1)
                days = daysForDecimal
                if integerDailySearches < perDaysSearches:
                    print("------",daysForDecimal)
                    print(perDaysSearches)
                    print(days)
                    startDate = (today+ timedelta(days=1)).replace(hour=00, minute=00, second=00)
                    endDate = (today+ timedelta(days=1+days)).replace(hour=23, minute=59, second=59)
                    print(startDate)
                    print(endDate)
                    decimalResults = SearchResult.objects.filter(Q(campaign = keyword.campaign) & Q(Keywords = keyword) & Q(Schedule__gte = startDate) & Q(Schedule__lte = endDate))
                    print(decimalResults)
                    if len(decimalResults) < perDaysSearches:
                        
                        random_date_time = radar.random_datetime(
                            start = startDate,
                            stop = endDate
                        )
                        print()
                        print(random_date_time)
                        obj_status = SearchResult.objects.create(campaign = keyword.campaign, Keywords = keyword, website_title = keyword.campaign.title, Schedule = random_date_time,active_device = keyword.getDeviceType)
                        print(obj_status)
        else:
            # add search results records for integer value
            mapDirectionStatus = False
            if searchNumberInteger > 0:
                IntegerResults = SearchResult.objects.filter(Q(campaign = keyword.campaign) & Q(Keywords = keyword) & Q(Schedule__date = today.date()))
                # logic for map driection start
                IntegerResultsMapCount = IntegerResults.filter(map_campaign_direction = False).count()
                IntegerResultsMapDirectionCount = IntegerResults.filter(map_campaign_direction = True).count()
                if IntegerResultsMapCount > IntegerResultsMapDirectionCount:
                    mapDirectionStatus = True
                # logic for map driection end
                print(IntegerResults)
                if len(IntegerResults) < searchNumberInteger:
                    for x in range(int(searchNumberInteger) - len(IntegerResults)):
                        print(x) 
                        # Generate random datetime from datetime.datetime values
                        startDate = (today+ timedelta(days=1)).replace(hour=00, minute=00, second=00)
                        endDate = (today+ timedelta(days=1)).replace(hour=23, minute=59, second=59)
                        print(startDate)
                        print(endDate)
                        random_date_time = radar.random_datetime(
                            start = startDate,
                            stop = endDate
                        )
                        print()
                        print(random_date_time)
                        obj_status = SearchResult.objects.create(campaign = keyword.campaign, Keywords = keyword, website_title = keyword.campaign.title, Schedule = random_date_time,active_device = keyword.getDeviceType,map_campaign_direction = mapDirectionStatus)
                        mapDirectionStatus = not mapDirectionStatus

                        print(obj_status)


            if searchNumberDecimal > 0:

                IntegerResults = SearchResult.objects.filter(Q(campaign = keyword.campaign) & Q(Keywords = keyword) & Q(Schedule__date = today.date()))
                # logic for map driection start
                IntegerResultsMapCount = IntegerResults.filter(map_campaign_direction = False).count()
                IntegerResultsMapDirectionCount = IntegerResults.filter(map_campaign_direction = True).count()
                if IntegerResultsMapCount > IntegerResultsMapDirectionCount:
                    mapDirectionStatus = True
                # logic for map driection end

                daysForDecimal = math.ceil(math.ceil((1/searchNumberDecimal)*100)/100)
                integerDailySearches = math.floor((perDaysSearches * daysForDecimal))
                perDaysSearches = math.floor((perDaysSearches * daysForDecimal) + 1)
                days = daysForDecimal
                if integerDailySearches < perDaysSearches:
                    print("------",daysForDecimal)
                    print(perDaysSearches)
                    print(days)
                    startDate = (today+ timedelta(days=1)).replace(hour=00, minute=00, second=00)
                    endDate = (today+ timedelta(days=1+days)).replace(hour=23, minute=59, second=59)
                    print(startDate)
                    print(endDate)
                    decimalResults = SearchResult.objects.filter(Q(campaign = keyword.campaign) & Q(Keywords = keyword) & Q(Schedule__gte = startDate) & Q(Schedule__lte = endDate))
                    print(decimalResults)
                    if len(decimalResults) < perDaysSearches:
                        
                        random_date_time = radar.random_datetime(
                            start = startDate,
                            stop = endDate
                        )
                        print()
                        print(random_date_time)
                        obj_status = SearchResult.objects.create(campaign = keyword.campaign, Keywords = keyword, website_title = keyword.campaign.title, Schedule = random_date_time,active_device = keyword.getDeviceType,map_campaign_direction = mapDirectionStatus)
                        print(obj_status)
        

def run_keyword_search_schedule():
    today = datetime.today()
    schedule_time_range = today - timedelta(minutes=30)
    keyword_search_data = SearchResult.objects.filter(Q(Schedule__gte = schedule_time_range) & Q(Schedule__lte = today))
    for obj in keyword_search_data:
        try:
            if obj.campaign.search_type == 'googlemap':
                if obj.map_campaign_direction:
                    if obj.active_device == 2:
                        found_website_in_map,found_in_mappack,knowledge_panel_found,direction_found,map_websites_list,position_of_website,bussiness_text = map_search_direction_mobile(obj.Keywords.keyword,obj.campaign.website, obj.Keywords.country, obj.Keywords.state, obj.Keywords.city, obj.campaign.business_name)
                        print(found_website_in_map,found_in_mappack,direction_found,knowledge_panel_found)
                        if found_website_in_map or found_in_mappack:
                            obj.found_index = True
                        map_websites_list, position_of_website = ListSkipAids(map_websites_list,obj.campaign.website,obj.campaign.business_name if bussiness_text else None)
                        obj.rank = position_of_website
                        obj.result = ','.join(map_websites_list)
                        obj.direction = direction_found
                        obj.knowledge_panel = knowledge_panel_found
                        obj.status = True
                        obj.save()
                    else:
                        found_website_in_map,found_in_mappack,direction_found,knowledge_panel_found,direction_list,map_websites_list,map_page,bussiness_text = map_search_direction_web(obj.Keywords.keyword,obj.campaign.website, obj.Keywords.country, obj.Keywords.state, obj.Keywords.city,obj.campaign.business_name)
                        print(found_website_in_map,found_in_mappack,direction_found,knowledge_panel_found,direction_list,map_websites_list,map_page)
                        if found_website_in_map or found_in_mappack:
                            obj.found_index = True
                        map_websites_list, map_page = ListSkipAids(map_websites_list, obj.campaign.website,obj.campaign.business_name if bussiness_text else None)
                        obj.direction = direction_found
                        obj.result = ','.join(map_websites_list)
                        if map_page:
                            obj.rank = map_page
                        if direction_found:
                            obj.direction_URL = direction_list
                        obj.knowledge_panel = knowledge_panel_found
                        obj.status = True
                        obj.save()
                        print(direction_list)
                else:
                    if obj.active_device == 2:
                        # found_website_in_map,found_in_mappack,visit_pages_on_web,map_page,direction_found,search_device_type,knowledge_panel_found
                        found_website_in_map,found_in_mappack,visit_pages_on_web,knowledge_panel_found,web_found_status,direction_found,websites_list,position_of_website,bussiness_text = map_search_mobile(obj.Keywords.keyword,obj.campaign.website, obj.Keywords.country, obj.Keywords.state, obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session, obj.campaign.business_name)
                        print(found_website_in_map,found_in_mappack,visit_pages_on_web,obj.campaign.business_name if bussiness_text else None)
                        if found_website_in_map or found_in_mappack:
                            obj.found_index = True
                        title = ''
                        url = ''
                        for item in visit_pages_on_web:
                            if title == '':
                                title = title + item[0]
                                url = url + item[1]
                            else:
                                title = title + ',' + item[0]
                                url = url + ',' + item[1]
                        obj.pages = url
                        obj.titles = title
                        obj.direction = direction_found
                        obj.knowledge_panel = knowledge_panel_found
                        websites_list, position_of_website = ListSkipAids(websites_list, obj.campaign.website) 
                        obj.rank = position_of_website
                        obj.result = ','.join(websites_list)
                        obj.status = True
                        obj.save()
                    else:
                        # found_website_in_map,found_in_mappack,visit_pages_on_web,map_page,direction_found,search_device_type,knowledge_panel_found
                        found_website_in_map,found_in_mappack,visit_pages_on_web,map_page,knowledge_panel_found,direction_found,websites_list,bussiness_text = map_search_web(obj.Keywords.keyword,obj.campaign.website, obj.Keywords.country, obj.Keywords.state, obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session,obj.campaign.business_name)
                        print(found_website_in_map,found_in_mappack,visit_pages_on_web,map_page)
                        if found_website_in_map or found_in_mappack:
                            obj.found_index = True
                        websites_list, map_page = ListSkipAids(websites_list, obj.campaign.website,obj.campaign.business_name if bussiness_text else None)
                        if map_page:
                            obj.rank = map_page
                        obj.result = ','.join(websites_list)
                        title = ''
                        url = ''
                        for item in visit_pages_on_web:
                            if title == '':
                                title = title + item[0]
                                url = url + item[1]
                            else:
                                title = title + ',' + item[0]
                                url = url + ',' + item[1]
                        obj.pages = url
                        obj.titles = title
                        obj.direction = direction_found
                        obj.knowledge_panel = knowledge_panel_found
                        obj.status = True
                        obj.save()
            else:
                if obj.active_device == 2:
                    site_found_status,site_found_index,all_website_list,visit_pages_on_web,knowledge_panel_found = keyword_search_mobile(obj.Keywords.keyword,obj.campaign.website, obj.Keywords.country, obj.Keywords.state, obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session)
                else:
                    site_found_status,site_found_index,all_website_list,visit_pages_on_web,knowledge_panel_found = keyword_search_web(obj.Keywords.keyword,obj.campaign.website, obj.Keywords.country, obj.Keywords.state, obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session)
                
                obj.found_index = site_found_status
                # added
                all_website_list, site_found_index = ListSkipAids(all_website_list, obj.campaign.website)
                obj.rank = site_found_index
                obj.result = ','.join(all_website_list)
                title = ''
                url = ''
                for item in visit_pages_on_web:
                    if title == '':
                        title = title + item[0]
                        url = url + item[1]
                    else:
                        title = title + ',' + item[0]
                        url = url + ',' + item[1]
                obj.pages = url
                obj.titles = title
                obj.status = True
                obj.knowledge_panel = knowledge_panel_found
                obj.save()
        except Exception as e:
            print(e)
            obj.rank = 0
            obj.status = True
            obj.save()