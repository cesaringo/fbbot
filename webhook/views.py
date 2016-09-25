from rest_framework.response import Response
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory
from fbbot import settings
import requests
import json
from .models import Denuncia, File


class WebhookView(viewsets.ViewSet):

    def list(self, request, format=None):
        challenge = request.GET.get('hub.challenge')
        if request.GET.get("hub.mode") and request.GET.get("hub.mode") == "subscribe" and (
                    request.GET.get("hub.verify_token") == "holamundo"):
                return HttpResponse(challenge)
        return Response('Error, invalid token. Update 1')

    def post(self, request, format=None):
        """WebHook Root"""
        data = request.data
        self.validate_request(data)
        entry = data.get('entry', [])
        for item in entry:
            for messaging_item in item["messaging"]:
                self.handle_request_field(messaging_item)

        # We return a HTTP 200
        return HttpResponse(status=200)

    def validate_request(self, data):
        """
        verify the signature of the request to validate the integrity and origin of the payload
        """
        pass

    def handle_request_field(self, messaging_item):
        if messaging_item.get('message'):
            message = self.init_message(messaging_item.get('sender')["id"])
            # Buscao si existe una denuncia activa para ese usuario
            try:
                denuncia = Denuncia.objects.get(fb_user_id=messaging_item.get('sender')["id"])

            except Denuncia.DoesNotExist:
                denuncia = None
                # Todo Hacer algo cuanod no hay denuncia activa y nos mandan un mensaje

            if denuncia is not None and denuncia.current_step == 1:
                denuncia.nombre_funcionario = messaging_item.get("message")["text"]
                denuncia.current_step += 1
                denuncia.save()
                return self.send_message_denuncia_step2(message)

            if denuncia is not None and denuncia.current_step == 2:
                denuncia.descripcion = messaging_item.get("message")["text"]
                denuncia.current_step += 1
                denuncia.save()
                return self.send_message_denuncia_step3(message)

            if denuncia is not None and denuncia.current_step == 3:
                denuncia.fecha_suceso = messaging_item.get("message")["text"]
                denuncia.current_step += 1
                denuncia.save()
                return self.send_message_denuncia_step4(message)

            if denuncia is not None and denuncia.current_step == 4:
                denuncia.lugar = messaging_item.get("message")["text"]
                denuncia.current_step += 1
                denuncia.save()
                return self.send_message_denuncia_step5(message)

            if denuncia is not None and denuncia.current_step == 5:
                pass

            self.typing_off(message.params["recipient"]["id"])
            return 0

        elif messaging_item.get('postback'):
            message = self.init_message(messaging_item.get('sender')["id"])

            # We need to read what button was tapped
            payload = json.loads(messaging_item["postback"]["payload"])
            if payload["menu_item"] == 'start_button':
                message.params["message"] = {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "button",
                            "text": "¡Hola!. Soy tu asistente virtual que te ayudará a realizar una de las siguientes opciones:",
                            "buttons": [
                                {
                                    "type": "postback",
                                    "title": "Denuncia",
                                    "payload": "{\"menu_item\": \"denuncia\"}"
                                },

                                {
                                    "type": "postback",
                                    "title": "Asistencia",
                                    "payload": "{\"menu_item\": \"asistencia\"}"
                                }
                            ]
                        }
                    }
                }
                message.send()

            elif payload["menu_item"] == 'denuncia':
                    denuncia = Denuncia(fb_user_id=messaging_item.get('sender')["id"], current_step=1)
                    denuncia.save()
                    return self.send_message_denuncia_step1(message)

            elif payload["menu_item"] == 'asistencia':
                message.params["message"] = {
                    "text": "Por favor escribe un tema sobre el que deseas sabes: Tránsito, asistencia legal, etc."
                }
                message.send()
                self.typing_off(message.params["recipient"]["id"])

        elif messaging_item.get('messaging_optins'):
            pass

        elif messaging_item.get('message_deliveries'):
            pass

        elif messaging_item.get('message_reads'):
            pass

        elif messaging_item.get('message_echoes'):
            pass

    @staticmethod
    def typing_on(recipient):
        typing_signal = SendAPI()
        typing_signal.params = {
            "recipient": {
                "id": recipient
            },
            "sender_action": "typing_on"
        }
        typing_signal.send()

    @staticmethod
    def typing_off(recipient):
        typing_signal = SendAPI()
        typing_signal.params = {
            "recipient": {
                "id": recipient
            },
            "sender_action": "typing_off"
        }
        typing_signal.send()

    def send_message_denuncia_step1(self, message):
        message.params["message"] = {
            "text": "Por favor comienza escribiendo el nombre del funcionario "
                    "o institución que deseas denunciar:"
        }
        message.send()
        self.typing_off(message.params["recipient"]["id"])

    def send_message_denuncia_step2(self, message):
        message.params["message"] = {
            "text": "Escribe el motivo de la denuncia:"
        }
        status = message.send()
        self.typing_off(message.params["recipient"]["id"])
        return status


    def send_message_denuncia_step3(self, message):
        message.params["message"] = {
            "text": "Fecha en que se presentó el acontecimiento:"
        }
        status = message.send()
        self.typing_off(message.params["recipient"]["id"])
        return status

    def send_message_denuncia_step4(self, message):
        message.params["message"] = {
            "text": "¿Dónde sucedió?"
        }
        status = message.send()
        self.typing_off(message.params["recipient"]["id"])
        return status

    def send_message_denuncia_step5(self, message):
        message.params["message"] = {
            "text": "Adjunta los documentos que prueben tu denuncía. Toma en cuenta que denuncias sin pruebas verídicas"
                    "no tendrán efecto."
        }
        status = message.send()
        self.typing_off(message.params["recipient"]["id"])
        return status

    def send_message_denuncia_step6(self, message):
        message.params["message"] = {
            "text": "Gracías por contribuir a un país mejor."
        }
        status = message.send()
        self.typing_off(message.params["recipient"]["id"])
        return status

    def init_message(self, recipient):
        self.typing_on(recipient)
        message = SendAPI()
        message.params = {
            "recipient": {
                "id": recipient
            }
        }
        return message


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
                    {"payload": "{\"menu_item\": \"start_button\"}"}
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
                "text": "Hola {{user_first_name}}, bienvenido al sistema de denuncia ciudadana y consulta de información."
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
                        "title": "Denuncia",
                        "payload": "{\"menu_item\": \"denuncia\"}"
                    },

                    {
                        "type": "postback",
                        "title": "Asistencia",
                        "payload": "{\"menu_item\": \"asistencia\"}"
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



