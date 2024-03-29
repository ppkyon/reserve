from django.http import JsonResponse

from setting.models import ShopOffline, ShopOfflineTime, ShopOnline, ShopOnlineTime, ManagerOffline, ManagerOfflineTime, ManagerOnline, ManagerOnlineTime
from sign.models import AuthUser
from table.models import TableSearch

from common import get_model_field

import uuid

def search(request):
    if TableSearch.objects.filter(url=request.POST.get('url'), manager=request.user).exists():
        search = TableSearch.objects.filter(url=request.POST.get('url'), manager=request.user).first()
        search.text = request.POST.get('id')
        search.save()
    else:
        search = TableSearch.objects.create(
            id = str(uuid.uuid4()),
            url = request.POST.get('url'),
            manager = request.user,
            text = request.POST.get('id'),
        )
    return JsonResponse( {}, safe=False )



def get(request):
    setting= None
    if ShopOffline.objects.filter(display_id=request.POST.get('id')).exists():
        setting = ShopOffline.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(ShopOffline)).first()
        setting['time'] = list(ShopOfflineTime.objects.filter(offline__id=setting['id']).order_by('week', 'number').values(*get_model_field(ShopOfflineTime)).all())
        for setting_time_index, setting_time_item in enumerate(setting['time']):
            if setting['time'][setting_time_index]['time_from']:
                setting['time'][setting_time_index]['time_from'] = setting_time_item['time_from'].strftime('%H:%M')
            if setting['time'][setting_time_index]['time_to']:
                setting['time'][setting_time_index]['time_to'] = setting_time_item['time_to'].strftime('%H:%M')
    if ShopOnline.objects.filter(display_id=request.POST.get('id')).exists():
        setting = ShopOnline.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(ShopOnline)).first()
        setting['time'] = list(ShopOnlineTime.objects.filter(online__id=setting['id']).order_by('week', 'number').values(*get_model_field(ShopOnlineTime)).all())
        for setting_time_index, setting_time_item in enumerate(setting['time']):
            if setting['time'][setting_time_index]['time_from']:
                setting['time'][setting_time_index]['time_from'] = setting_time_item['time_from'].strftime('%H:%M')
            if setting['time'][setting_time_index]['time_to']:
                setting['time'][setting_time_index]['time_to'] = setting_time_item['time_to'].strftime('%H:%M')
    return JsonResponse( setting, safe=False )

def get_time(request):
    manager = AuthUser.objects.filter(display_id=request.POST.get('manager_id')).first()
    if ShopOffline.objects.filter(display_id=request.POST.get('id')).exists():
        setting = ShopOffline.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(ShopOffline)).first()
        if ManagerOffline.objects.filter(manager=manager, offline__id=setting['id']).exists():
            setting['time'] = list(ManagerOfflineTime.objects.filter(offline=ManagerOffline.objects.filter(manager=manager, offline__id=setting['id']).first()).order_by('week').values(*get_model_field(ManagerOfflineTime)).all())
        else:
            setting['time'] = list(ShopOfflineTime.objects.filter(offline__id=setting['id']).order_by('week').values(*get_model_field(ShopOfflineTime)).all())
        for setting_time_index, setting_time_item in enumerate(setting['time']):
            if setting['time'][setting_time_index]['time_from']:
                setting['time'][setting_time_index]['time_from'] = setting_time_item['time_from'].strftime('%H:%M')
            if setting['time'][setting_time_index]['time_to']:
                setting['time'][setting_time_index]['time_to'] = setting_time_item['time_to'].strftime('%H:%M')
    if ShopOnline.objects.filter(display_id=request.POST.get('id')).exists():
        setting = ShopOnline.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(ShopOnline)).first()
        if ManagerOnline.objects.filter(manager=manager, online__id=setting['id']).exists():
            setting['time'] = list(ManagerOnlineTime.objects.filter(online=ManagerOnline.objects.filter(manager=manager, online__id=setting['id']).first()).order_by('week').values(*get_model_field(ManagerOnlineTime)).all())
        else:
            setting['time'] = list(ShopOnlineTime.objects.filter(online__id=setting['id']).order_by('week').values(*get_model_field(ShopOnlineTime)).all())
        for setting_time_index, setting_time_item in enumerate(setting['time']):
            if setting['time'][setting_time_index]['time_from']:
                setting['time'][setting_time_index]['time_from'] = setting_time_item['time_from'].strftime('%H:%M')
            if setting['time'][setting_time_index]['time_to']:
                setting['time'][setting_time_index]['time_to'] = setting_time_item['time_to'].strftime('%H:%M')
    return JsonResponse( setting, safe=False )