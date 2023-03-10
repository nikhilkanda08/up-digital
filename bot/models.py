from email.policy import default
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, date, timedelta

from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver

import math
import radar
import random
from django.db.models import Sum, Q, F

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):

        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    # WARNING!
    """
    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    username = models.CharField(
        _('username'),
        blank=True,
        null=True,
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    searches = models.IntegerField(blank=False, null=False, default=0, verbose_name='Allowed Searches')
    searches_status = models.BooleanField(blank=False, null=False, default=False, verbose_name='Searches Status')
    OTP = models.IntegerField(blank=True, null=True, verbose_name='Reset Password OTP')
    strip_client_ID = models.CharField(_("Stripe Client ID"), default="", blank=True, null=True, max_length=255)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return '{}'.format(self.email)
    
    @property
    def userCampaign(self):
        return Campaign.objects.filter(user = User.objects.get(id=self.id))


class Campaign(models.Model):

    SEARCH_TYPES = (
        ('organic_search', 'Organic Search'),
        ('googlemap', 'Google Maps'),
    )

    is_active = models.BooleanField(blank=False, null=False, default=True, verbose_name='Is Active')
    title = models.CharField(max_length=256, verbose_name='Campaign Title')
    description = models.TextField(blank=True, null=True, verbose_name='Campaign Description')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_related_name')
    search_type = models.CharField(choices=SEARCH_TYPES, default=SEARCH_TYPES[0][0], blank=False, null=False, max_length=100, verbose_name='Search Type')
    website = models.CharField(max_length=256, verbose_name='Website Name')
    mobile_Searches = models.IntegerField(default=30, validators=[MaxValueValidator(100), MinValueValidator(0)], verbose_name='Mobile Searches')
    bounce_rate = models.IntegerField(default=50, validators=[MaxValueValidator(100), MinValueValidator(0)], verbose_name='Bounce Rate')
    pages_per_session = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)], verbose_name='Pages Per Session')
    avg_session_duration = models.IntegerField(default=70, validators=[MaxValueValidator(300), MinValueValidator(70)], verbose_name='Average Session Duration')
    business_name = models.CharField(default="", blank=True, null=True, max_length=250, verbose_name='Business Name')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Keywords(models.Model):

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_related_name')

    city = models.CharField(max_length=256, blank=True, verbose_name='City')
    state = models.CharField(max_length=256, blank=True, verbose_name='State')
    country = models.CharField(max_length=256, blank=True, null=True, verbose_name='Country')

    keyword = models.CharField(max_length=256, blank=False, null=False, verbose_name='Keyword')
    searches_per_day = models.DecimalField(blank=False, null=False, max_digits=5, default=0.0, verbose_name='Pages Per Session', decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keyword
    
    @property
    def getDeviceType(self):
        try:
            campObj = Campaign.objects.get(id=self.campaign.id)
            records = SearchResult.objects.filter(Q(campaign = campObj) & Q(Keywords = self))
            recordsCount = records.count()
            mobRecordsCount = records.filter(active_device = 2).count()
            if ((mobRecordsCount/recordsCount)* 100) >= campObj.mobile_Searches:
                return random.randint(0,1)
            else:
                return 2
        except:
            if campObj.mobile_Searches > 0:
                return 2
            return random.randint(0,1)

class SearchResult(models.Model):

    DEVICE_TYPES = (
        (0, 'Tablet'),
        (1, 'Laptop'),
        (2, 'Mobile Phones'),
    )

    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_name')
    Keywords = models.ForeignKey(Keywords, on_delete=models.CASCADE, related_name='Keywords_name')
    map_campaign_direction = models.BooleanField(default=False, blank=False, null=False, verbose_name='Map Campaigns with Directions')

    website_title = models.CharField(max_length=256, blank=True, null=True, verbose_name='Website Title')
    rank = models.IntegerField(blank=True, null=True, verbose_name='Website Rank in Search')
    found_index = models.BooleanField(blank=False, null=False, default=False, verbose_name='Website Found Index')
    result = models.TextField(blank=True, null=True, verbose_name='Search Results')
    titles = models.TextField(blank=True, null=True, verbose_name='Search Results Titles')
    pages = models.TextField(blank=True, null=True, verbose_name='Search Pages')

    direction = models.BooleanField(blank=False, null=False, default=False, verbose_name='Website Directions')
    direction_URL = models.TextField(blank=True, null=True, verbose_name='Direction URL')
    knowledge_panel = models.BooleanField(blank=False, null=False, default=False, verbose_name='Knowledge Panel')

    active_device = models.IntegerField(choices=DEVICE_TYPES, blank=True, null=True, verbose_name='Active Device')
    time_on_site = models.IntegerField(default=0, verbose_name='Time on Site')

    status = models.BooleanField(blank=False, null=False, default=False, verbose_name='Search Result Status')
    Schedule = models.DateTimeField(default=None, blank=True, null=True, verbose_name='Search Result schedule')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.website_title

class SearchPlan(models.Model):

    planID = models.IntegerField(blank=True, null=True,verbose_name='Plan ID')
    cost = models.IntegerField(verbose_name='Cost')
    total_pages = models.IntegerField(verbose_name='Number of Pages')
    onsite_time = models.IntegerField(verbose_name='Time on Site')
    daily_searches = models.IntegerField(blank=True, null=True,verbose_name='Number of searches per day')
    searche_cost = models.FloatField(blank=True, null=True,verbose_name='Cost per search')
    stripe_price_ID = models.CharField(blank=True, null=True,max_length=800,verbose_name='Stripe Price ID')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cost)

class country(models.Model):

    name = models.CharField(max_length=800)
    value = models.CharField(max_length=800)

    def __str__(self):
        return str(self.name)

class state(models.Model):

    country = models.ForeignKey(country, on_delete=models.CASCADE, related_name='stateCountryID')
    name = models.CharField(max_length=800)
    value = models.CharField(max_length=800)

    def __str__(self):
        return str(self.name)

class city(models.Model):

    country = models.ForeignKey(country, on_delete=models.CASCADE, related_name='cityCountryID')
    state = models.ForeignKey(state, on_delete=models.CASCADE, related_name='stateID')
    name = models.CharField(max_length=800)
    value = models.CharField(max_length=800)

    def __str__(self):
        return str(self.name)

class Subscription(models.Model):
    PAY_SOURCE_TYPES = (
        ('stripe', 'Stripe'),
        ('paypal', 'Paypal'),
        ('crypto_currency', 'Crypto Currency'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription_user')
    paid = models.BooleanField(default="False")
    amount = models.IntegerField(default=0)
    source = models.CharField(choices=PAY_SOURCE_TYPES, default=PAY_SOURCE_TYPES[0][0], blank=False, null=False, max_length=100, verbose_name='Paying Source')
    subscriptionID = models.CharField(default=None, max_length=800)
    subscriptionNumber = models.CharField(blank=True, null=True,max_length=800)
    clientID = models.CharField(blank=True, null=True,max_length=800)
    description = models.CharField(default=None,null=True,blank=True,max_length=800)

    def __str__(self):
        return self.source

class monthlyBillReport(models.Model):

    user = models.ForeignKey(User, default=None , on_delete=models.CASCADE, related_name='user_monthly_sheet')
    
    body_ID = models.CharField(blank=True, null=True, max_length=800)
    body_created = models.DateTimeField(blank=True, null=True)
    account_name = models.CharField(blank=True, null=True, max_length=800)
    object_charge = models.CharField(blank=True, null=True, max_length=800)
    charge = models.CharField(blank=True, null=True, max_length=800)
    obj_created = models.DateTimeField(blank=True, null=True)
    currency = models.CharField(blank=True, null=True, max_length=800)
    customer = models.CharField(blank=True, null=True, max_length=800)
    hosted_invoice_url = models.CharField(blank=True, null=True, max_length=800)
    invoice_pdf = models.CharField(blank=True, null=True, max_length=800)
    total = models.FloatField(blank=True, null=True, default=0)
    invoice_number = models.CharField(blank=True, null=True, max_length=800) # invoice number
    payment_intent = models.CharField(blank=True, null=True, max_length=800)
    paid = models.BooleanField(default=False)
    status = models.CharField(blank=True, null=True, max_length=800)
    period_end = models.DateTimeField(blank=True, null=True)
    period_start = models.DateTimeField(blank=True, null=True)
    request_id = models.CharField(blank=True, null=True, max_length=800)
    request_idempotency_key = models.CharField(blank=True, null=True, max_length=800)

    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.body_ID)

@receiver(post_save, sender=Keywords)
def create_search_result_record(sender, instance, created, **kwargs):
    today = datetime.today()
    print(instance.searches_per_day)
    searchNumber = math.modf(float(instance.searches_per_day))
    print(round(searchNumber[0], 2))
    print(searchNumber[1])
    searchNumberInteger = searchNumber[1]
    searchNumberDecimal = round(searchNumber[0], 2)
    perDaysSearches = searchNumberInteger
    days = 1
    if instance.campaign.search_type == 'organic_search':
        # add search results records for integer value
        if searchNumberInteger > 0:
            IntegerResults = SearchResult.objects.filter(Q(campaign = instance.campaign) & Q(Keywords = instance) & Q(Schedule__date = today.date()))
            print(IntegerResults)
            if len(IntegerResults) < searchNumberInteger:
                for x in range(int(searchNumberInteger) - len(IntegerResults)):
                    print(x) 
                    # Generate random datetime from datetime.datetime values
                    startDate = today
                    endDate = (today).replace(hour=23, minute=59, second=59)
                    print(startDate)
                    print(endDate)
                    random_date_time = radar.random_datetime(
                        start = startDate,
                        stop = endDate
                    )
                    print()
                    print(random_date_time)
                    obj_status = SearchResult.objects.create(campaign = instance.campaign, Keywords = instance, website_title = instance.campaign.title, Schedule = random_date_time,active_device = instance.getDeviceType)

                    print(obj_status)


        if searchNumberDecimal > 0:
            daysForDecimal = math.ceil((1/searchNumberDecimal)*100)/100
            perDaysSearches = math.floor((perDaysSearches * daysForDecimal) + 1)
            days = math.ceil(daysForDecimal)
            print("------",daysForDecimal)
            print(perDaysSearches)
            print(days)
            startDate = today
            endDate = (today+ timedelta(days=1+days)).replace(hour=23, minute=59, second=59)
            print(startDate)
            print(endDate)
            random_date_time = radar.random_datetime(
                start = startDate,
                stop = endDate
            )
            print()
            print(random_date_time)
            obj_status = SearchResult.objects.create(campaign = instance.campaign, Keywords = instance, website_title = instance.campaign.title, Schedule = random_date_time,active_device = instance.getDeviceType)
            print(obj_status)
    else:
        # add search results records for integer value
        mapDirectionStatus = False
        if searchNumberInteger > 0:
            IntegerResults = SearchResult.objects.filter(Q(campaign = instance.campaign) & Q(Keywords = instance) & Q(Schedule__date = today.date()))
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
                    startDate = today
                    endDate = (today).replace(hour=23, minute=59, second=59)
                    print(startDate)
                    print(endDate)
                    random_date_time = radar.random_datetime(
                        start = startDate,
                        stop = endDate
                    )
                    print()
                    print(random_date_time)
                    obj_status = SearchResult.objects.create(campaign = instance.campaign, Keywords = instance, website_title = instance.campaign.title, Schedule = random_date_time,active_device = instance.getDeviceType,map_campaign_direction = mapDirectionStatus)
                    mapDirectionStatus = not mapDirectionStatus
                    print(obj_status)


        if searchNumberDecimal > 0:
            
            IntegerResults = SearchResult.objects.filter(Q(campaign = instance.campaign) & Q(Keywords = instance) & Q(Schedule__date = today.date()))
            # logic for map driection start
            IntegerResultsMapCount = IntegerResults.filter(map_campaign_direction = False).count()
            IntegerResultsMapDirectionCount = IntegerResults.filter(map_campaign_direction = True).count()
            if IntegerResultsMapCount > IntegerResultsMapDirectionCount:
                mapDirectionStatus = True
            # logic for map driection end

            daysForDecimal = math.ceil((1/searchNumberDecimal)*100)/100
            perDaysSearches = math.floor((perDaysSearches * daysForDecimal) + 1)
            days = math.ceil(daysForDecimal)
            print("------",daysForDecimal)
            print(perDaysSearches)
            print(days)
            startDate = today
            endDate = (today+ timedelta(days=1+days)).replace(hour=23, minute=59, second=59)
            print(startDate)
            print(endDate)
            random_date_time = radar.random_datetime(
                start = startDate,
                stop = endDate
            )
            # print()
            print(random_date_time)
            obj_status = SearchResult.objects.create(campaign = instance.campaign, Keywords = instance, website_title = instance.campaign.title, Schedule = random_date_time,active_device = instance.getDeviceType,map_campaign_direction = mapDirectionStatus)
            print(obj_status)