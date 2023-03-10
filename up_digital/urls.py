"""up_digital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
# from django.conf.urls import url, include
from django.conf.urls import  include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # url('', include('bot.urls')),
    path('', include('bot.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),

]


admin.site.site_header = 'UP DIGITAL'                    # default: "Django Administration"
admin.site.index_title = 'UP DIGITAL'                    # default: "Site administration"
admin.site.site_title = 'UP DIGITAL'                     # default: "Django site admin"

# urlpatterns = [url(r'^backend/', include(urlpatterns))]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)