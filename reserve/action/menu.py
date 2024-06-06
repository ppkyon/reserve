from django.db.models import Q
from django.http import JsonResponse

from flow.models import HeadFlow
from reserve.models import (
    ReserveOfflineSetting, ReserveOnlineSetting, ReserveOfflineFacility, ReserveOnlineFacility, ReserveCalendarDate, ReserveCalendarUpdate,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu, ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
)
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthLogin, AuthUser

from common import create_code

import datetime
import re
import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    ReserveOfflineManagerMenu.objects.filter(shop=auth_login.shop).all().delete()
    ReserveOnlineManagerMenu.objects.filter(shop=auth_login.shop).all().delete()
    ReserveOfflineFacilityMenu.objects.filter(shop=auth_login.shop).all().delete()
    ReserveOnlineFacilityMenu.objects.filter(shop=auth_login.shop).all().delete()
    ReserveOfflineFlowMenu.objects.filter(shop=auth_login.shop).all().delete()
    ReserveOnlineFlowMenu.objects.filter(shop=auth_login.shop).all().delete()

    flow_list = list()
    for flow in HeadFlow.objects.order_by('-created_at').all():
        flow_name_list = flow.description.split('→')
        for flow_name_index, flow_name_item in enumerate(flow_name_list):
            if flow_name_index != 0:
                flow_name = re.sub('\(.*?\)','',flow_name_item).strip()
                if not flow_name in flow_list:
                    flow_list.append(flow_name)

    for manager_item in request.POST.get('manager_list').split(','):
        manager = manager_item.split('_')
        if ReserveOfflineSetting.objects.filter(display_id=manager[0]).exists():
            ReserveOfflineManagerMenu.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, ReserveOfflineManagerMenu),
                shop = auth_login.shop,
                offline = ReserveOfflineSetting.objects.filter(display_id=manager[0]).first(),
                manager = AuthUser.objects.filter(display_id=manager[1]).first(),
            )
        if ReserveOnlineSetting.objects.filter(display_id=manager[0]).exists():
            ReserveOnlineManagerMenu.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, ReserveOnlineManagerMenu),
                shop = auth_login.shop,
                online = ReserveOnlineSetting.objects.filter(display_id=manager[0]).first(),
                manager = AuthUser.objects.filter(display_id=manager[1]).first(),
            )
    for facility_item in request.POST.get('facility_list').split(','):
        facility = facility_item.split('_')
        if ReserveOfflineSetting.objects.filter(display_id=facility[0]).exists():
            ReserveOfflineFacilityMenu.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, ReserveOfflineFacilityMenu),
                shop = auth_login.shop,
                offline = ReserveOfflineSetting.objects.filter(display_id=facility[0]).first(),
                facility = ReserveOfflineFacility.objects.filter(display_id=facility[1]).first(),
            )
        if ReserveOnlineSetting.objects.filter(display_id=facility[0]).exists():
            ReserveOnlineFacilityMenu.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, ReserveOnlineFacilityMenu),
                shop = auth_login.shop,
                online = ReserveOnlineSetting.objects.filter(display_id=facility[0]).first(),
                facility = ReserveOnlineFacility.objects.filter(display_id=facility[1]).first(),
            )
    for flow_item in request.POST.get('flow_list').split(','):
        flow = flow_item.split('_')
        if ReserveOfflineSetting.objects.filter(display_id=flow[0]).exists():
            ReserveOfflineFlowMenu.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, ReserveOfflineFlowMenu),
                shop = auth_login.shop,
                offline = ReserveOfflineSetting.objects.filter(display_id=flow[0]).first(),
                flow = flow_list[int(flow[1])-1],
            )
        if ReserveOnlineSetting.objects.filter(display_id=flow[0]).exists():
            ReserveOnlineFlowMenu.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, ReserveOnlineFlowMenu),
                shop = auth_login.shop,
                online = ReserveOnlineSetting.objects.filter(display_id=flow[0]).first(),
                flow = flow_list[int(flow[1])-1],
            )
    
    offline_list = list()
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