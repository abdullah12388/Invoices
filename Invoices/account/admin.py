from django import forms
from django.contrib import admin
from .models import *
from django.contrib.auth.hashers import make_password
# Register your models here.


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'type',
        'add_date'
    ]


@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'email',
        'username',
        'password',
        'role',
        'add_date',
        'first_login',
        'is_locked',
        'attempts'
    ]
    
    def save_model(self, request, obj, form, change):
        # Check if the instance is being created
        if not change:
            if obj.password:
                obj.password = make_password(obj.password)
        # Call the parent class's save_model() to perform the actual saving
        super().save_model(request, obj, form, change)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = [
        'get_user_email',
        'token',
        'timestamp'
    ]

    def get_user_email(self, obj):
        return obj.user.username
    get_user_email.short_description = 'Username'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'key',
        'timestamp'
    ]


@admin.register(UserOTP)
class UserOTPAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'key',
        'timeout',
        'timestamp'
    ]







