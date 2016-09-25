from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets


class WebhookView(viewsets.ViewSet):

    def list(self, request, format=None):
        challenge = request.data.get('hub_challenge', 'hub_challenge')
        verify_token = request.data.get('hub_verify_token', 'hub_verify_token')

        if verify_token == 'holamundo':
            return Response(challenge)

        return Response('holamundo')
