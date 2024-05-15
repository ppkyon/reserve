from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from sign.models import AuthUser, ManagerProfile, PasswordChangeToken

from common import create_token, create_password, create_expiration_date

import environ
import uuid

env = environ.Env()
env.read_env('.env')

def change(request):
    if request.user.head_flg or request.user.company_flg or request.user.authority > 2:
        token = create_token()
        if PasswordChangeToken.objects.filter(manager=request.user).exists():
            token_data = PasswordChangeToken.objects.filter(manager=request.user).first()
            token_data.password = make_password(request.POST.get("new_password")),
            token_data.token = token
            token_data.expiration_date = create_expiration_date(24)
            token_data.save()
        else:
            PasswordChangeToken.objects.create(
                id = str(uuid.uuid4()),
                manager = request.user,
                password = make_password(request.POST.get("new_password")),
                token = token,
                expiration_date = create_expiration_date(24)
            )
        
        if env('ENCODING') == 'True':
            site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")
        else:
            site_name = env('SITE_NAME')
        subject = '【' + site_name + '】パスワード変更認証メール'
        template = get_template('setting/email/change_password.txt')
        site = get_current_site(request)
        context = {
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': site.domain,
            'uid': force_str(urlsafe_base64_encode(force_bytes(token))),
            'site_name': site_name,
        }
        send_mail(subject, template.render(context), settings.EMAIL_HOST_USER, [request.user.email])
    else:
        request.user.password = make_password(request.POST.get("new_password"))
        request.user.status = 3
        request.user.save()

        manager_profile = ManagerProfile.objects.filter(manager=request.user).first()
        manager_profile.password = request.POST.get("new_password")
        manager_profile.save()
    
    return JsonResponse( {}, safe=False )

def change_check(request):
    if not authenticate(username=request.user.email, password=request.POST.get('now_password')):
        return JsonResponse( {'check': False}, safe=False )
    return JsonResponse( {'check': True}, safe=False )

def reset(request):
    password = create_password()
    user = AuthUser.objects.filter(display_id=request.POST.get('id')).first()
    if user.head_flg or user.company_flg or user.authority > 2:
        user.password = make_password(password)
        user.status = 1
        user.save()

        if env('ENCODING') == 'True':
            site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")
        else:
            site_name = env('SITE_NAME')
        subject = '【' + site_name + '】パスワードリセットメール'
        template = get_template('setting/email/reset_password.txt')
        site = get_current_site(request)
        context = {
            'protocol': 'https' if request.is_secure() else 'http',
            'domain': site.domain,
            'site_name': site_name,
            'user': user,
            'password': password,
        }
        send_mail(subject, template.render(context), settings.EMAIL_HOST_USER, [user.email])
    else:
        user.password = make_password(password)
        user.save()

        manager_profile = ManagerProfile.objects.filter(manager=user).first()
        manager_profile.password = password
        manager_profile.save()

    return JsonResponse( {}, safe=False )