from django.core.management.base import BaseCommand, CommandError

from bot.utils.keyword_search import keyword_search

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('operation started')
        # keyword_search("friends","https://www.facebook.com/")
        print(keyword_search("dogsblog","www.dogsblog.com"))
        print('operation ended')