import os
from celery import Celery
from celery.schedules import crontab
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'up_digital.settings')
app = Celery('up_digital')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.beat_schedule = {
# Executes every Monday morning at 7:30 a.m.
'send-reminder': {
    # run this task every minute
    'task': 'bot.tasks.send_reminder',
    'schedule': crontab(minute=2),
  },
}