#* Models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTestCase(APITestCase):

    def setUp(self) -> None:
        '''
        THis method is called before the invocation or each test method.
        '''
        return super().setUp()
    
    def test_create_account(self):
        '''
        Testing registration process
        '''
        url = reverse('register')
        correct_data = {
            "email": "test1@mail.com",
            "username": "test1",
            "password": "test1",
            "password2": "test1",
        }

        response = self.client.post(url, correct_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'create account')
        # response = self.client.post(url, incorrect_data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_account_error(self):
    #     '''
    #     Create account error test
    #     '''
    #     url = reverse('register')
    #     incorrect_data = {
    #         "email": "test1@mail.com",
    #         # "username": "test1",
    #         "password": "test1",
    #         "password2": "test1",
    #     }
        
    #     response = self.client.post(url, incorrect_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'create account error')

    def tearDown(self) -> None:
        '''
        This method is called after all the test methods.
        '''
        return super().tearDown()
    
class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        user_data = {
            "email": "test1@mail.com",
            "username": "test1",
            "password": "test1",
        }
        self.user = User.objects.create_user(**user_data)
        Token.objects.get_or_create(user=self.user)

    def test_login(self):
        ''' Login test '''
        url = reverse('login')
        data = {
            "username": "test1",
            "password": "test1",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg='Logging')

    def test_logout(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    