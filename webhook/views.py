from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


class WebhookView(viewsets.ViewSet):

    def list(self, request, format=None):
        challenge = request.GET.get("hub.challenge").replace('"', '')
        if request.GET.get("hub.mode") and request.GET.get("hub.mode") == "subscribe" and (
                    request.GET.get("hub.verify_token") == "holamundo"):
                return Response(challenge)
        return Response('Error, invalid token2')