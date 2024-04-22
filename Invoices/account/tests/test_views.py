from django.test import TestCase, Client
from django.urls import reverse, resolve
from account.views import *
from django.contrib.auth.hashers import make_password, check_password
import json


class TestViews(TestCase):

    def setUp(self):
        self.user_type = UserType.objects.create(
            type = 'Manager'
        )
        UserAccount.objects.create(
            first_name='Abdullah',
            last_name='Kamal',
            email='abdullah.mk96@yahoo.com',
            username='abdullah',
            password=make_password('As123123'),
            role=self.user_type,
            first_login=1
        )
        UserAccount.objects.create(
            first_name='Abdullah',
            last_name='Kamal',
            email='abdullah.mk96@yahoo.com',
            username='ali',
            password=make_password('As123123'),
            role=self.user_type,
            first_login=0
        )
        self.client = Client()
        self.CreateOTPApi_url = reverse('CreateOTPApi')

    # def test_generate_otp_view_function(self):
    #     otp = generate_otp(10)
    #     self.assertEqual(len(otp), 10)
    #     self.assertEqual(type(otp), str)

    def test_CreateOTPApi_view_function(self):
        response1 = self.client.post(self.CreateOTPApi_url, {
            'username': 'abdullah',
            'password': 'As123123'
        })
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.post(self.CreateOTPApi_url, {
            'username': 'ali',
            'password': 'As123123'
        })
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json().get('status'), 'valid')



