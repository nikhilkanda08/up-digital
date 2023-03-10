from .forms import *
from .models import *
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import monthlyBillReport
# Register your models here.

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_form_template = 'admin_templates/user_change_form.html'
    list_display = ['searches_status','email',]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'searches', 'searches_status','OTP', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js',
            '/static/js/UserAdmin.js',
        )
        css = {
            'all': ('/static/css/adminStyle.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css')
        }

admin.site.register(User, UserAdmin)

class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'search_type', 'website',]
    class Meta:
        model = Campaign

admin.site.register(Campaign, CampaignAdmin)

class KeywordsAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'country', 'keyword',]
    class Meta:
        model = Keywords

admin.site.register(Keywords, KeywordsAdmin)

class SearchResultAdmin(admin.ModelAdmin):
    list_display = ['website_title', 'rank', 'campaign',]
    class Meta:
        model = SearchResult

admin.site.register(SearchResult, SearchResultAdmin)

class SearchPlanAdmin(admin.ModelAdmin):
    list_display = ['cost', 'total_pages', 'onsite_time',]
    class Meta:
        model = SearchPlan

admin.site.register(SearchPlan, SearchPlanAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'clientID', 'subscriptionID', 'subscriptionNumber',]
    class Meta:
        model = Subscription

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(monthlyBillReport)