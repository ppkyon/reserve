from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import get_template

from sign.models import AuthUser, ManagerProfile, AuthLogin

from common import create_code, create_password

import environ
import os
import uuid

env = environ.Env()
env.read_env('.env')

def add(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    password = create_password()
    user = AuthUser.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(12, AuthUser),
        company = auth_login.company,
        shop = None,
        email = request.POST.get('email'),
        password = make_password(password),
        authority = request.POST.get("authority"),
        company_flg = True,
        status = 1,
        author = request.user.id,
    )

    if env('ENCODING') == 'True':
        site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")
    else:
        site_name = env('SITE_NAME')
    subject = '【アトエル】アトエルアカウント登録について'
    template = get_template('company/setting/email/add_manager.txt')
    site = get_current_site(request)
    context = {
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': site.domain,
        'site_name': site_name,
        'user': user,
        'password': password,
    }
    send_mail(subject, template.render(context), settings.EMAIL_HOST_USER, [request.POST.get("email")])
    
    return JsonResponse( {}, safe=False )

def add_check(request):
    if AuthUser.objects.filter(email=request.POST.get('email')).exists():
        return JsonResponse( {'check': False}, safe=False )
    else:
        return JsonResponse( {'check': True}, safe=False )



def save(request):
    if ManagerProfile.objects.filter(manager=request.user).exists():
        profile = ManagerProfile.objects.filter(manager=request.user).first()
        profile.family_name = request.POST.get('family_name')
        profile.first_name = request.POST.get('first_name')
        profile.family_name_kana = request.POST.get('family_name_kana')
        profile.first_name_kana = request.POST.get('first_name_kana')
        profile.age = request.POST.get('age')
        profile.sex = request.POST.get('sex')
        profile.phone_number = request.POST.get('phone_number').replace('-', '')
        profile.department = request.POST.get('department')
        profile.job = request.POST.get('job')
        profile.work = request.POST.get('work')

        old_image = profile.image
        if "image_file" in request.FILES:
            profile.image = request.FILES['image_file']
        profile.save()

        if old_image and "image_file" in request.FILES:
            os.remove(old_image.url[1:])
            
        if request.POST.get('family_name') and request.POST.get('first_name') and ( request.user.status == 2 or request.user.status == 1 ):
            manager = AuthUser.objects.filter(id=request.user.id).first()
            manager.status = 3
            manager.save()
        elif ( not request.POST.get('family_name') or not request.POST.get('first_name') ) and request.user.status == 3:
            manager = AuthUser.objects.filter(id=request.user.id).first()
            manager.status = 2
            manager.save()
    else:
        image = None
        if "image_file" in request.FILES:
            image = request.FILES['image_file']

        ManagerProfile.objects.create(
            id = str(uuid.uuid4()),
            manager = request.user,
            family_name = request.POST.get('family_name'),
            first_name = request.POST.get('first_name'),
            family_name_kana = request.POST.get('family_name_kana'),
            first_name_kana = request.POST.get('first_name_kana'),
            image = image,
            age = request.POST.get('age'),
            sex = request.POST.get('sex'),
            phone_number = request.POST.get('phone_number').replace('-', ''),
            department = request.POST.get('department'),
            job = request.POST.get('job'),
            work = request.POST.get('work'),
        )

        if request.POST.get('family_name') and request.POST.get('first_name') and request.user.status == 2:
            manager = AuthUser.objects.filter(id=request.user.id).first()
            manager.status = 3
            manager.save()

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )



def delete(request):
    manager = AuthUser.objects.filter(display_id=request.POST.get('id')).first()
    manager.delete_flg = True
    manager.save()
    return JsonResponse( {}, safe=False )



def save_authority(request):
    manager = AuthUser.objects.filter(display_id=request.POST.get('id')).first()
    manager.authority = request.POST.get('authority')
    manager.save()
    return JsonResponse( {}, safe=False )