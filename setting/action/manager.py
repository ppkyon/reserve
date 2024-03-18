from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from sign.models import AuthUser, ManagerProfile, AuthLogin

from common import create_code, create_password

import environ
import os
import uuid

env = environ.Env()
env.read_env('.env')

def add(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    code = create_code(12, AuthUser)
    password = create_password()
    user = AuthUser.objects.create(
        id = str(uuid.uuid4()),
        display_id = code,
        company = auth_login.company,
        shop = auth_login.shop,
        email = 'atelle' + str(code) + '@atelle' + str(code) + '.jp',
        password = make_password(password),
        authority = request.POST.get("authority"),
        status = 1,
        author = request.user.id,
    )
    ManagerProfile.objects.create(
        id = str(uuid.uuid4()),
        manager = user,
        family_name = request.POST.get('family_name'),
        first_name = request.POST.get('first_name'),
        family_name_kana = request.POST.get('family_name_kana'),
        first_name_kana = request.POST.get('first_name_kana'),
        password = password,
    )
    
    return JsonResponse( {}, safe=False )

def add_check(request):
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