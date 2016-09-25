from .views import WebhookView, DenunciasView
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include

router = DefaultRouter()

router.register(r'webhook', WebhookView, base_name='webhook')

router.register(r'denuncias', DenunciasView, base_name='denuncias')

urlpatterns = [
    url(r'^', include(router.urls)),
]