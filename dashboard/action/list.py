from django.db.models import Q

from flow.models import UserFlow, UserFlowSchedule
from reserve.models import ReserveOfflineSetting, ReserveOnlineSetting
from sign.models import AuthLogin
from table.models import MiniTableNumber
from user.models import LineUser, UserProfile

from common import get_model_field

import datetime

def get_list(request, page):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    url = request.path.replace('paging/', '').replace('search/', '')
    if url == '/':
        url = '/dashboard/'

    page = int(page)
    number = 5
    table_number = MiniTableNumber.objects.filter(url=url, shop=auth_login.shop, manager=request.user, page=request.POST.get('page'), item=request.POST.get('item')).first()
    if table_number:
        number = table_number.number
    
    start = number * ( page - 1 )
    end = number * page

    now = datetime.datetime.now()
    after = now + datetime.timedelta(days=1)
    
    data = list()
    if request.POST.get('item') == 'today':
        data = list(UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
        if len(data) > 0:
            for data_index, data_item in enumerate(data):
                if data_item['date']:
                    data[data_index]['flow'] = UserFlow.objects.filter(id=data[data_index]['flow']).values(*get_model_field(UserFlow)).first()
                    data[data_index]['flow']['user'] = LineUser.objects.filter(id=data[data_index]['flow']['user']).values(*get_model_field(LineUser)).first()
                    if data[data_index]['flow']['user']:
                        data[data_index]['flow']['user']['profile'] = UserProfile.objects.filter(user__id=data[data_index]['flow']['user']['id']).values(*get_model_field(UserProfile)).first()
                        data[data_index]['flow']['user']['flow'] = UserFlow.objects.filter(id=UserFlowSchedule.objects.filter(id=data_item['id']).first().flow.id).values(*get_model_field(UserFlow)).first()
                        data[data_index]['flow']['user']['schedule'] = UserFlowSchedule.objects.filter(id=data_item['id']).values(*get_model_field(UserFlowSchedule)).first()
                        if data[data_index]['flow']['user']['schedule']['offline']:
                            data[data_index]['flow']['user']['schedule']['offline'] = ReserveOfflineSetting.objects.filter(id=data[data_index]['flow']['user']['schedule']['offline']).values(*get_model_field(ReserveOfflineSetting)).first()
                        elif data[data_index]['flow']['user']['schedule']['online']:
                            data[data_index]['flow']['user']['schedule']['online'] = ReserveOnlineSetting.objects.filter(id=data[data_index]['flow']['user']['schedule']['online']).values(*get_model_field(ReserveOnlineSetting)).first()
                        data[data_index]['flow']['user']['reserve'] = get_reserve_date(data_item)
                    data[data_index]['number'] = start + data_index + 1
                    data[data_index]['total'] = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).distinct().count()
    if request.POST.get('item') == 'new':
        data = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end]
        if len(data) > 0:
            for data_index, data_item in enumerate(data):
                if data_item['date']:
                    data[data_index]['flow'] = UserFlow.objects.filter(id=data[data_index]['flow']).values(*get_model_field(UserFlow)).first()
                    data[data_index]['flow']['user'] = LineUser.objects.filter(id=data[data_index]['flow']['user']).values(*get_model_field(LineUser)).first()
                    if data[data_index]['flow']['user']:
                        data[data_index]['flow']['user']['profile'] = UserProfile.objects.filter(user__id=data[data_index]['flow']['user']['id']).values(*get_model_field(UserProfile)).first()
                        data[data_index]['flow']['user']['flow'] = UserFlow.objects.filter(id=UserFlowSchedule.objects.filter(id=data_item['id']).first().flow.id).values(*get_model_field(UserFlow)).first()
                        data[data_index]['flow']['user']['schedule'] = UserFlowSchedule.objects.filter(id=data_item['id']).values(*get_model_field(UserFlowSchedule)).first()
                        if data[data_index]['flow']['user']['schedule']['offline']:
                            data[data_index]['flow']['user']['schedule']['offline'] = ReserveOfflineSetting.objects.filter(id=data[data_index]['flow']['user']['schedule']['offline']).values(*get_model_field(ReserveOfflineSetting)).first()
                        elif data[data_index]['flow']['user']['schedule']['online']:
                            data[data_index]['flow']['user']['schedule']['online'] = ReserveOnlineSetting.objects.filter(id=data[data_index]['flow']['user']['schedule']['online']).values(*get_model_field(ReserveOnlineSetting)).first()
                        data[data_index]['flow']['user']['reserve'] = get_reserve_date(data_item)
                    data[data_index]['number'] = start + data_index + 1
                    data[data_index]['total'] = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).distinct().count()
    if request.POST.get('item') == 'after':
        data = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end]
        if len(data) > 0:
            for data_index, data_item in enumerate(data):
                if data_item['date']:
                    data[data_index]['flow'] = UserFlow.objects.filter(id=data[data_index]['flow']).values(*get_model_field(UserFlow)).first()
                    data[data_index]['flow']['user'] = LineUser.objects.filter(id=data[data_index]['flow']['user']).values(*get_model_field(LineUser)).first()
                    if data[data_index]['flow']['user']:
                        data[data_index]['flow']['user']['profile'] = UserProfile.objects.filter(user__id=data[data_index]['flow']['user']['id']).values(*get_model_field(UserProfile)).first()
                        data[data_index]['flow']['user']['flow'] = UserFlow.objects.filter(id=UserFlowSchedule.objects.filter(id=data_item['id']).first().flow.id).values(*get_model_field(UserFlow)).first()
                        data[data_index]['flow']['user']['schedule'] = UserFlowSchedule.objects.filter(id=data_item['id']).values(*get_model_field(UserFlowSchedule)).first()
                        if data[data_index]['flow']['user']['schedule']['offline']:
                            data[data_index]['flow']['user']['schedule']['offline'] = ReserveOfflineSetting.objects.filter(id=data[data_index]['flow']['user']['schedule']['offline']).values(*get_model_field(ReserveOfflineSetting)).first()
                        elif data[data_index]['flow']['user']['schedule']['online']:
                            data[data_index]['flow']['user']['schedule']['online'] = ReserveOnlineSetting.objects.filter(id=data[data_index]['flow']['user']['schedule']['online']).values(*get_model_field(ReserveOnlineSetting)).first()
                        data[data_index]['flow']['user']['reserve'] = get_reserve_date(data_item)
                    data[data_index]['number'] = start + data_index + 1
                    data[data_index]['total'] = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).distinct().count()
    if request.POST.get('item') == 'line':
        data = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('created_at').values(*get_model_field(LineUser)).distinct().all()[start:end]
        if len(data) > 0:
            for data_index, data_item in enumerate(data):
                data[data_index]['profile'] = UserProfile.objects.filter(user__id=data[data_index]['id']).values(*get_model_field(UserProfile)).first()
                data[data_index]['number'] = start + data_index + 1
                data[data_index]['total'] = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('created_at').values(*get_model_field(LineUser)).distinct().count()
    return data



def get_reserve_date(schedule):
    date = datetime.datetime(schedule['date'].year, schedule['date'].month, schedule['date'].day, schedule['time'].hour, schedule['time'].minute, 0)
    if schedule['online']:
        online = ReserveOnlineSetting.objects.filter(id=schedule['online']).first()
        add_date = date + datetime.timedelta(minutes=online.time)
    elif schedule['offline']:
        offline = ReserveOfflineSetting.objects.filter(id=schedule['offline']).first()
        add_date = date + datetime.timedelta(minutes=offline.time)
    if schedule['date'].weekday() == 0:
        week = '(月)'
    elif schedule['date'].weekday() == 1:
        week = '(火)'
    elif schedule['date'].weekday() == 2:
        week = '(水)'
    elif schedule['date'].weekday() == 3:
        week = '(木)'
    elif schedule['date'].weekday() == 4:
        week = '(金)'
    elif schedule['date'].weekday() == 5:
        week = '(土)'
    elif schedule['date'].weekday() == 6:
        week = '(日)'
    reserve_data = str(date.month) + '/' + str(date.day) + week + ' ' + str(date.hour) + ':' + str(date.minute).zfill(2) + '～' + str(add_date.hour) + ':' + str(add_date.minute).zfill(2)
    return reserve_data