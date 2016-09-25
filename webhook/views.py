from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


class WebhookView(viewsets.ViewSet):

    def list(self, request, format=None):
        return Response("holamundo")