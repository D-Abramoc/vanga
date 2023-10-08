from django.test import TestCase, Client
from http.client import METHOD_NOT_ALLOWED, BAD_REQUEST


class ForecastURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_api_v1_ready_response(self):
        """Проверка ответа api/v1/ready при неверном запросе"""
        get_response = self.guest_client.get('/api/v1/ready')
        bad_post_response = self.guest_client.post(
            '/api/v1/ready',
            data={'status': 'not_ready'}
        )
        self.assertEqual(get_response.status_code, METHOD_NOT_ALLOWED)
        self.assertEqual(bad_post_response.status_code, BAD_REQUEST)
