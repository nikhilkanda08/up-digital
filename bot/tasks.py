from up_digital.celery import app
import logging
from .utils import keyword_search_schedule
logger = logging.getLogger('__name__')
@app.task
def send_reminder():
    print('start clery')
    logger.error(str('celery is working for shedule task'))
    keyword_search_schedule.run_keyword_search_schedule()
    # this will be used to send mail to all subscribed users
  
    return {'status': 'sent successfully'}