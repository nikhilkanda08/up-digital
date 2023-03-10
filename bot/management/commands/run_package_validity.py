from django.core.management.base import BaseCommand, CommandError

from bot.utils.package_validity import run_user_validity

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print('operation started')
        run_user_validity()
        print('operation ended')