from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from system.views import send_email
import random
from django.conf import settings
from datetime import datetime, timedelta
import secrets
import string
# Create your views here.


def generate_otp(length=10):
    """Generate a random user token of specified length."""
    characters = string.ascii_letters + string.digits
    otp = ''.join(secrets.choice(characters) for _ in range(length))
    return otp


def CreateOTPApi(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # print(username, password)
        # print(make_password(password))
        try:
            user = UserAccount.objects.get(username=username)
            # print('user first login => ', user.first_login)
            if user.first_login:
                request.session['username'] = user.username
                # return HttpResponseRedirect('/change/password/first/login/')
                return JsonResponse(data={'status': '/change/password/first/login/'}, safe=False)
            else:
                password_checher = check_password(password, user.password)
                print('password_checher => ', password_checher)
                # print(password, user.password)
                if password_checher:
                    if user.is_locked:
                        return JsonResponse(data={'status': 'invalid'}, safe=False)
                    # print(password_checher)
                    current_datetime = datetime.now()
                    check_user_otp = UserOTP.objects.filter(user=user)
                    if check_user_otp.exists():
                        user_otp = check_user_otp.first()
                        if current_datetime >= user_otp.timeout:
                            # create new otp
                            user_otp.key = generate_otp()
                            user_otp.timeout = current_datetime + timedelta(minutes=5)
                            user_otp.save()
                    else:
                        user_otp = UserOTP.objects.create(
                            user=user,
                            key=generate_otp(),
                            timeout=current_datetime + timedelta(minutes=5)
                        )
                    # send old otp
                    sender = settings.EMAIL_USER
                    receiver = [user.email]
                    subject = f"OTP | {user.email}"
                    message = f"The OTP is {user_otp.key}."
                    send_email(sender,receiver,subject,message)
                    return JsonResponse(data={'status': 'valid'}, safe=False)
                else:
                    user.attempts += 1
                    if user.attempts == 3:
                        user.is_locked = True
                    user.save()
                    return JsonResponse(data={'status': 'invalid'}, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse(data={'status': 'invalid'}, safe=False)


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        otp = request.POST.get('otp', None)
        # print(username, password)
        try:
            user = UserAccount.objects.get(username=username)
            # print('user first login => ', user.first_login)
            password_checher = check_password(password, user.password)
            print('password_checher => ', password_checher)
            # print(password, user.password)
            if password_checher:
                # print(password_checher)
                #user_otp = UserOTP.objects.filter(user=user)
                #if user_otp.exists():
                    # print(user_otp.first().key, otp)
                    # print(type(user_otp.first().key), type(otp))
                    #if user_otp.first().key == otp:
                userToken = Token.objects.get(user=user).token
                request.session['user_token'] = userToken
                UserSession.objects.create(user=user, key=True)
                    # print(user)
                if user.role.id == 1: # vendor
                    return HttpResponseRedirect('/system/Vendor/')
                if user.role.id == 2: # procurement
                    return HttpResponseRedirect('/system/Procurement/')
                if user.role.id == 3: # manager
                    return HttpResponseRedirect('/system/Manager/')
                if user.role.id == 4: # Presales
                    return HttpResponseRedirect('/system/Presales/')
                    #else:
                        #return HttpResponseRedirect('/?error=IOTP')
                #else:
                    #return HttpResponseRedirect('/?error=NOTP')
            else:
                user.attempts += 1
                if user.attempts == 3:
                    user.is_locked = True
                user.save()
                return HttpResponseRedirect('/?error=IPASS')
        except Exception as ex:
            print(ex)
    return render(request, 'login.html', {})



def UserLogout(request):
    if 'user_token' in request.session:
        user = Token.objects.get(token=request.session.get('user_token', None)).user
        UserSession.objects.create(user=user, key=False)
        del request.session['user_token']
    if 'username' in request.session:
        del request.session['username']
    return HttpResponseRedirect('/')


def UserChangePasswordFirstLogin(request):
    if 'username' in request.session:
        if request.method == 'POST':
            username = request.POST.get('reg_username', None)
            password = request.POST.get('new_password', None)
            try:
                user = UserAccount.objects.get(username=username)
                user.password = make_password(password)
                user.first_login = False
                user.save()
                del request.session['username']
                return HttpResponseRedirect('/')
            except Exception as ex:
                print(ex)
        return render(request, 'changePasswordFirstLogin.html', {'username': request.session['username']})
    else:
        return HttpResponseRedirect('/logout/')


def UserForgetPassword(request):
    if request.method == 'POST':
        username = request.POST.get('reg_username', None)
        password = request.POST.get('new_password', None)
        otp = request.POST.get('otp', None)
        user_obj = UserAccount.objects.get(username=username)
        user_otp = UserOTP.objects.filter(user=user_obj, key=otp)
        if user_otp.exists():
            user_obj.password = make_password(password)
            user_obj.save()
            return HttpResponseRedirect('/')
        else:
            print('OTP Expired')
    return render(request, 'forgetPassword.html', {})


def ForgetPasswordGenerateOTPApi(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        try:
            current_datetime = datetime.now()
            user = UserAccount.objects.get(username=username)
            user_otp = UserOTP.objects.get(user=user)
            user_otp.key = generate_otp()
            user_otp.timeout = current_datetime + timedelta(minutes=5)
            user_otp.save()
            sender = settings.EMAIL_USER
            receiver = [user.email]
            subject = f"OTP | {user.email}"
            message = f"The OTP is {user_otp.key}."
            send_email(sender,receiver,subject,message)
            return JsonResponse(data={'status': 'valid'}, safe=False)
        except Exception as ex:
            print(ex)
            return JsonResponse(data={'status': 'invalid'}, safe=False)


def ForgetPasswordcheckOTPApi(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        otp = request.POST.get('otp', None)
        user_otp = UserOTP.objects.select_related('user')\
            .filter(user__username=username, key=otp)
        if user_otp.exists():
            return JsonResponse(data={'status': 'valid'}, safe=False)
        else:
            return JsonResponse(data={'status': 'invalid'}, safe=False)
            





