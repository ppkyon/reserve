from django.db.models import Q
from django.http import JsonResponse

from reserve.models import ReserveOfflineSetting, ReserveOnlineSetting, ReserveOfflineFacility, ReserveOnlineFacility, ReserveCalendarDate, ReserveCalendarUpdate
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthLogin

from common import create_code

import datetime
import uuid

def save(request):
    random_list = list()
    for i in range(int(request.POST.get('count'))):
        random_list.append(request.POST.get('random_'+str( i + 1 )))

    ReserveOfflineFacility.objects.filter(offline=ShopOffline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all().delete()
    ReserveOnlineFacility.objects.filter(online=ShopOnline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all().delete()

    for i in range(int(request.POST.get('count'))):
        if ReserveOfflineFacility.objects.filter(display_id=request.POST.get('random_'+str(i+1))).exists():
            offline = ReserveOfflineFacility.objects.filter(display_id=request.POST.get('random_'+str(i+1))).first()
            offline.number = ( i + 1 )
            offline.name = request.POST.get('name_'+str( i + 1 ))
            offline.count = request.POST.get('count_'+str( i + 1 ))
            offline.order = request.POST.get('order_'+str( i + 1 ))
            offline.save()
        elif ReserveOnlineFacility.objects.filter(display_id=request.POST.get('random_'+str(i+1))).exists():
            online = ReserveOnlineFacility.objects.filter(display_id=request.POST.get('random_'+str(i+1))).first()
            online.number = ( i + 1 )
            online.name = request.POST.get('name_'+str( i + 1 ))
            online.count = request.POST.get('count_'+str( i + 1 ))
            online.order = request.POST.get('order_'+str( i + 1 ))
            online.save()
        else:
            if ShopOffline.objects.filter(display_id=request.POST.get('id')).exists():
                ReserveOfflineFacility.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOfflineFacility),
                    offline = ShopOffline.objects.filter(display_id=request.POST.get('id')).first(),
                    number = ( i + 1 ),
                    name = request.POST.get('name_'+str( i + 1 )),
                    count = request.POST.get('count_'+str( i + 1 )),
                    order = request.POST.get('order_'+str( i + 1 )),
                )
            if ShopOnline.objects.filter(display_id=request.POST.get('id')).exists():
                ReserveOnlineFacility.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOnlineFacility),
                    online = ShopOnline.objects.filter(display_id=request.POST.get('id')).first(),
                    number = ( i + 1 ),
                    name = request.POST.get('name_'+str( i + 1 )),
                    count = request.POST.get('count_'+str( i + 1 )),
                    order = request.POST.get('order_'+str( i + 1 )),
                )
    
    offline_list = list()
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    for offline in ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all():
        for offline_setting in ReserveOfflineSetting.objects.filter(offline=offline).all():
            offline_list.append(offline_setting.display_id)
            all_date = ReserveCalendarDate.objects.filter(offline=offline_setting).order_by('date').all()
            for all_date_item in all_date:
                date = all_date_item.date
                for offline_setting in ReserveOfflineSetting.objects.filter(offline=offline).all():
                    if not ReserveCalendarUpdate.objects.filter(shop=auth_login.shop, offline=offline_setting, date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0)).exists():
                        ReserveCalendarUpdate.objects.create(
                            id = str(uuid.uuid4()),
                            shop = auth_login.shop,
                            offline = offline_setting,
                            date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                            flg = True,
                        )
    
    online_list = list()
    for online in ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all():
        for online_setting in ReserveOnlineSetting.objects.filter(online=online).all():
            online_list.append(offline_setting.display_id)
            all_date = ReserveCalendarDate.objects.filter(online=online_setting).all()
            for all_date_item in all_date:
                date = all_date_item.date
                for online_setting in ReserveOnlineSetting.objects.filter(online=online).all():
                    if not ReserveCalendarUpdate.objects.filter(shop=auth_login.shop, online=online_setting, date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0)).exists():
                        ReserveCalendarUpdate.objects.create(
                            id = str(uuid.uuid4()),
                            shop = auth_login.shop,
                            online = online_setting,
                            date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                            flg = True,
                        )

    ReserveCalendarDate.objects.filter(Q(shop=auth_login.shop)).exclude(Q(offline__display_id__in=offline_list)|Q(online__display_id__in=online_list)).all().delete()

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )