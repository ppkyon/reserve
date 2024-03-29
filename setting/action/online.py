from django.http import JsonResponse

from setting.models import ShopOnline, ShopOnlineTime
from sign.models import AuthLogin

from common import create_code

import uuid

def add(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    online = ShopOnline.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(12, ShopOnline),
        shop = auth_login.shop,
        title = request.POST.get('title'),
        name = request.POST.get('name'),
        outline = request.POST.get('outline'),
        note = request.POST.get('note'),
    )
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
                flg = False
                if request.POST.get('time_check_'+str(i+1)) == '1':
                    flg = True
                
                ShopOnlineTime.objects.create(
                    id = str(uuid.uuid4()),
                    online = online,
                    week = i + 1,
                    number = number,
                    time_from = time_from,
                    time_to = time_to,
                    flg = flg,
                )
                number = number + 1
    return JsonResponse( {}, safe=False )

def add_check(request):
    check = True
    error_list = list()
    for i in range(8):
        last_time = None
        for j in range(int(request.POST.get('time_count_'+str(i+1)))):
            target = str(i+1) + '_' + str(j+1)
            if ( request.POST.get('time_from_'+target) and request.POST.get('time_to_'+target) ):
                if request.POST.get('time_from_'+target) >= request.POST.get('time_to_'+target) or ( last_time and last_time >= request.POST.get('time_from_'+target)):
                    error_list.append(target)
                    check = False
                last_time = request.POST.get('time_to_'+target)
            else:
                if request.POST.get('time_from_'+target) or request.POST.get('time_to_'+target):
                    error_list.append(target)
                    check = False
    return JsonResponse( {'check': check, 'error_list': error_list}, safe=False )

def save(request):
    online = ShopOnline.objects.filter(display_id=request.POST.get('id')).first()
    online.title = request.POST.get('title')
    online.name = request.POST.get('name')
    online.outline = request.POST.get('outline')
    online.note = request.POST.get('note')
    online.save()
    
    ShopOnlineTime.objects.filter(online=online).all().delete()
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
                flg = False
                if request.POST.get('time_check_'+str(i+1)) == '1':
                    flg = True

                ShopOnlineTime.objects.create(
                    id = str(uuid.uuid4()),
                    online = online,
                    week = i + 1,
                    number = number,
                    time_from = time_from,
                    time_to = time_to,
                    flg = flg,
                )
                number = number + 1
    return JsonResponse( {}, safe=False )

def save_check(request):
    check = True
    error_list = list()
    for i in range(8):
        last_time = None
        for j in range(int(request.POST.get('time_count_'+str(i+1)))):
            target = str(i+1) + '_' + str(j+1)
            if ( request.POST.get('time_from_'+target) and request.POST.get('time_to_'+target) ):
                if request.POST.get('time_from_'+target) >= request.POST.get('time_to_'+target) or ( last_time and last_time >= request.POST.get('time_from_'+target)):
                    error_list.append(target)
                    check = False
                last_time = request.POST.get('time_to_'+target)
            else:
                if request.POST.get('time_from_'+target) or request.POST.get('time_to_'+target):
                    error_list.append(target)
                    check = False
    return JsonResponse( {'check': check, 'error_list': error_list}, safe=False )

def delete(request):
    ShopOnlineTime.objects.filter(online=ShopOnline.objects.filter(display_id=request.POST.get('id')).first()).all().delete()
    ShopOnline.objects.filter(display_id=request.POST.get('id')).delete()
    return JsonResponse( {}, safe=False )