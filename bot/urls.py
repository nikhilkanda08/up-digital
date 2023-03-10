
from django.urls import path
from .views import *

app_name = 'bot'
urlpatterns = [
        # path('test/', test, name='test'),
        # general
        path('', dashboard, name='dashboard'),
        path('landingPage/', landingPage, name='landingPage'),
        path('custom-Price/', pricing, name='pricing'),
        path('recent-searches/', recent_searches,name='recent_searches'),
        path('get-country/', getCItyStateCountry,name='getCItyStateCountry'),
        path('get-state/', getCItyStateCountry,name='getCItyStateCountry'),
        path('get-city/', getCItyStateCountry,name='getCItyStateCountry'),
        
        # overlay     user account creation
        path('sign-in/', sign_in, name='sign_in'),
        path('sign-up/', sign_up, name='sign_up'),
        # path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
        # path('rest-auth/google/', GoogleLogin.as_view(), name='google_login')
        path('create-account/', create_account, name='create_account'),
        path('login/', user_login, name='user_login'),
        path('sign-out/', user_logout, name='user_logout'),
        # password
        path('admin-reset-password/', admin_reset_password, name='admin_reset_password'),
        path('change-password/', change_password, name='change_password'),
        path('reset-password/', reset_pwd, name='reset_pwd'),
        path('reset-pwd-OTP/', reset_pwd_OTP, name='reset_pwd_OTP'),
        path('two-steps/<str:email>/', OTP_page, name='OTP_page'),
        path('validate-OTP/', validate_OTP, name='validate_OTP'),
        path('new-password/', new_pwd, name='new_pwd'),
        
        # campaign_apis
        path('campaign/', campaign_apis, name='campaign_apis'),
        path('update-campaign/', campaign_update, name='campaign_update'),
        path('campaign-detail/<int:pk>/', campaign_detail, name='campaign_detail'),
        path('campaign-keywords/<int:pk>/', campaign_detail_keywords, name='campaign_detail_keywords'),
        path('campaign-searches/<int:pk>/', campaign_detail_searches, name='campaign_detail_searches'),
        path('campaign-schedule-searches/<int:pk>/', campaign_detail_schedule_searches, name='campaign_detail_schedule_searches'),
        path('campaign-activity/<int:pk>/', campaign_detail_activity, name='campaign_detail_activity'),
        path('campaign-setting/<int:pk>/', campaign_detail_setting, name='campaign_detail_setting'),
        # keyword
        path('keyword/', keyword_apis, name='keyword_apis'),
        path('keyword-detail/<int:pk>/', keyword_detail, name='keyword_detail'),
        # path('campaign-detail/<int:pk>/', campaign_detail, name='campaign_detail'),
        # search_results
        path('search-results/<int:pk>/', search_results, name='search_results'),
        path('result-detail/<int:pk>/', search_result_detail, name='search_result_detail'),

        # strip
        path('stripe/<str:planID>/', stripe_view, name='stripe'),
        path('create-checkout-session/', create_checkout_session, name='checkout'),
        path('success.html/', success,name='success'),
        path('cancel.html/', cancel,name='cancel'),
        path('cancel-subscription/', cancelStripeSubscription,name='cancelStripeSubscription'),
        # strip webhooks
        path('webhook/payment-succeeded/', webhook_invoice_payment_scceeded,name='webhook_invoice_payment_scceeded'),

        # paypal
        path('paypal_view/', paypal_view,name='paypal_view'),
        path('run-bot/', run_bot,name='run_bot'),

        # pricing
        path('get-search-plan/', get_search_plan,name='get_search_plan'),

        # statement
        path('monthly-statement/', statement_view,name='statement_view'),
        # term_of_use
        path('terms-of-use/', term_of_use,name='term_of_use'),
        #paypal new
        path('checkout/', checkout, name='checkout'),
        path('process-payment/<str:planID>/', process_payment, name='process_payment'),
        # path('process-payment/', process_payment, name='process_payment'),
        path('payment-done/', payment_done, name='payment_done'),
        path('payment-cancelled/', payment_canceled, name='payment_cancelled'),

        
    ]