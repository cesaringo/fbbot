from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


class WebhookView(viewsets.ViewSet):

    def list(self, request, format=None):
        if request.GET.get("hub.mode") and request.GET.get("hub.mode") == "subscribe" and (
                    request.GET.get("hub.verify_token") == "holamundo"):
                return Response(request.GET.get("hub.challenge").replace("\"", ""))
        return Response('Error, invalid token')