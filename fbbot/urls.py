from django.contrib import admin
from django.conf.urls import patterns, include, url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('webhook.urls')),
]
