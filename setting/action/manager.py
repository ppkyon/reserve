from django.contrib.auth.hashers import make_password
from django.http import JsonResponse

from setting.models import ShopOffline, ShopOfflineTime, ShopOnline, ShopOnlineTime, ManagerOffline, ManagerOfflineTime, ManagerOnline, ManagerOnlineTime
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
    manager = AuthUser.objects.filter(display_id=request.POST.get('id')).first()
    if ManagerProfile.objects.filter(manager=manager).exists():
        profile = ManagerProfile.objects.filter(manager=manager).first()
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
            
        if request.POST.get('family_name') and request.POST.get('first_name') and ( manager.status == 2 or manager.status == 1 ):
            manager = AuthUser.objects.filter(id=manager.id).first()
            manager.status = 3
            manager.save()
        elif ( not request.POST.get('family_name') or not request.POST.get('first_name') ) and manager.status == 3:
            manager = AuthUser.objects.filter(id=manager.id).first()
            manager.status = 2
            manager.save()
    else:
        image = None
        if "image_file" in request.FILES:
            image = request.FILES['image_file']

        ManagerProfile.objects.create(
            id = str(uuid.uuid4()),
            manager = manager,
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

        if request.POST.get('family_name') and request.POST.get('first_name') and manager.status == 2:
            manager = AuthUser.objects.filter(id=manager.id).first()
            manager.status = 3
            manager.save()
    
    if request.POST.get('setting'):
        setting = None
        if ShopOffline.objects.filter(display_id=request.POST.get('setting')).exists():
            setting = ShopOffline.objects.filter(display_id=request.POST.get('setting')).first()
            if ManagerOffline.objects.filter(manager=manager, offline=setting).exists():
                setting = ManagerOffline.objects.filter(manager=manager, offline=setting).first()
            else:
                setting = ManagerOffline.objects.create(
                    id = str(uuid.uuid4()),
                    manager = manager,
                    offline = setting,
                )
            ManagerOfflineTime.objects.filter(offline=setting).all().delete()
            for i in range(8):
                number = 1
                for j in range(int(request.POST.get('time_count_'+str(i+1)))):
                    target = str(i+1) + '_' + str(j+1)
                    if ( request.POST.get('time_from_'+target) and request.POST.get('time_to_'+target) ) or ( request.POST.get('time_check_'+str(i+1)) == '1' and number == 1 ):
                        time_from = None
                        if request.POST.get('time_from_'+target):
                            time_from = request.POST.get('time_from_'+target)
                        time_to = None
                        if request.POST.get('time_to_'+target):
                            time_to = request.POST.get('time_to_'+target)
                        holiday_flg = False
                        if request.POST.get('time_check_'+str(i+1)) == '1':
                            holiday_flg = True
                        calendar_flg = False
                        if request.POST.get('calendar_check_'+str(i+1)) == '1':
                            calendar_flg = True

                        ManagerOfflineTime.objects.create(
                            id = str(uuid.uuid4()),
                            offline = setting,
                            week = i + 1,
                            number = number,
                            time_from = time_from,
                            time_to = time_to,
                            holiday_flg = holiday_flg,
                            calendar_flg = calendar_flg,
                        )
                        number = number + 1
        if ShopOnline.objects.filter(display_id=request.POST.get('interview')).exists():
            setting = ShopOnline.objects.filter(display_id=request.POST.get('setting')).first()
            if ManagerOnline.objects.filter(manager=manager, online=setting).exists():
                setting = ManagerOnline.objects.filter(manager=manager, online=setting).first()
            else:
                setting = ManagerOnline.objects.create(
                    id = str(uuid.uuid4()),
                    manager = manager,
                    online = setting,
                )
            ManagerOnlineTime.objects.filter(online=setting).all().delete()
            for i in range(8):
                number = 1
                for j in range(int(request.POST.get('time_count_'+str(i+1)))):
                    target = str(i+1) + '_' + str(j+1)
                    if ( request.POST.get('time_from_'+target) and request.POST.get('time_to_'+target) ) or ( request.POST.get('time_check_'+str(i+1)) == '1' and number == 1 ):
                        time_from = None
                        if request.POST.get('time_from_'+target):
                            time_from = request.POST.get('time_from_'+target)
                        time_to = None
                        if request.POST.get('time_to_'+target):
                            time_to = request.POST.get('time_to_'+target)
                        holiday_flg = False
                        if request.POST.get('time_check_'+str(i+1)) == '1':
                            holiday_flg = True
                        calendar_flg = False
                        if request.POST.get('calendar_check_'+str(i+1)) == '1':
                            calendar_flg = True

                        ManagerOnlineTime.objects.create(
                            id = str(uuid.uuid4()),
                            online = setting,
                            week = i + 1,
                            number = number,
                            time_from = time_from,
                            time_to = time_to,
                            holiday_flg = holiday_flg,
                            calendar_flg = calendar_flg,
                        )
                        number = number + 1
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