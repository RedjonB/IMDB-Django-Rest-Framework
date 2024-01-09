from django.contrib.auth.models import User
from rest_framework import status

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class RegisterTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('account:register')

    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@gmial.com',
            'password': '12345678',
            'password2': '12345678',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example', password='12345678')

    def test_login(self):
        url = reverse('account:login')
        data = {
            'username': 'example',
            'password': '12345678',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('account:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
