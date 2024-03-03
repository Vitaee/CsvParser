from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from core.models import User
import json

class TestUserRegistrationLoginView(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        self.user = User.objects.create_user(username='testuser1', password='testpassword1')


    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login(self):
        # Register user
        self.client.post(self.register_url, self.user_data, format='json')
        

        # Login user
        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', json.loads(response.content))

class TestUserView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_view_url = reverse('current_user')

    def test_user_view_authenticated(self):
        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.user_view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestCSVUser(APITestCase):
    def setUp(self):
        self.user_filter_url = reverse('user_filter')
        data = [
            User(username="1", first_name="Dániel", last_name="Dibiasi", address="Yrttimaanpolku 2, 06892 Geta" ),
            User(username="2",first_name="Beriye", last_name="Ülker", address="Dunckerinbulevardi 1, 01547 Lapua" ),      
            User(username="3", first_name="Etta", last_name="Sárközi", address="Usvatie 52, 58886 Punkalaidun" ),  
        ]

        self.users = User.objects.bulk_create(data)

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.user_data = {
            'first_name': 'Dániel',
            'last_name': 'Dibiasi',
            'address': 'Yrttimaanpolku 2, 06892 Geta'
        }

    def test_user_filter(self):
        # Login user
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Filter users
        response = self.client.get(self.user_filter_url, {'q': 'Dániel'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['fields']['first_name'], self.user_data['first_name'])
        self.assertEqual(data[0]['fields']['last_name'], self.user_data['last_name'])
        self.assertEqual(data[0]['fields']['address'], self.user_data['address'])

        # Filter with non-existent search term
        response = self.client.get(self.user_filter_url, {'q': 'NonExistent'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)