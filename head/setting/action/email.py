from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from sign.models import AuthUser, EmailChangeToken

from common import create_token, create_expiration_date

import environ
import uuid

env = environ.Env()
env.read_env('.env')

def change(request):
    token = create_token()
    if EmailChangeToken.objects.filter(manager=request.user).exists():
        token_data = EmailChangeToken.objects.filter(manager=request.user).first()
        token_data.email = request.POST.get("email"),
        token_data.token = token
        token_data.expiration_date = create_expiration_date(24)
        token_data.save()
    else:
        EmailChangeToken.objects.create(
            id = str(uuid.uuid4()),
            manager = request.user,
            email = request.POST.get("email"),
            token = token,
            expiration_date = create_expiration_date(24)
        )

    if env('ENCODING') == 'True':
        site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")
    else:
        site_name = env('SITE_NAME')
    subject = '【' + site_name + '】メールアドレス変更認証メール'
    template = get_template('head/setting/email/change_email.txt')
    site = get_current_site(request)
    context = {
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': site.domain,
        'uid': force_str(urlsafe_base64_encode(force_bytes(token))),
        'site_name': site_name,
    }
    send_mail(subject, template.render(context), settings.EMAIL_HOST_USER, [request.POST.get("email")])

    return JsonResponse( {}, safe=False )

def change_check(request):
    if AuthUser.objects.filter(email=request.POST.get('email')).exists():
        return JsonResponse( {'check': False, 'message': 'すでに登録済みのメールアドレスです'}, safe=False )
    if not authenticate(username=request.user.email, password=request.POST.get('password')):
        return JsonResponse( {'check': False, 'message': 'パスワードが間違っています'}, safe=False )
    return JsonResponse( {'check': True}, safe=False )