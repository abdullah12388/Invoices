from django .test import TestCase
from account.models import *
from django.contrib.auth.hashers import make_password, check_password


class TestModels(TestCase):
    
    def setUp(self):
        self.user_type_object = UserType.objects.create(
            type = 'Manager'
        )
        self.user_account_object = UserAccount.objects.create(
            first_name = 'Abdullah',
            last_name = 'Kamal',
            email = 'abdullah.mk96@yahoo.com',
            username = 'abdullah',
            password = make_password('As123123'),
            role = self.user_type_object,
            first_login = 1
        )
        self.user_token = Token.objects.create(
            user = self.user_account_object,
            token = 'Asd123456'
        )
        self.user_session = UserSession.objects.create(
            user = self.user_account_object,
            key = 1
        )
        self.user_otp = UserOTP.objects.create(
            user = self.user_account_object,
            key = 'Asd123456789',
            timeout = '2024-04-02 00:00:00.000'
        )
    
    def test_UserType_model_creation(self):
        self.assertEquals(self.user_type_object.type, 'Manager')
    
    def test_UserType_model_str_method(self):
        self.assertEquals(str(self.user_type_object), 'Manager')
    
    def test_UserAccount_model_creation(self):
        self.assertEquals(self.user_account_object.first_name, 'Abdullah')
        self.assertEquals(self.user_account_object.last_name, 'Kamal')
        self.assertEquals(self.user_account_object.email, 'abdullah.mk96@yahoo.com')
        self.assertEquals(self.user_account_object.username, 'abdullah')
        self.assertEquals(check_password('As123123', self.user_account_object.password), True)
        self.assertEquals(self.user_account_object.role, self.user_type_object)
        self.assertEquals(self.user_account_object.first_login, 1)
    
    def test_UserAccount_model_str_method(self):
        self.assertEquals(str(self.user_account_object), 'Abdullah Kamal')
        
    def test_Token_model_creation(self):
        self.assertEquals(self.user_token.user, self.user_account_object)
        self.assertEquals(self.user_token.token, 'Asd123456')
    
    def test_Token_model_str_method(self):
        self.assertEquals(str(self.user_token), 'Abdullah')
    
    def test_TokenAndUsernameCreate_model_signal(self):
        TokenAndUsernameCreate(UserAccount, self.user_account_object, created=True)
        self.assertEquals(Token.objects.filter(user=self.user_account_object).exists(), True)
        
    def test_generate_user_token_model_function(self):
        token = generate_user_token(16)
        self.assertEquals(type(token), str)
        self.assertEquals(len(token), 16)
        
    def test_UserSession_model_creation(self):
        self.assertEquals(self.user_session.user, self.user_account_object)
        self.assertEquals(self.user_session.key, 1)
        
    def test_UserOTP_model_creation(self):
        self.assertEquals(self.user_otp.user, self.user_account_object)
        self.assertEquals(self.user_otp.key, 'Asd123456789')
        self.assertEquals(self.user_otp.timeout, '2024-04-02 00:00:00.000')

    