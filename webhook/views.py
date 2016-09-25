from rest_framework.response import Response
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory
from fbbot import settings
import requests
import json


class WebhookView(viewsets.ViewSet):

    def list(self, request, format=None):
        challenge = request.GET.get('hub.challenge')
        if request.GET.get("hub.mode") and request.GET.get("hub.mode") == "subscribe" and (
                    request.GET.get("hub.verify_token") == "holamundo"):
                return HttpResponse(challenge)
        return Response('Error, invalid token2')

    def post(self, request, format=None):
        """WebHook Root"""
        data = request.data
        self.validate_request(data)
        self.handle_request_field(data)

        # We return a HTTP 200
        return HttpResponse(status=200)

    def validate_request(self, data):
        """
        verify the signature of the request to validate the integrity and origin of the payload
        """
        pass

    def handle_request_field(self, data):
        if data.get('message'):
            """We sent a hello back message"""
            message = SendAPI()
            message.params = {
                "recipient": {
                    "id": data.get('sender')
                },
                "message": {
                    "text": "hello, world!"
                }
            }
            message.send()

        elif data.get('messaging_postbacks'):
            pass

        elif data.get('messaging_optins'):
            pass

        elif data.get('message_deliveries'):
            pass

        elif data.get('message_reads'):
            pass

        elif data.get('message_echoes'):
            pass




class ThreadSettings:
    url = 'https://graph.facebook.com/v2.6/me/thread_settings'
    default_params = {}
    params = {}

    def __init__(self, params=None):
        self.url = self.url + '?access_token=' + settings.PAGE_ACCESS_TOKEN
        if params is None:
            self.params = self.default_params

    def send(self, method='post'):
        if method is 'post':
            response = requests.post(self.url, json=self.params)

        elif method is 'delete':
            response = requests.delete(self.url, json=self.params)

        return response.status_code

    def set_started_button(self):
        self.params = {
            "setting_type": "call_to_actions",
            "thread_state": "new_thread",
            "call_to_actions":
                [
                    {"payload": "USER_DEFINED_PAYLOAD"}
                ]
        }
        return self.send()

    def delete_started_button(self):
        self.params = {
            "setting_type": "call_to_actions",
            "thread_state": "new_thread"
        }
        return self.send(method='delete')

    def set_greeting_text(self):
        self.params = {
            "setting_type": "greeting",
            "greeting": {
                "text": "Hi {{user_first_name}}, welcome to this bot."
            }
        }
        return self.send()

    def set_persistent_menu(self, params=None):
        if params is None:
            self.params = {
                "setting_type": "call_to_actions",
                "thread_state": "existing_thread",
                "call_to_actions": [
                    {
                        "type": "postback",
                        "title": "Help",
                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_HELP"
                    },

                    {
                        "type": "web_url",
                        "title": "View Website",
                        "url": "http://google.com/"
                    }
                ]
            }

        return self.send()

    def delete_persistent_menu(self):
        self.params = {
            "setting_type": "call_to_actions",
            "thread_state": "existing_thread"
        }
        self.send(method='delete')


class SendAPI:
    url = 'https://graph.facebook.com/v2.6/me/messages'
    recipient = None
    params = None

    def __init__(self):
        self.url = self.url + '?access_token=' + settings.PAGE_ACCESS_TOKEN

    def send(self):
        response = requests.post(self.url, json=self.params)
        return response.status_code

    def set_params(self, params_name, params_value):
        self.params[params_name] = params_value



class MessageReceivedCallback:
    """
    This callback will occur when a message has been sent to your page.
    You may receive text messages or messages with attachments (image, audio, video, file or location).
    """

    pass




