from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.http import HttpResponse


class WebhookView(viewsets.ViewSet):

    def list(self, request, format=None):
        challenge = request.GET.get('hub.challenge')
        if request.GET.get("hub.mode") and request.GET.get("hub.mode") == "subscribe" and (
                    request.GET.get("hub.verify_token") == "holamundo"):
                return HttpResponse(challenge)
        return Response('Error, invalid token2')