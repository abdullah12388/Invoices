from typing import Iterable, Optional
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import secrets
import string


# Create your models here.
class UserType(models.Model):
    type = models.CharField(max_length=254)
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type


class UserAccount(models.Model):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    email = models.CharField(max_length=254, blank=True, null=True)
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    role = models.ForeignKey(UserType, on_delete=models.CASCADE, related_name='role')
    add_date = models.DateTimeField(auto_now_add=True)
    first_login = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    attempts = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Token(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='userToken')
    token = models.CharField(max_length=254)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

@receiver(post_save, sender=UserAccount)
def TokenAndUsernameCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(
            user=instance,
            token=generate_user_token()
        )

def generate_user_token(length=16):
    """Generate a random user token of specified length."""
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


class UserSession(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='userSession')
    key = models.BooleanField() # 1 for login 0 for logout
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class UserOTP(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='userOTP')
    key = models.CharField(max_length=50)
    timeout = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
