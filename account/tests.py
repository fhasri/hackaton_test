from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from .views import RegistrationView, LoginView, LogoutView, ChangePasswordView, ForgotPasswordView, ForgotPasswordCompleteView
from django.contrib.auth import get_user_model



class AuthTest(APITestCase):
    
    def setUp(self,):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password= '12345',
            is_active= True,
            activation_code='12345'
        )

    def test_registr(self):
        data ={
            'email': 'new_user@gmail.com',
            'password': '12345',
            'password_confirm':'12345',
            'name': 'test',
            'last_name': 'Test'
        }

        request = self.factory.post('api/v1/register/', data , format= 'json')
        # print(request)
        view = RegistrationView.as_view()
        responce = view(request)
        # print(responce)

        assert responce.status_code == 200
        assert get_user_model().objects.filter(email=data['email']).exists()
    
    def test_login(self):
        data = {
            'email':'user@gmail.com',
            'password': '12345',
        }
        request = self.factory.post('api/v1/login/' , data, format='json')
        view = LoginView.as_view()
        responce = view(request)

        assert responce.status_code == 200
        assert 'token' in responce.data

    
    def test_change_password(self):
        data = {
            'old_password': '12345',
            'new_password': '1234',
            'new_password_conf': '1234'
        }

        request = self.factory.post('api/v1/change_password/', data, format='json')
        force_authenticate(request, user=self.user)
        view = ChangePasswordView.as_view()
        responce = view(request)
        print(responce)
        assert responce.status_code == 200


    def test_forgot_confirm(self):
        data = {
        'email':'user@gmail.com',
        }
        request = self.factory.post('api/v1/forgot_password/', data, format='json')
        view = ForgotPasswordView.as_view()
        responce = view(request)
        print(responce)
        assert responce.status_code ==200

    def test_forgot_password_confirm(self):
        data = {
        'email':'user@gmail.com',
        'code': '1234',
        'password': '1234567',
        'password_confirm': '1234567',
    
        }

        request = self.factory.post('api/v1/for/forgot_password_confirm/', data, format='json')
        view = ForgotPasswordCompleteView.as_view()
        responce = view(request)
        print(responce)
        assert responce.status_code == 200



