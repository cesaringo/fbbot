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
            "sender": {
                "id": "cesaringo90"
            },
            "recipient": {
                "id": "190897027755358"
            },
            "timestamp": 1458692752478,
            "message": {
                "mid": "mid.1457764197618:41d102a3e1ae206a38",
                "seq": 73,
                "text": "hello, world!",
                "quick_reply": {
                  "payload": "DEVELOPER_DEFINED_PAYLOAD"
                }
            }
        }
        response = requests.post(settings.TEST_WEB_HOOK_URL, json=fake_data)
        self.assertEqual('200', response.status_code)










