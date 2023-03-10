
import pytz 
from bot.models import *

def run_user_validity():
    today = datetime.utcnow().replace(tzinfo=pytz.UTC)
    users = User.objects.all()
    
    for user in users:
        try:
            obj = monthlyBillReport.objects.filter(user = User.objects.get(id=user.id)).latest('created_at')
            try:
                if obj.end >= today:
                    user.searches_status = True
                    user.save()
                else:
                    user.searches_status = False
                    user.save()
            except Exception as ex:
                print(ex)
                user.searches_status = False
                user.save()
        except:
            user.searches_status = False
            user.save()
