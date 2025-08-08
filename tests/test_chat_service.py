# File: openrouter-streamlit-chat/tests/test_chat_service.py

import unittest
from src.services.chat_service import ChatService
from src.api.openrouter_client import OpenRouterClient

class TestChatService(unittest.TestCase):
    def setUp(self):
        self.client = OpenRouterClient(api_key='test_api_key')
        self.chat_service = ChatService(self.client)

    def test_send_message(self):
        response = self.chat_service.send_message("Hello, how are you?")
        self.assertIsNotNone(response)
        self.assertIn('response', response)

    def test_receive_message(self):
        self.chat_service.send_message("Hello!")
        message = self.chat_service.receive_message()
        self.assertIsNotNone(message)
        self.assertEqual(message.sender, 'user')

    def test_chat_service_integration(self):
        self.chat_service.send_message("What's the weather like?")
        response = self.chat_service.receive_message()
        self.assertIn('weather', response.content.lower())

if __name__ == '__main__':
    unittest.main()

