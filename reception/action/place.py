from django.http import JsonResponse

from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace
from setting.models import ShopOffline, ShopOnline, ShopOfflineTime, ShopOnlineTime

from common import create_code, get_model_field

import datetime
import uuid

def save(request):
    setting = None
    if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
        setting = ShopOffline.objects.filter(display_id=request.POST.get("id")).first()
    if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
        setting = ShopOnline.objects.filter(display_id=request.POST.get("id")).first()

    for i in range(int(request.POST.get('day'))):
        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), (i+1))
        if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
            ReceptionOfflinePlace.objects.filter(offline=setting, reception_date__date=date).all().delete()
        if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
            ReceptionOnlinePlace.objects.filter(online=setting, reception_date__date=date).all().delete()

        flg = False
        if request.POST.get('setting_not_' + str(i+1)) == '1':
            flg = True
        count = 0
        number = 1
        for j in range(int(request.POST.get('setting_input_count_'+str(i+1)))):
            target = str(i+1) + '_' + str(j+1)
            if ( request.POST.get('setting_not_' + str(i+1)) == '1' and number == 1 ) or ( request.POST.get('setting_not_' + str(i+1)) == '0' and request.POST.get('setting_from_' + target) and request.POST.get('setting_to_' + target) ):
                if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
                    ReceptionOfflinePlace.objects.create(
                        id = str(uuid.uuid4()),
                        display_id = create_code(12, ReceptionOfflinePlace),
                        offline = setting,
                        number = number,
                        reception_date = date,
                        reception_from = request.POST.get('setting_from_' + target),
                        reception_to = request.POST.get('setting_to_' + target),
                        reception_count = count,
                        reception_flg = flg,
                    )
                if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
                    ReceptionOnlinePlace.objects.create(
                        id = str(uuid.uuid4()),
                        display_id = create_code(12, ReceptionOnlinePlace),
                        online = setting,
                        number = number,
                        reception_date = date,
                        reception_from = request.POST.get('setting_from_' + target),
                        reception_to = request.POST.get('setting_to_' + target),
                        reception_count = count,
                        reception_flg = flg,
                    )
                number = number + 1
    return JsonResponse( {}, safe=False )

def save_check(request):
    check = True
    error_list = list()
    for i in range(int(request.POST.get('day'))):
        last_time = None
        for j in range(int(request.POST.get('setting_input_count_'+str(i+1)))):
            target = str(i+1) + '_' + str(j+1)
            if ( request.POST.get('setting_from_'+target) and request.POST.get('setting_to_'+target) ):
                if request.POST.get('setting_from_'+target) >= request.POST.get('setting_to_'+target) or ( last_time and last_time >= request.POST.get('setting_from_'+target)):
                    error_list.append(target)
                    check = False
                last_time = request.POST.get('setting_to_'+target)
            else:
                if request.POST.get('setting_from_'+target) or request.POST.get('setting_to_'+target):
                    error_list.append(target)
                    check = False
    return JsonResponse( {'check': check, 'error_list': error_list}, safe=False )



def get(request):
    setting = None
    if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
        setting = ShopOffline.objects.filter(display_id=request.POST.get("id")).values(*get_model_field(ShopOffline)).first()
        setting['time'] = list(ShopOfflineTime.objects.filter(offline__id=setting['id']).order_by('week', 'number').values(*get_model_field(ShopOfflineTime)).all())
    if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
        setting = ShopOnline.objects.filter(display_id=request.POST.get("id")).values(*get_model_field(ShopOnline)).first()
        setting['time'] = list(ShopOnlineTime.objects.filter(online__id=setting['id']).order_by('week', 'number').values(*get_model_field(ShopOnlineTime)).all())
    return JsonResponse( setting, safe=False )