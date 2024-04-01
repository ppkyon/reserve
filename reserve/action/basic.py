from django.http import JsonResponse

from reserve.models import ReserveBasic
from sign.models import AuthLogin

from common import create_code

import uuid

def save(request):
    business_day = {}
    for i in range(7):
        if request.POST.get('business_check_'+str(i+1)) == '1':
            business_day[i] = True
        else:
            business_day[i] = False
    
    start = 0
    if request.POST.get('start'):
        start = request.POST.get('start')
    deadline = 0
    if request.POST.get('deadline'):
        deadline = request.POST.get('deadline')
    on_time = 0
    if request.POST.get('on_time'):
        on_time = request.POST.get('on_time')
    any_day = 0
    if request.POST.get('any_day'):
        any_day = request.POST.get('any_day')
    any_time = 0
    if request.POST.get('any_time'):
        any_time = request.POST.get('any_time')
    method = 0
    if request.POST.get('method'):
        method = request.POST.get('method')
    unit = 0
    if request.POST.get('unit'):
        unit = request.POST.get('unit')

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    ReserveBasic.objects.filter(shop=auth_login.shop).all().delete()
    ReserveBasic.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(12, ReserveBasic),
        shop = auth_login.shop,
        start = start,
        deadline = deadline,
        on_time = on_time,
        any_day = any_day,
        any_time = any_time,
        method = method,
        unit = unit,
        business_mon_day = business_day[0],
        business_tue_day = business_day[1],
        business_wed_day = business_day[2],
        business_thu_day = business_day[3],
        business_fri_day = business_day[4],
        business_sat_day = business_day[5],
        business_sun_day = business_day[6],

    )
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )