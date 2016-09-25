from rest_framework import status
from rest_framework.test import APITestCase
from .views import ThreadSettings
import requests
from fbbot import settings


class FBPlatformTests(APITestCase):
    def test_set_greeting_text(self):
        thread_settings = ThreadSettings()
        response = thread_settings.set_greeting_text()
        self.assertEqual('200', response)

    def test_set_started_button(self):
        thread_settings = ThreadSettings()
        response = thread_settings.set_started_button()
        self.assertEqual('200', response)

    def test_set_persistent_menu(self):
        thread_settings = ThreadSettings()
        response = thread_settings.set_persistent_menu()
        self.assertEqual('200', response)

    def test_handle_message(self):
        fake_data = {
            "object": "page",
            "entry": [
                {
                    "id": "PAGE_ID",
                    "time": 1458692752478,
                    "messaging": [
                        {
                            "sender": {
                                "id": "100000500686974"
                            },

                            "recipient": {
                                "id": "PAGE_ID"
                            },

                            "message": {
                                "mid": "mid.1457764197618:41d102a3e1ae206a38",
                                "seq": 73,
                                "text": "hello, world!",
                                "quick_reply": {
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                }
                            }
                        }
                    ]
                }
            ]
        }

        response = requests.post(settings.TEST_WEB_HOOK_URL, json=fake_data)
        self.assertEqual('200', response.status_code)










