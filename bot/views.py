import logging
from ast import keyword
from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.http import HttpResponseRedirect, JsonResponse, BadHeaderError, HttpResponse, Http404

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from bot.forms import *
from django.db.models import Count
from dateutil.relativedelta import relativedelta

# from django.utils.http import is_safe_url

from bot.Utils import *
from bot.Utils import ListSkipAids
import json
from decimal import Decimal

from django.core.mail import EmailMessage
from django.template.loader import get_template
# Create your views here.

# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from rest_auth.registration.views import SocialLoginView

# stripe
import stripe
from django.conf import settings

from bot.utils.keyword_search import *
from bot.utils.keyword_search_mobile import keyword_search_mobile
from bot.utils.keyword_search_web import keyword_search_web
from bot.utils.map_search import map_search
from bot.utils.map_search_direction import map_search_direction
from bot.utils.map_search_direction_mobile import map_search_direction_mobile
from bot.utils.map_search_direction_web import map_search_direction_web
from bot.utils.map_search_mobile import map_search_mobile
from bot.utils.map_search_web import map_search_web

#paypal
from paypal.standard.forms import PayPalPaymentsForm




stripe.api_key = settings.STRIPE_PRIVATE_KEY
# YOUR_DOMAIN = 'http://localhost:8000'
YOUR_DOMAIN = 'http://137.184.107.221'

logger = logging.getLogger('__name__')

# logger.debug('This is a debug message=>')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')


def test(request):
    return render(request, 'payment.html')

def landingPage(request):
    return render(request, 'landing.html')

def pricing(request):
    return render(request, 'pricing.html')

@login_required(login_url="/sign-in/")
def dashboard(request):
    # if pk:
    # print("check => ",request.GET.get('session_id', ''))
        # print(pk)
    if(request.GET.get('session_id', '')):
        logger.debug(f'payment session back url')
        session = stripe.checkout.Session.retrieve(request.GET.get('session_id', ''))
        customer = stripe.Customer.retrieve(session.customer)
        # print("session")
        # print(session)
        # print("customer")
        # print(customer)
        # print(session['customer'])
        # print(session['subscription'])
        # print(stripe.Charge.retrieve(request.GET.get('session_id', ''),expand=['customer', 'invoice.subscription']))
        try:
            subscriptionObj = Subscription.objects.get(subscriptionID = request.GET.get('session_id', ''), user = User.objects.get(id = request.user.id))
            subscriptionObj.paid = True
            subscriptionObj.subscriptionNumber = session['subscription']
            subscriptionObj.clientID = session['customer']
            subscriptionObj.save()
            userObj = User.objects.get(id = request.user.id)
            userObj.searches_status = True
            userObj.save()
            return HttpResponseRedirect("/")
        except:
            logger.debug(f'Could not find the subscription with the provided ID.')
            return HttpResponseRedirect("/")

    current_month = datetime.now().month
    last_month = (datetime.now().replace(day=1) - timedelta(days=1)).month
    data = {}
    data['campaign_count'] = Campaign.objects.filter(user = User.objects.get(id=request.user.id)).count()
    campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
    campaign_list =  Campaign.objects.filter(user = User.objects.get(id=request.user.id)).values_list('id')
    keywords = Keywords.objects.filter(campaign__in = campaign)
    data['allowed_searches'] = User.objects.get(id=request.user.id).searches
    searches_current_month = SearchResult.objects.filter(campaign__in = campaign_list, created_at__month = current_month).count()
    keywords_current_month = Keywords.objects.filter(campaign__in = campaign, created_at__month = current_month).count()
    # mobile searches monthly
    searches_current_month_groups = SearchResult.objects.filter(campaign__in = campaign, created_at__month = current_month).values('campaign__mobile_Searches').annotate(total=Count('campaign__mobile_Searches')).order_by('total')
    if len(searches_current_month_groups):
        data['searches_current_month_mobile'] = searches_current_month_groups[0]['campaign__mobile_Searches']
        data['searches_current_month_others'] = 100 - searches_current_month_groups[0]['campaign__mobile_Searches']
    else:
        data['searches_current_month_mobile'] = 0
        data['searches_current_month_others'] = 100

    # active campaigns
    active_campaigns = campaign.filter(is_active = True).count()
    active_campaigns_percentage = is_what_percent_of(active_campaigns,len(campaign))
    data['active_campaigns'] = active_campaigns
    data['active_campaigns_percentage'] = round(Decimal((str(active_campaigns_percentage))), 2)
    # organic_search campaign
    organic_search_campaigns = campaign.filter(search_type = 'organic_search').count()
    organic_search_campaigns_percentage = is_what_percent_of(organic_search_campaigns,len(campaign))
    data['organic_search_campaigns'] = organic_search_campaigns
    data['organic_search_campaigns_percentage'] = round(Decimal((str(organic_search_campaigns_percentage))), 2)
    data['total_per_day_search_allowed'] = round(Decimal((str(request.user.searches))), 2)
    
    total_per_day_search_data = Keywords.objects.filter(campaign__in = campaign).aggregate(total=Sum('searches_per_day'))
    try:
        if total_per_day_search_data:
            data['total_per_day_search'] = round(Decimal((str(total_per_day_search_data['total']))), 2)
        else:
            data['total_per_day_search'] = 0.00
    except:
        data['total_per_day_search'] = 0.00

    # last 6 month keywords counts
    keywords_history = Keywords.objects.filter(
        campaign__in = campaign,
        created_at__gte=datetime.today() - relativedelta(months=6),
    ).values(
        'created_at__month'
    ).annotate(
        count=Count('id')
    ).order_by('-created_at__month')

    keywords_history = {month_name(r['created_at__month']): r['count'] for r in keywords_history}
    # keywords_history = dict((month_name(r['created_at__month']), r['count']) for r in keywords_history)
    print("keywords_history")
    print(keywords_history)

    # last 6 month search results counts
    search_result_history = SearchResult.objects.filter(
        campaign__in = campaign,
        created_at__gte=datetime.today() - relativedelta(months=6),
    ).values(
        'created_at__month'
    ).annotate(
        count=Count('id')
    ).order_by('created_at__month')

    search_result_history = {month_name(r['created_at__month']): r['count'] for r in search_result_history}

    # activities
    # , status=True
    SearchResultData = SearchResult.objects.filter(status = True,campaign__user=User.objects.get(id=request.user.id)).order_by('-id')[:8][::-1]
    # print("=>",SearchResultData)

    # # arrow icon status
    current_month_campaigns = campaign.filter(is_active = True, created_at__month = current_month).count()
    last_month_campaigns = campaign.filter(is_active = True, created_at__month = last_month).count()
    campaignsArrowStatus, campaignsArrowScore = get_number_to_number_percentage(current_month_campaigns, last_month_campaigns)

    currentMonthSearchesArrow = SearchResult.objects.filter(campaign__in = campaign_list, created_at__month = current_month).count()
    lastMonthSearchesArrow = SearchResult.objects.filter(campaign__in = campaign_list, created_at__month = last_month).count()
    currentMonthSearchesArrowStatus, currentMonthSearchesArrowScore = get_number_to_number_percentage(currentMonthSearchesArrow, lastMonthSearchesArrow)
    
    return render(request, 'dashboard.html',{"SearchResultData":SearchResultData,"data_dict":data,"campaign":campaign, "keywords":keywords, "searches_current_month": searches_current_month, "keywords_current_month":keywords_current_month, "current_month":current_month,"keywords_history":json.dumps(keywords_history),"search_result_history":json.dumps(search_result_history),
    "campaignsArrowStatus":campaignsArrowStatus,"campaignsArrowScore":campaignsArrowScore,
    "currentMonthSearchesArrowStatus":currentMonthSearchesArrowStatus,"currentMonthSearchesArrowScore":currentMonthSearchesArrowScore})

def sign_in(request):
    return render(request, 'overlay/sign-in.html')

def sign_up(request):
    return render(request, 'overlay/sign-up.html')


def create_account(request):
    if request.method == 'POST':
        create_account_form = UserCreationForm(request.POST)
        if create_account_form.is_valid():
            user = create_account_form.save()
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('bot:dashboard'))
            return render(request, 'overlay/sign-up.html',{"error":"error"})
        else:
            print(list(dict((create_account_form.errors)).values())[0])
            return render(request, 'overlay/sign-up.html',{"error":list(dict((create_account_form.errors)).values())[0]})
    return render(request, 'overlay/sign-up.html',{"error":"error"})

@csrf_exempt
def user_login(request):
    try:
        login_form = LoginForm()
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.user
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                redirect_to = request.GET.get('next', '')
                # if is_safe_url(url=redirect_to, allowed_hosts=request.get_host()):
                #     return HttpResponseRedirect(redirect_to)
                # else:
                #     return HttpResponseRedirect(reverse('bot:dashboard'))
                return HttpResponseRedirect(reverse('bot:dashboard'))
            else:
                return render(request, 'overlay/sign-in.html',{"error":list(dict((login_form.errors)).values())[0]})
    except Exception as e:
        return render(request, 'overlay/sign-in.html',{"error":e})

@login_required(login_url="/sign-in/")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

@csrf_exempt
@login_required(login_url="/sign-in/")
def admin_reset_password(request):
    if request.method == 'POST':
        if not request.user.is_staff:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        data = request.POST
        user = User.objects.get(id=data['id']) 
        user.set_password(data['password1'])
        user.save()
        return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)

@csrf_exempt
@login_required(login_url="/sign-in/")
def change_password(request):
    if request.method == 'POST':
        data = request.POST
        user = User.objects.get(id=request.user.id) 
        user.set_password(data['password1'])
        user.save()
        return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)

def reset_pwd(request):
    return render(request, 'overlay/reset-password.html')

@csrf_exempt
def reset_pwd_OTP(request):
    if request.method == 'POST':
        try:
            data = request.POST
            email = data['email']
            try:
                user = User.objects.get(email=email)
                OTP = random.randint(100000,999999)
                user.OTP = OTP
                user.save()
            except:
                return JsonResponse({"status":"false","msg":"No user with this email"},status=status.HTTP_200_OK)    
            
            message = get_template("OTP.html").render({
                'OTP': OTP, 'email':email
            })
            email = EmailMessage(
                'CTR Boss Password Reset',
                message,
                settings.EMAIL_HOST_USER,
                to=[email, ],
            )
            email.content_subtype = "html"
            email.send(fail_silently=True)
            return JsonResponse({"status":"true"},status=status.HTTP_200_OK)
        except:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

def OTP_page(request,email):
    return render(request, 'overlay/two-steps.html',{"email":email})

@csrf_exempt
def validate_OTP(request):
    if request.method == 'POST':
        try:
            data = request.POST
            print(data)
            email = data['email']
            OTP = data['code_1'] + data['code_2'] + data['code_3'] + data['code_4'] + data['code_5'] + data['code_6'] 
            try:
                user = User.objects.get(email=email)

                if str(user.OTP) == OTP:
                    return render(request, "overlay/new-password.html",{"email":email,"OTP":OTP})
                else:
                    return render(request, "overlay/two-steps.html",{"email":email,"error":"Wrong OTP. Try Again"})
            except:
                return render(request, "overlay/two-steps.html",{"email":email,"error":"Something is wrong."})
        except Exception as e:
            return render(request, "overlay/two-steps.html",{"email":email,"error":e})
@csrf_exempt
def new_pwd(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        email = data['email']
        OTP = data['OTP']
        password = data['password']
        confirm_password = data['confirm-password']
        try:
            user = User.objects.get(email=email)
            if str(user.OTP) == OTP:
                if password == confirm_password:
                    user.set_password(data['password'])
                    user.OTP = None
                    user.save()
                    return HttpResponseRedirect(reverse('bot:sign_in'))
                else:
                    return render(request, "overlay/new-password.html",{"email":email,"OTP":OTP,"error":"Password Mismatch."})    
            else:
                return render(request, "overlay/new-password.html",{"email":email,"OTP":OTP,"error":"Something Wrong. Try Again"})
        except:
            return render(request, "overlay/new-password.html",{"email":email,"OTP":OTP,"error":"Something Wrong. Try Again"})


# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter
    
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter

@csrf_exempt
@login_required(login_url="/sign-in/")
def campaign_apis(request):
    if request.method == 'GET':
        return render(request, 'campaign.html')
    if request.method == 'POST':
        try:
            data = request.POST
            search_type = "organic_search" 
            if data['camp_search_type'] == '1':
                search_type = "googlemap"
            obj = Campaign.objects.create(title = data['camp_title'], business_name= data['business_name'], search_type = search_type, website = data['website_url'], user = User.objects.get(id = request.user.id))
            return JsonResponse({"status":"true","id":obj.id},status=status.HTTP_202_ACCEPTED)
        except:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({"status":"true"})

@csrf_exempt
@login_required(login_url="/sign-in/")
def campaign_update(request):
    if request.method == 'POST':
        try:
            data = request.POST
            # print(data)
            try:
                # validate the time and number of pages
                SearchPlanData = SearchPlan.objects.get(daily_searches=request.user.searches)
                # data = data[0]
                if int(data['pages']) > int(SearchPlanData.total_pages) or int(data['session_time']) > int(SearchPlanData.onsite_time):
                    return JsonResponse({"status":"False", "msg":"Validation failed"},status=status.HTTP_202_ACCEPTED)
                pass
            except:
                print("validation failed")

            obj = Campaign.objects.get(id=data['id'],user = User.objects.get(id=request.user.id))
            obj.title = data['name']
            obj.website = data['website']
            obj.mobile_Searches = data['mobile_search']
            obj.bounce_rate = data['bounce']
            obj.pages_per_session = data['pages']
            obj.avg_session_duration = data['session_time']
            obj.description = data['description']
            obj.is_active = True if data['active'] == 'true' else False
            # obj.search_type = data['search_type']
            obj.save()

            return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)
        except:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
@login_required(login_url="/sign-in/")
def campaign_detail(request,pk):
    if request.method == 'GET':
        data = Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id))
        keywords_data = Keywords.objects.filter(campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id))).order_by('searches_per_day')
        Search_result_data = SearchResult.objects.filter(status=True, campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))

        data_dict = {}
        data_dict['campaign_count'] = Campaign.objects.filter(user = User.objects.get(id=request.user.id)).count()
        campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
        keywords = Keywords.objects.filter(campaign__in = campaign)
        data_dict['allowed_searches'] = User.objects.get(id=request.user.id).searches

        # search plan
        try:
            searchPlan = SearchPlan.objects.filter(daily_searches=request.user.searches).values("total_pages","onsite_time")
            searchPlan = list(searchPlan)[0]
        except:
            searchPlan = []

        current_month = datetime.now().month
        last_month = (datetime.now().replace(day=1) - timedelta(days=1)).month
        current_keywords_data = keywords_data.filter(created_at__month = current_month).count()
        last_keywords_data = keywords_data.filter(created_at__month = last_month).count()
        keywordArrowStatus, keywordArrowScore = get_number_to_number_percentage(current_keywords_data, last_keywords_data)
        current_Search_result_data = Search_result_data.filter(created_at__month = current_month).count()
        last_Search_result_data = Search_result_data.filter(created_at__month = last_month).count()
        searchResultArrowStatus, searchResultArrowScore = get_number_to_number_percentage(current_Search_result_data, last_Search_result_data)

        return render(request, 'campaign/overview.html',{"searchPlan":searchPlan, "data":data, "keywords_data":keywords_data, "data_dict":data_dict,"campaign":campaign, "keywords":keywords,'Search_result_data':Search_result_data, "active":"overview", "keywordArrowStatus":keywordArrowStatus, "searchResultArrowStatus":searchResultArrowStatus})
    elif request.method == 'PUT':
        return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        try:
            Campaign.objects.get(id=pk,user = User.objects.get(id=request.user.id)).delete()
            return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)
        except:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url="/sign-in/")
def campaign_detail_keywords(request,pk):
    if request.method == 'GET':
        data = Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id))
        keywords_data = Keywords.objects.filter(campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))
        Search_result_data = SearchResult.objects.filter(status=True, campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))

        data_dict = {}
        data_dict['campaign_count'] = Campaign.objects.filter(user = User.objects.get(id=request.user.id)).count()
        campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
        keywords = Keywords.objects.filter(campaign__in = campaign)
        data_dict['allowed_searches'] = User.objects.get(id=request.user.id).searches

        current_month = datetime.now().month
        last_month = (datetime.now().replace(day=1) - timedelta(days=1)).month
        current_keywords_data = keywords_data.filter(created_at__month = current_month).count()
        last_keywords_data = keywords_data.filter(created_at__month = last_month).count()
        keywordArrowStatus, keywordArrowScore = get_number_to_number_percentage(current_keywords_data, last_keywords_data)
        current_Search_result_data = Search_result_data.filter(created_at__month = current_month).count()
        last_Search_result_data = Search_result_data.filter(created_at__month = last_month).count()
        searchResultArrowStatus, searchResultArrowScore = get_number_to_number_percentage(current_Search_result_data, last_Search_result_data)
 
        return render(request, 'campaign/keywords.html',{"data":data, "keywords_data":keywords_data, "data_dict":data_dict,"campaign":campaign, "keywords":keywords, "active":"keyword",'Search_result_data':Search_result_data, "keywordArrowStatus":keywordArrowStatus, "searchResultArrowStatus":searchResultArrowStatus})

@csrf_exempt
@login_required(login_url="/sign-in/")
def campaign_detail_searches(request,pk):
    if request.method == 'GET':
        data = Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id))
        keywords_data = Keywords.objects.filter(campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))
        Search_result_data = SearchResult.objects.filter(status=True, campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))

        data_dict = {}
        data_dict['campaign_count'] = Campaign.objects.filter(user = User.objects.get(id=request.user.id)).count()
        campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
        keywords = Keywords.objects.filter(campaign__in = campaign)
        data_dict['allowed_searches'] = User.objects.get(id=request.user.id).searches
        SearchResultData = SearchResult.objects.filter(campaign = Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)), Keywords__in = keywords_data, status = True)

        current_month = datetime.now().month
        last_month = (datetime.now().replace(day=1) - timedelta(days=1)).month
        current_keywords_data = keywords_data.filter(created_at__month = current_month).count()
        last_keywords_data = keywords_data.filter(created_at__month = last_month).count()
        keywordArrowStatus, keywordArrowScore = get_number_to_number_percentage(current_keywords_data, last_keywords_data)
        current_Search_result_data = Search_result_data.filter(created_at__month = current_month).count()
        last_Search_result_data = Search_result_data.filter(created_at__month = last_month).count()
        searchResultArrowStatus, searchResultArrowScore = get_number_to_number_percentage(current_Search_result_data, last_Search_result_data)
 
        return render(request, 'campaign/searches.html',{"data":data, "keywords_data":keywords_data, "data_dict":data_dict,"campaign":campaign, "keywords":keywords,"SearchResultData":SearchResultData, "active":"search",'Search_result_data':Search_result_data, "keywordArrowStatus":keywordArrowStatus, "searchResultArrowStatus":searchResultArrowStatus})

@csrf_exempt
@login_required(login_url="/sign-in/")
def campaign_detail_schedule_searches(request,pk):
    if request.method == 'GET':
        data = Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id))
        keywords_data = Keywords.objects.filter(campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))
        Search_result_data = SearchResult.objects.filter(status=True, campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))

        data_dict = {}
        data_dict['campaign_count'] = Campaign.objects.filter(user = User.objects.get(id=request.user.id)).count()
        campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
        keywords = Keywords.objects.filter(campaign__in = campaign)
        data_dict['allowed_searches'] = User.objects.get(id=request.user.id).searches
        SearchResultData = SearchResult.objects.filter(campaign = Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)), Keywords__in = keywords_data, status = False)

        current_month = datetime.now().month
        last_month = (datetime.now().replace(day=1) - timedelta(days=1)).month
        current_keywords_data = keywords_data.filter(created_at__month = current_month).count()
        last_keywords_data = keywords_data.filter(created_at__month = last_month).count()
        keywordArrowStatus, keywordArrowScore = get_number_to_number_percentage(current_keywords_data, last_keywords_data)
        current_Search_result_data = Search_result_data.filter(created_at__month = current_month).count()
        last_Search_result_data = Search_result_data.filter(created_at__month = last_month).count()
        searchResultArrowStatus, searchResultArrowScore = get_number_to_number_percentage(current_Search_result_data, last_Search_result_data)
 
        return render(request, 'campaign/scheduleSearches.html',{"data":data, "keywords_data":keywords_data, "data_dict":data_dict,"campaign":campaign, "keywords":keywords,"SearchResultData":SearchResultData, "active":"schedule",'Search_result_data':Search_result_data, "keywordArrowStatus":keywordArrowStatus, "searchResultArrowStatus":searchResultArrowStatus})

@csrf_exempt
@login_required(login_url="/sign-in/")
def campaign_detail_activity(request,pk):
    if request.method == 'GET':
        data = Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id))
        keywords_data = Keywords.objects.filter(campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))
        Search_result_data = SearchResult.objects.filter(status=True, campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))

        data_dict = {}
        data_dict['campaign_count'] = Campaign.objects.filter(user = User.objects.get(id=request.user.id)).count()
        campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
        keywords = Keywords.objects.filter(campaign__in = campaign)
        data_dict['allowed_searches'] = User.objects.get(id=request.user.id).searches
        SearchResultData = SearchResult.objects.filter(campaign = Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)), Keywords__in = keywords_data, status = True)

        current_month = datetime.now().month
        last_month = (datetime.now().replace(day=1) - timedelta(days=1)).month
        current_keywords_data = keywords_data.filter(created_at__month = current_month).count()
        last_keywords_data = keywords_data.filter(created_at__month = last_month).count()
        keywordArrowStatus, keywordArrowScore = get_number_to_number_percentage(current_keywords_data, last_keywords_data)
        current_Search_result_data = Search_result_data.filter(created_at__month = current_month).count()
        last_Search_result_data = Search_result_data.filter(created_at__month = last_month).count()
        searchResultArrowStatus, searchResultArrowScore = get_number_to_number_percentage(current_Search_result_data, last_Search_result_data)
 

        return render(request, 'campaign/activity.html',{"data":data, "keywords_data":keywords_data, "data_dict":data_dict,"campaign":campaign, "keywords":keywords,"SearchResultData":SearchResultData, "active":"activity",'Search_result_data':Search_result_data, "keywordArrowStatus":keywordArrowStatus, "searchResultArrowStatus":searchResultArrowStatus})

@csrf_exempt
@login_required(login_url="/sign-in/")
def campaign_detail_setting(request,pk):
    if request.method == 'GET':
        data = Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id))
        keywords_data = Keywords.objects.filter(campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))
        Search_result_data = SearchResult.objects.filter(status=True, campaign=Campaign.objects.get(id=pk, user = User.objects.get(id=request.user.id)))

        data_dict = {}
        data_dict['campaign_count'] = Campaign.objects.filter(user = User.objects.get(id=request.user.id)).count()
        campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
        keywords = Keywords.objects.filter(campaign__in = campaign)
        data_dict['allowed_searches'] = User.objects.get(id=request.user.id).searches
        # search plan
        try:
            searchPlan = SearchPlan.objects.filter(daily_searches=request.user.searches).values("total_pages","onsite_time")
            searchPlan = list(searchPlan)[0]
        except:
            searchPlan = []

        current_month = datetime.now().month
        last_month = (datetime.now().replace(day=1) - timedelta(days=1)).month
        current_keywords_data = keywords_data.filter(created_at__month = current_month).count()
        last_keywords_data = keywords_data.filter(created_at__month = last_month).count()
        keywordArrowStatus, keywordArrowScore = get_number_to_number_percentage(current_keywords_data, last_keywords_data)
        current_Search_result_data = Search_result_data.filter(created_at__month = current_month).count()
        last_Search_result_data = Search_result_data.filter(created_at__month = last_month).count()
        searchResultArrowStatus, searchResultArrowScore = get_number_to_number_percentage(current_Search_result_data, last_Search_result_data)

        return render(request, 'campaign/setting.html',{"searchPlan":searchPlan, "data":data, "keywords_data":keywords_data, "data_dict":data_dict,"campaign":campaign, "keywords":keywords, "active":"setting",'Search_result_data':Search_result_data, "keywordArrowStatus":keywordArrowStatus, "searchResultArrowStatus":searchResultArrowStatus})

@csrf_exempt
@login_required(login_url="/sign-in/")
def keyword_apis(request):
    if request.method == 'POST':
        try:
            data = request.POST 
            if request.user.searches_status:
                result = per_day_search_status(request.user.searches,request.user.id)
                # print(result['count'])
                # print(data['search_per_day'])
                # print(float(result['count'])>=float(data['search_per_day']))
                # print(float(data['search_per_day']) - float(result['count']))
                logger.debug(f'keyword status =>{float(result["count"])>=float(data["search_per_day"])}')
                if result['status']:
                    if float(result['count'])>=float(data['search_per_day']):
                        Keywords.objects.create(campaign = Campaign.objects.get(id = data['camp_id']),
                            keyword = data['keyword_str'], searches_per_day = data['search_per_day'], country = data['country_assign'], state = data['state_assign'], city = data['city_assign'],)
                        return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)
                    else:

                        return JsonResponse({"status":"false", "count":float(result['count'])},status=status.HTTP_202_ACCEPTED)    
                else:
                    return JsonResponse({"status":"false", "count":0},status=status.HTTP_202_ACCEPTED)
            else:
                return JsonResponse({"status":"false", "count":0},status=status.HTTP_202_ACCEPTED)
        except:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({"status":"true"})

@csrf_exempt
@login_required(login_url="/sign-in/")
def keyword_detail(request,pk):
    if request.method == 'DELETE':
        try:
            Keywords.objects.get(id=pk,campaign__in=Campaign.objects.filter(user = User.objects.get(id=request.user.id))).delete()
            return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)
        except:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url="/sign-in/")
def search_results(request,pk):
    if request.method == 'GET':
        SearchResultData = SearchResult.objects.filter(Keywords=Keywords.objects.get(id=pk, campaign__in=Campaign.objects.filter(user = User.objects.get(id=request.user.id))))
        Keyword=Keywords.objects.get(id=pk, campaign__in=Campaign.objects.filter(user = User.objects.get(id=request.user.id)))

        data_dict = {}
        data_dict['campaign_count'] = Campaign.objects.filter(user = User.objects.get(id=request.user.id)).count()
        campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
        keywords = Keywords.objects.filter(campaign__in = campaign)
        data_dict['allowed_searches'] = User.objects.get(id=request.user.id).searches

        return render(request, 'search_results.html',{"SearchResult":SearchResultData, "keyword":Keyword.keyword, "data_dict":data_dict,"campaign":campaign, "keywords":keywords})

@csrf_exempt
@login_required(login_url="/sign-in/")
def recent_searches(request):
    if request.method == 'GET':
        SearchResultData = SearchResult.objects.filter(status=True,campaign__user=User.objects.get(id=request.user.id)).order_by('-created_at')
        campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
        keywords = Keywords.objects.filter(campaign__in = campaign)

        return render(request, 'recentSearches.html',{"SearchResult":SearchResultData, "campaign":campaign, "keywords":keywords})

@csrf_exempt
@login_required(login_url="/sign-in/")
def search_result_detail(request,pk):
    if request.method == 'GET':
        SearchResultDetail = SearchResult.objects.get(id=pk,campaign__user=User.objects.get(id=request.user.id))
        data_dict = {}
        data_dict['campaign_count'] = Campaign.objects.filter(user = User.objects.get(id=request.user.id)).count()
        campaign = Campaign.objects.filter(user = User.objects.get(id=request.user.id))
        keywords = Keywords.objects.filter(campaign__in = campaign)
        data_dict['allowed_searches'] = User.objects.get(id=request.user.id).searches

        return render(request, 'result_details.html',{"SearchResultDetail":SearchResultDetail, "data_dict":data_dict,"campaign":campaign, "keywords":keywords})

#stripe_view view
@csrf_exempt
@login_required(login_url="/sign-in/")
def stripe_view(request, planID):
    return render(request,'payment/stripe/checkout.html',{"planID":planID})

#success view
@csrf_exempt
@login_required(login_url="/sign-in/")
def success(request):
    return render(request,'payment/stripe/success.html')
    
#cancel view
@csrf_exempt
@login_required(login_url="/sign-in/")
def cancel(request):
    return render(request,'payment/stripe/cancel.html')

@csrf_exempt
@login_required(login_url="/sign-in/")
def create_checkout_session(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    planID = body['planID']
    planObj = SearchPlan.objects.get(stripe_price_ID=planID)
    # try:
    userObj = User.objects.get(id=request.user.id)
    # print(userObj.id)
    # print("userObj")
    obj = Subscription.objects.filter(paid = True, user = User.objects.get(id=request.user.id)).last()
    if obj and obj.clientID:
        # print(obj)
        # # obj = obj[]
        # print(obj.clientID)
        # print("if")
        print(obj.subscriptionNumber)
        print(userObj.searches_status)
        print(obj.paid)
        # print(obj.paid and obj.subscriptionNumber and userObj.searches_status)
        if(obj.paid and obj.subscriptionNumber and userObj.searches_status):
            print("update the subscription")
            print(obj.subscriptionNumber, request.user.id)
            # update the subscription
            try:
                sessionID = stripeSubscriptionUpdate(obj.subscriptionNumber, request.user.id, planObj)
                return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)
            except:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST)            
        else:
            print("add the subscription with previou;y client ID")
            sessionID = stripeSubscription(request.user.id, planID, planObj, obj.clientID)
        return JsonResponse({'id': sessionID})
    else:
        print("add the subscription")
        sessionID = stripeSubscription(request.user.id, planID, planObj)
        return JsonResponse({'id': sessionID})
    # except:
    #     print("add the subscription with showing error")
    #     sessionID = stripeSubscription(request.user.id, planID)
    #     return JsonResponse({'id': sessionID})

@csrf_exempt
@login_required(login_url="/sign-in/")
def cancelStripeSubscription(request):
    try:
        if(stripeSubscriptionCancelation(request.user.id)):
            return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)     
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    except:
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def webhook_invoice_payment_scceeded(request):
    logger.debug(f'Stripe Trigger')
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        if body['type'] == "invoice.payment_succeeded":
            logger.debug(f'Invoice Payment Successed')
            # get the user with stripe client ID
            userObj = User.objects.get(strip_client_ID=body['data']['object']['customer'])
            datetimeObj = datetime.fromtimestamp(body['created'])
            datetimeEndObj = datetimeObj + relativedelta(months=1)
            total = 0
            if body['data']['object']['total']:
                total = (float(body['data']['object']['total']))/100
            paid = False
            if body['data']['object']['paid'] == 'True':
                paid = True
        
            status_obj = monthlyBillReport.objects.create(
                user=userObj,
                body_ID=body['id'],
                body_created=datetime.fromtimestamp(body['created']),
                account_name=body['data']['object']['account_name'],
                object_charge=body['data']['object']['charge'],
                charge=body['data']['object']['charge'],
                obj_created=datetime.fromtimestamp(body['data']['object']['created']),
                currency=body['data']['object']['currency'],
                customer=body['data']['object']['customer'],
                hosted_invoice_url=body['data']['object']['hosted_invoice_url'],
                invoice_pdf=body['data']['object']['invoice_pdf'],
                total=total,
                invoice_number=body['data']['object']['number'],
                payment_intent=body['data']['object']['payment_intent'],
                status=body['data']['object']['status'],
                paid=paid,
                period_end=datetime.fromtimestamp(body['data']['object']['period_end']),
                period_start=datetime.fromtimestamp(body['data']['object']['period_start']),
                request_id=body['request']['id'],
                request_idempotency_key=body['request']['idempotency_key'],
                start=datetimeObj,
                end=datetimeEndObj,
                )
        return JsonResponse({"status":"true"},status=status.HTTP_202_ACCEPTED)
    except Exception as ex:
        logger.debug(f'Error in Invoice Payment Successed {ex}')
        return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

#paypal_view view
def paypal_view(request):
    return render(request,'payment/paypal/payment.html')
    

def stripeSubscription(userID, planID, planObj, clientID=None):
    if clientID:
        session = stripe.checkout.Session.create(
        customer=clientID,
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price': planID,
            'quantity': 1
        }],
        success_url=YOUR_DOMAIN + '/?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        # print("session")
        # print(session)

        Subscription.objects.get_or_create(paid = False, amount = planObj.cost, subscriptionID = session.id, user = User.objects.get(id = userID))
        userObj = User.objects.get(id = userID)
        userObj.searches = planObj.daily_searches
        userObj.searches_status = False
        userObj.save()
        return session.id
    else:
        userObj = User.objects.get(id = userID)

        customer_data = stripe.Customer.create(
            email=userObj.email,
        )
        userObj.strip_client_ID = customer_data.id
        userObj.save()

        session = stripe.checkout.Session.create(
        customer=customer_data.id,
        payment_method_types=['card'],
        # line_items=[{
        #   'price_data': {
        #     'currency': 'usd',
        #     'product_data': {
        #       'name': 'Intro to Django Course',
        #     },
        #     'unit_amount': 10000,
        #   },
        #   'quantity': 1,
        # }],
        # mode='payment',
        mode='subscription',
        line_items=[{
            'price': planID,
            # For metered billing, do not pass quantity
            'quantity': 1
        }],
        success_url=YOUR_DOMAIN + '/?session_id={CHECKOUT_SESSION_ID}',
        # success_url=YOUR_DOMAIN + '/',
        cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        # print("session")
        # print(session)
        Subscription.objects.get_or_create(paid = False, amount = planObj.cost, subscriptionID = session.id, user = User.objects.get(id = userID))
        userObj = User.objects.get(id = userID)
        userObj.searches = planObj.daily_searches
        userObj.searches_status = False
        userObj.save()
        return session.id

def stripeSubscriptionCancelation(userID):
    try:
        userObj = User.objects.get(id = userID)
        # print(userObj.searches_status)
        if userObj.searches_status:
            data = Subscription.objects.filter(paid = True, user = User.objects.get(id = userID))
            if len(data) > 0:
                # print(data[len(data)-1].paid)
                # print(data[len(data)-1].subscriptionNumber)
                stripe.Subscription.delete(
                data[len(data)-1].subscriptionNumber,
                )
                userObj.searches_status = False
                userObj.save()
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def stripeSubscriptionUpdate(subscriptionNumber, userID, planObj):
    subscription = stripe.Subscription.retrieve(subscriptionNumber)
    session = stripe.Subscription.modify(
    subscription.id,
    cancel_at_period_end=False,
    proration_behavior='always_invoice',
    # proration_behavior='create_prorations',
    items=[{
        'id': subscription['items']['data'][0].id,
        'price': planObj.stripe_price_ID,
    }]
    )
    logger.debug(f'Session ID =>{session.id}')
    subscriptionObj, created = Subscription.objects.get_or_create(subscriptionNumber = subscriptionNumber, user = User.objects.get(id = userID))
    # subscriptionObj.paid = False
    subscriptionObj.amount = planObj.cost
    # subscriptionObj.subscriptionID = session.id
    subscriptionObj.save()
    userObj = User.objects.get(id = userID)
    userObj.searches = planObj.daily_searches
    # userObj.searches_status = False
    userObj.save()

    return True


@csrf_exempt
@login_required(login_url="/sign-in/")
def run_bot(request):
    if request.method == 'POST':
        print("here bot start")
        # try:
        data = request.POST
        # try:
        logger.debug(f'operation started')
        obj = SearchResult.objects.get(id=data['id'])
        # print(keyword_search("dogsblog","www.dogsblog.com"))
        # print(keyword_search(obj.Keywords.keyword,obj.campaign.website))
        # print(obj.Keywords.keyword,obj.campaign.website)
        if obj.campaign.search_type == 'googlemap':
            if obj.map_campaign_direction:
                if obj.active_device == 2:

                    # found_website_in_map,found_in_mappack,direction_found,search_device_type,knowledge_panel_found,direction_list
                    found_website_in_map, found_in_mappack, knowledge_panel_found, direction_found, map_websites_list, position_of_website,bussiness_text = map_search_direction_mobile(
                        obj.Keywords.keyword, obj.campaign.website, obj.Keywords.country, obj.Keywords.state,
                        obj.Keywords.city, obj.campaign.business_name)
                    print(found_website_in_map, found_in_mappack, knowledge_panel_found, direction_found, map_websites_list,position_of_website,bussiness_text)

                    if found_website_in_map or found_in_mappack:
                        obj.found_index = True
                    # if map_page:
                    #     obj.rank = map_page
                    map_websites_list,position_of_website = ListSkipAids(map_websites_list, obj.campaign.website,obj.campaign.business_name if bussiness_text else None )
                    print(map_websites_list,position_of_website)
                    obj.rank = position_of_website
                    obj.result = ','.join(map_websites_list)
                    # obj.pages = ','.join(visit_pages_on_web)
                    # if laptop == 1:
                    #     obj.active_device = 0
                    # if tablet == 1:
                    #     obj.active_device = 1
                    # if phone == 1:
                    #     obj.active_device = 2
                    obj.direction = direction_found
                    # if direction_found:
                    #     obj.direction_URL = direction_list
                    #     # obj.direction_URL = ','.join(direction_list)
                    obj.knowledge_panel = knowledge_panel_found
                    obj.status = True
                    obj.save()
                    # print(direction_list)
                    logger.debug(f'operation ended')
                    return JsonResponse({"status": "true"}, status=status.HTTP_202_ACCEPTED)
                else:
                    # found_website_in_map,found_in_mappack,direction_found,search_device_type,knowledge_panel_found,direction_list
                    # found_website_in_map, found_in_mappack, direction_found, knowledge_panel_found, direction_list, map_websites_list,map_page = map_search_direction_web(
                    #     obj.Keywords.keyword, obj.campaign.website, obj.Keywords.country, obj.Keywords.state,
                    #     obj.Keywords.city)
                    found_website_in_map, found_in_mappack, direction_found, knowledge_panel_found, direction_list, map_websites_list,map_page,bussiness_text = map_search_direction_web(
                        obj.Keywords.keyword, obj.campaign.website, obj.Keywords.country, obj.Keywords.state,
                        obj.Keywords.city,obj.campaign.business_name)
                    print(found_website_in_map, found_in_mappack, direction_found, knowledge_panel_found, direction_list, map_websites_list,map_page)
                    if found_website_in_map or found_in_mappack:
                        obj.found_index = True
                    map_websites_list, map_page = ListSkipAids(map_websites_list, obj.campaign.website,obj.campaign.business_name if bussiness_text else None )

                    obj.result = ','.join(map_websites_list)
                    if map_page:
                        obj.rank = map_page
                    # obj.rank = site_found_index
                    # title and url
                    # title = ''
                    # url = ''
                    # for item in visit_pages_on_web:
                    #     if title == '':
                    #         title = title + item[0]
                    #         url = url + item[1]
                    #     else:
                    #         title = title + ',' + item[0]
                    #         url = url + ',' + item[1]
                    # obj.pages = url
                    # obj.titles = title
                    # obj.pages = ','.join(visit_pages_on_web)
                    # if laptop == 1:
                    #     obj.active_device = 0
                    # if tablet == 1:
                    #     obj.active_device = 1
                    # if phone == 1:
                    #     obj.active_device = 2
                    obj.direction = direction_found
                    if direction_found:
                        obj.direction_URL = direction_list
                        # obj.direction_URL = ','.join(direction_list)

                    # print(1+'1')
                    obj.knowledge_panel = knowledge_panel_found
                    obj.status = True
                    obj.save()
                    print(direction_list)
                    logger.debug(f'operation ended')
                    return JsonResponse({"status": "true"}, status=status.HTTP_202_ACCEPTED)
            else:
                if obj.active_device == 2:
                    print("here hit mobile without direction")
                    # found_website_in_map,found_in_mappack,visit_pages_on_web,map_page,direction_found,search_device_type,knowledge_panel_found
                    found_website_in_map, found_in_mappack, visit_pages_on_web, knowledge_panel_found, web_found_status, direction_found, websites_list, position_of_website,bussiness_text = map_search_mobile(
                        obj.Keywords.keyword, obj.campaign.website, obj.Keywords.country, obj.Keywords.state,
                        obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session,
                        obj.campaign.business_name)

                    print("here is data")
                    print(found_website_in_map, found_in_mappack, visit_pages_on_web, knowledge_panel_found, web_found_status, direction_found, websites_list, position_of_website)
                    print('end')
                    
                    if found_website_in_map or found_in_mappack:
                        obj.found_index = True
                    # if map_page:
                    #     obj.rank = map_page
                    print("here bussiness text")
                    print(bussiness_text)
                    print("end")
                    websites_list,position_of_website = ListSkipAids(websites_list, obj.campaign.website,obj.campaign.business_name if bussiness_text else None )
                    print(websites_list,position_of_website)
                    obj.rank = position_of_website
                    obj.result = ','.join(websites_list)
                    # title and url
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
                    # obj.pages = ','.join(visit_pages_on_web)
                    # if laptop == 1:
                    #     obj.active_device = 0
                    # if tablet == 1:
                    #     obj.active_device = 1
                    # if phone == 1:
                    #     obj.active_device = 2
                    obj.direction = direction_found
                    # if direction_found:
                    #     obj.direction_URL = direction_list
                    obj.knowledge_panel = knowledge_panel_found
                    obj.status = True
                    print(1+'1')
                    obj.save()
                    # print(direction_list)
                    logger.debug(f'operation ended')
                    return JsonResponse({"status": "true"}, status=status.HTTP_202_ACCEPTED)
                else:
                    # found_website_in_map,found_in_mappack,visit_pages_on_web,map_page,direction_found,search_device_type,knowledge_panel_found
                    # found_website_in_map, found_in_mappack, visit_pages_on_web, map_page, knowledge_panel_found, direction_found, websites_list = map_search_web(
                    #     obj.Keywords.keyword, obj.campaign.website, obj.Keywords.country, obj.Keywords.state,
                    #     obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session)

                    found_website_in_map, found_in_mappack, visit_pages_on_web, map_page, knowledge_panel_found, direction_found, websites_list,bussiness_text = map_search_web(
                        obj.Keywords.keyword, obj.campaign.website, obj.Keywords.country, obj.Keywords.state,
                        obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session,obj.campaign.business_name)
                    print(found_website_in_map, found_in_mappack, visit_pages_on_web, map_page)
                    print( found_website_in_map, found_in_mappack, visit_pages_on_web, map_page, knowledge_panel_found, direction_found, websites_list)
                    if found_website_in_map or found_in_mappack:
                        obj.found_index = True

                    websites_list,map_page = ListSkipAids(websites_list, obj.campaign.website,obj.campaign.business_name if bussiness_text else None )
                    print("here",'map_page',map_page)
                    if map_page:
                        obj.rank = map_page
                    # obj.rank = site_found_index
                    # title and url
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
                    obj.result = ','.join(websites_list)
                    # obj.pages = ','.join(visit_pages_on_web)
                    # if laptop == 1:
                    #     obj.active_device = 0
                    # if tablet == 1:
                    #     obj.active_device = 1
                    # if phone == 1:
                    #     obj.active_device = 2
                    obj.direction = direction_found
                    # if direction_found:
                    #     obj.direction_URL = direction_list
                    obj.knowledge_panel = knowledge_panel_found
                    obj.status = True
                    print(1+'1')
                    obj.save()
                    # print(direction_list)
                    logger.debug(f'operation ended')
                    return JsonResponse({"status": "true"}, status=status.HTTP_202_ACCEPTED)
        else:
            # keyword,website_link,country,state,city,time_to_visit,page_visit_no,search_device_type
            # site_found_status,site_found_index,all_website_list,visit_pages_on_web_after,knowledge_panel_found,search_device_type
            if obj.active_device == 2:
                site_found_status, site_found_index, all_website_list, visit_pages_on_web, knowledge_panel_found = keyword_search_mobile(
                    obj.Keywords.keyword, obj.campaign.website, obj.Keywords.country, obj.Keywords.state,
                    obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session)
            else:
                site_found_status, site_found_index, all_website_list, visit_pages_on_web, knowledge_panel_found = keyword_search_web(
                    obj.Keywords.keyword, obj.campaign.website, obj.Keywords.country, obj.Keywords.state,
                    obj.Keywords.city, obj.campaign.avg_session_duration, obj.campaign.pages_per_session)

            obj.found_index = site_found_status
            print(site_found_status,site_found_index,all_website_list,visit_pages_on_web)
            #added
            all_website_list,site_found_index = ListSkipAids(all_website_list,obj.campaign.website)
            obj.rank = site_found_index
            obj.result = ','.join(all_website_list)
            # obj.pages = ','.join(visit_pages_on_web)
            # if laptop == 1:
            #     obj.active_device = 0
            # if tablet == 1:
            #     obj.active_device = 1
            # if phone == 1:
            #     obj.active_device = 2
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
            logger.debug(f'operation ended')
            return JsonResponse({"status": "true"}, status=status.HTTP_202_ACCEPTED)
        #     except:
        #         print("finish")
        #         return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return JsonResponse(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@login_required(login_url="/sign-in/")
def getCItyStateCountry(request):
    if request.method == 'POST':
        data = request.POST 
        # try:
        print('operation started')
        if data['flag'] == 'country':
            data = country.objects.all().values()
            return JsonResponse({"status":"true","data":list(data)},status=status.HTTP_202_ACCEPTED)
        elif data['flag'] == 'state':
            data = state.objects.filter(country=country.objects.get(value=data['countryValue'])).values()
            return JsonResponse({"status":"true","data":list(data)},status=status.HTTP_202_ACCEPTED)
        elif data['flag'] == 'city':
            data = city.objects.filter(country=country.objects.get(value=data['countryValue']), state=state.objects.get(value=data['stateValue'])).values()
            return JsonResponse({"status":"true","data":list(data)},status=status.HTTP_202_ACCEPTED)
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return JsonResponse(status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url="/sign-in/")
def get_search_plan(request):
    if request.method == 'POST':
        data = SearchPlan.objects.filter(daily_searches=request.user.searches).values()
        return JsonResponse({"status":"true","data":list(data)},status=status.HTTP_200_OK)

@csrf_exempt
@login_required(login_url="/sign-in/")
def statement_view(request):
    data  = monthlyBillReport.objects.filter(user = User.objects.get(id=request.user.id))
    return render(request,'statement.html',{"data":data})

@csrf_exempt
def term_of_use(request):
    return render(request,'termOfUse.html')



#paypal


def checkout(request):
    # if request.method == 'POST':
    #     form = CheckoutForm(request.POST)
    #     if form.is_valid():
    #         cleaned_data = form.cleaned_data
    #         # cart.clear(request)
    #
    #         request.session['order_id'] = o.id
    #         return redirect('process_payment')
    #
    #
    # else:
    #     form = CheckoutForm()
    return render(request, 'ecommerce_app/checkout.html')





# 
# 
def process_payment(request,planID):
    host = request.get_host()
    planObj = SearchPlan.objects.get(stripe_price_ID=planID)
    # try:
    userObj = User.objects.get(id=request.user.id)

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        # 'amount': '%.2f' % planObj.cost.quantize(
        #     Decimal('.01')),
        
        'amount': float(planObj.cost),
        # 'amount': 134.00,
        'item_name': 'search per day-{}'.format(planObj.daily_searches),
        'invoice': str(planObj.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           '/payment-done/'),
        'cancel_return': 'http://{}{}'.format(host,
                                              '/payment-cancelled/'),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/paypal/process_payment.html', {'order': planObj, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/paypal/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/paypal/payment_cancelled.html')
