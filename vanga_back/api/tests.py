from http import HTTPStatus
from rest_framework.test import APIClient, APITestCase
from users.models import User


class ApiTest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user(self):
        '''Регистрация пользователя'''
        number_users = User.objects.count()
        data = {
            'email': 'gector_barbossa@black.perl',
            'password': 'pass_word'
        }
        # Регистрация нового пользователя
        response = self.client.post('/api/auth/users/', data)
        self.assertEqual(User.objects.count(), number_users + 1)
        # Дублирование пользователя
        response = self.client.post('/api/auth/users/', data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
