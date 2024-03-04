from django.urls import path
from .views import *

urlpatterns = [
    path('', userLogin, name='login'),
    path('logout/', UserLogout, name='UserLogout'),
    path('change/password/first/login/', UserChangePasswordFirstLogin, name='UserChangePasswordFirstLogin'),
    path('create/otp/api/', CreateOTPApi, name='CreateOTPApi'),
    path('forget/password/', UserForgetPassword, name='UserForgetPassword'),
    path('forget/password/generate/otp/api/', ForgetPasswordGenerateOTPApi, name='ForgetPasswordGenerateOTPApi'),
    path('forget/password/check/otp/api/', ForgetPasswordcheckOTPApi, name='ForgetPasswordcheckOTPApi'),
]
