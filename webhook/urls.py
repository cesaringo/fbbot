from .views import WebhookView
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include

router = DefaultRouter()

router.register(r'webhook', WebhookView, base_name='webhook')

urlpatterns = [
    url(r'^', include(router.urls)),
]