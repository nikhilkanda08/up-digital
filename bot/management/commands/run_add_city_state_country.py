from django.core.management.base import BaseCommand, CommandError

from bot.utils.cityStateCountry import addCityStateCountry

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('operation started')
        print(addCityStateCountry())
        print('operation ended')