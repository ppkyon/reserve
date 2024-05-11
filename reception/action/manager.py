from django.http import JsonResponse

from reception.models import ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import ReserveOfflineSetting, ReserveOnlineSetting
from setting.models import ShopOffline, ShopOnline, ShopOfflineTime, ShopOnlineTime, ManagerOffline, ManagerOnline, ManagerOfflineTime, ManagerOnlineTime
from sign.models import AuthLogin, AuthUser

from common import create_code, get_model_field

import calendar
import datetime
import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    agenda = calendar.Calendar(6)
    days = agenda.monthdatescalendar(int(request.POST.get('year')), int(request.POST.get('month')))
    days_count = 0
    for week in days:
        for day in week:
            if day.month == int(request.POST.get('month')):
                days_count = days_count + 1
    
    for offline in ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all():
        for manager in AuthUser.objects.filter(shop=auth_login.shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all():
            for i in range(days_count):
                date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), ( i + 1 ) )
                ReceptionOfflineManager.objects.filter(offline=offline, manager=manager, reception_date__date=date).all().delete()

                if request.POST.get('flg_' + str(offline.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 )):
                    if request.POST.get('flg_' + str(offline.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 )) == '0':
                        ReceptionOfflineManager.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, ReceptionOfflineManager),
                            offline = offline,
                            number = 1,
                            manager = manager,
                            reception_date = date,
                            reception_from = None,
                            reception_to = None,
                            reception_flg = False,
                        )
                    elif request.POST.get('flg_' + str(offline.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 )) == '1':
                        for j in range(int(request.POST.get('count_' + str(offline.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 )))):
                            reception_offline_manager = ReceptionOfflineManager.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, ReceptionOfflineManager),
                                offline = offline,
                                number = ( j + 1 ),
                                manager = manager,
                                reception_date = date,
                                reception_from = request.POST.get('from_' + str(offline.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 ) + '_' + str( j + 1 )),
                                reception_to = request.POST.get('to_' + str(offline.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 ) + '_' + str( j + 1 )),
                                reception_flg = True,
                            )
                            for offline_item in ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all():
                                for reserve_offline_setting in ReserveOfflineSetting.objects.filter(offline=offline_item).order_by('created_at').all():
                                    if request.POST.get('setting_' + str(reserve_offline_setting.display_id) + '_' + str(offline.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 ) + '_' + str( j + 1 )) == 'false':
                                        ReceptionOfflineManagerSetting.objects.create(
                                            id = str(uuid.uuid4()),
                                            offline = reserve_offline_setting,
                                            manager = reception_offline_manager,
                                            flg = False,
                                        )
                                    else:
                                        ReceptionOfflineManagerSetting.objects.create(
                                            id = str(uuid.uuid4()),
                                            offline = reserve_offline_setting,
                                            manager = reception_offline_manager,
                                            flg = True,
                                        )
    
    for online in ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all():
        for manager in AuthUser.objects.filter(shop=auth_login.shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all():
            for i in range(days_count):
                date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), ( i + 1 ) )
                ReceptionOnlineManager.objects.filter(online=online, manager=manager, reception_date__date=date).all().delete()

                if request.POST.get('flg_' + str(online.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 )):
                    if request.POST.get('flg_' + str(online.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 )) == '0':
                        ReceptionOnlineManager.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, ReceptionOnlineManager),
                            online = online,
                            number = 1,
                            manager = manager,
                            reception_date = date,
                            reception_from = None,
                            reception_to = None,
                            reception_flg = False,
                        )
                    elif request.POST.get('flg_' + str(online.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 )) == '1':
                        for j in range(int(request.POST.get('count_' + str(online.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 )))):
                            reception_online_manager = ReceptionOnlineManager.objects.create(
                                id = str(uuid.uuid4()),
                                display_id = create_code(12, ReceptionOnlineManager),
                                online = online,
                                number = ( j + 1 ),
                                manager = manager,
                                reception_date = date,
                                reception_from = request.POST.get('from_' + str(online.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 ) + '_' + str( j + 1 )),
                                reception_to = request.POST.get('to_' + str(online.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 ) + '_' + str( j + 1 )),
                                reception_flg = True,
                            )
                            for online_item in ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all():
                                for reserve_online_setting in ReserveOnlineSetting.objects.filter(online=online_item).order_by('created_at').all():
                                    if request.POST.get('setting_' + str(reserve_online_setting.display_id) + '_' + str(online.display_id) + '_' + str(manager.display_id) + '_' + str( i + 1 ) + '_' + str( j + 1 )) == 'false':
                                        ReceptionOnlineManagerSetting.objects.create(
                                            id = str(uuid.uuid4()),
                                            online = reserve_online_setting,
                                            manager = reception_online_manager,
                                            flg = False,
                                        )
                                    else:
                                        ReceptionOnlineManagerSetting.objects.create(
                                            id = str(uuid.uuid4()),
                                            online = reserve_online_setting,
                                            manager = reception_online_manager,
                                            flg = True,
                                        )
                            
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )



def get(request):
    setting = None
    if ShopOffline.objects.filter(display_id=request.POST.get("setting_id")).exists():
        setting = ShopOffline.objects.filter(display_id=request.POST.get("setting_id")).first()
    if ShopOnline.objects.filter(display_id=request.POST.get("setting_id")).exists():
        setting = ShopOnline.objects.filter(display_id=request.POST.get("setting_id")).first()
    manager = AuthUser.objects.filter(display_id=request.POST.get("manager_id")).first()
    if ShopOffline.objects.filter(display_id=request.POST.get("setting_id")).exists():
        manager_setting = ManagerOffline.objects.filter(offline=setting, manager=manager).first()
    if ShopOnline.objects.filter(display_id=request.POST.get("setting_id")).exists():
        manager_setting = ManagerOnline.objects.filter(online=setting, manager=manager).first()
    if manager_setting:
        if ShopOffline.objects.filter(display_id=request.POST.get("setting_id")).exists():
            time = list(ManagerOfflineTime.objects.filter(offline=manager_setting).order_by('week', 'number').values(*get_model_field(ManagerOfflineTime)).all())
        if ShopOnline.objects.filter(display_id=request.POST.get("setting_id")).exists():
            time = list(ManagerOnlineTime.objects.filter(online=manager_setting).order_by('week', 'number').values(*get_model_field(ManagerOnlineTime)).all())
    else:
        if ShopOffline.objects.filter(display_id=request.POST.get("setting_id")).exists():
            time = list(ShopOfflineTime.objects.filter(offline=setting).order_by('week', 'number').values(*get_model_field(ShopOfflineTime)).all())
        if ShopOnline.objects.filter(display_id=request.POST.get("setting_id")).exists():
            time = list(ShopOnlineTime.objects.filter(online=setting).order_by('week', 'number').values(*get_model_field(ShopOnlineTime)).all())
    return JsonResponse( time, safe=False )