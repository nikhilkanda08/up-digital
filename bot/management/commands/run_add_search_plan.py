from django.core.management.base import BaseCommand, CommandError

from bot.utils.searchPlan import addSearchPlan

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('operation started')
        print(addSearchPlan())
        print('operation ended')