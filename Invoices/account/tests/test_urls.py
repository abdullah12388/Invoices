from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account.views import *


class TestUrls(SimpleTestCase):
    
    def test_login_url_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, userLogin)
        
    def test_UserLogout_url_resolved(self):
        url = reverse('UserLogout')
        self.assertEquals(resolve(url).func, UserLogout)
        
    def test_UserChangePasswordFirstLogin_url_resolved(self):
        url = reverse('UserChangePasswordFirstLogin')
        self.assertEquals(resolve(url).func, UserChangePasswordFirstLogin)
        
    def test_CreateOTPApi_url_resolved(self):
        url = reverse('CreateOTPApi')
        self.assertEquals(resolve(url).func, CreateOTPApi)

    def test_UserForgetPassword_url_resolved(self):
        url = reverse('UserForgetPassword')
        self.assertEquals(resolve(url).func, UserForgetPassword)

    def test_ForgetPasswordGenerateOTPApi_url_resolved(self):
        url = reverse('ForgetPasswordGenerateOTPApi')
        self.assertEquals(resolve(url).func, ForgetPasswordGenerateOTPApi)

    def test_ForgetPasswordcheckOTPApi_url_resolved(self):
        url = reverse('ForgetPasswordcheckOTPApi')
        self.assertEquals(resolve(url).func, ForgetPasswordcheckOTPApi)


