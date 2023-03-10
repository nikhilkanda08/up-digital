from django.core.management.base import BaseCommand, CommandError

from bot.utils.keyword_search import keyword_search
from bot.models import *
from bot.utils.keyword_search_mobile import keyword_search_mobile
from bot.utils.keyword_search_web import keyword_search_web

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('id', type=int)
    def handle(self, *args, **kwargs):
        print('operation started')
        id = kwargs['id']
        # try:
        obj = SearchResult.objects.get(id = id)
        # print(keyword_search("dogsblog","www.dogsblog.com"))
        # print(keyword_search(obj.Keywords.keyword,obj.campaign.website))
        # time_to_visit_site,country,city,state

        # keyword,website_link,country,state,city,time_to_visit,page_visit_no,search_device_type
        # site_found_status,site_found_index,all_website_list,visit_pages_on_web_after,knowledge_panel_found,search_device_type
        if obj.active_device == 2:
            site_found_status,site_found_index,all_website_list,visit_pages_on_web,knowledge_panel_found = keyword_search_mobile(obj.Keywords.keyword,obj.campaign.website, obj.Keywords.country, obj.Keywords.state, obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session)
        else:
            site_found_status,site_found_index,all_website_list,visit_pages_on_web,knowledge_panel_found = keyword_search_web(obj.Keywords.keyword,obj.campaign.website, obj.Keywords.country, obj.Keywords.state, obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session)

        obj.found_index = site_found_status
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
        print('operation ended')
        # except:
        #     print("finish")
        #     pass