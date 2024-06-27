from django.db.models import Q, Subquery, OuterRef

from flow.models import HeadFlow, UserFlow, UserFlowSchedule
from reserve.models import ReserveOfflineSetting, ReserveOnlineSetting
from sign.models import AuthLogin
from table.models import MiniTableSearch, MiniTableNumber, MiniTableSort
from user.models import LineUser, UserProfile

from common import get_model_field

import datetime
import re

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
        query = get_query_data(request, auth_login.company, auth_login.shop, 'today')
        sort = MiniTableSort.objects.filter(url='/dashboard/', company=auth_login.company, shop=auth_login.shop, manager=request.user, page='dashboard', item='today').first()
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__user_profile__name_kana', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__user_profile__name_kana', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            elif sort.target == 'date':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            elif sort.target == 'setting':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__flow_tab__number', 'date', 'time', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__flow_tab__number', 'date', 'time', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            elif sort.target == 'line':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__proxy_flg', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__proxy_flg', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            else:
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
        else:
            data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
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
        query = get_query_data(request, auth_login.company, auth_login.shop, 'new')
        sort = MiniTableSort.objects.filter(url='/dashboard/', company=auth_login.company, shop=auth_login.shop, manager=request.user, page='dashboard', item='new').first()
        new = UserFlowSchedule.objects.filter(id=OuterRef('pk'), created_at__gte=datetime.datetime.now()-datetime.timedelta(days=1)).values("check_flg")
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'flow__user__user_profile__name_kana', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', '-flow__user__user_profile__name_kana', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            elif sort.target == 'date':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', '-date', '-time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            elif sort.target == 'setting':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'flow__flow_tab__number', 'date', 'time', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', '-flow__flow_tab__number', 'date', 'time', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            elif sort.target == 'line':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'flow__user__proxy_flg', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', '-flow__user__proxy_flg', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            else:
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', '-date', '-time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
        else:
            data = list(UserFlowSchedule.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('new', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
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
                        if data_item['number'] > 1:
                            prev_schedule = UserFlowSchedule.objects.filter(flow__id=data[data_index]['flow']['id'], number=data_item['number']-1, temp_flg=False).exclude(number=0).values(*get_model_field(UserFlowSchedule)).first()
                            if prev_schedule and prev_schedule['date']:
                                data[data_index]['flow']['user']['reserve'] = get_reserve_date(prev_schedule) + ' → ' + data[data_index]['flow']['user']['reserve']
                    data[data_index]['number'] = start + data_index + 1
                    if data_item['created_at'] >= datetime.datetime.now() - datetime.timedelta(days=1):
                        data[data_index]['new_flg'] = True
                    else:
                        data[data_index]['new_flg'] = False
                    data[data_index]['total'] = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).distinct().count()
    if request.POST.get('item') == 'after':
        query = get_query_data(request, auth_login.company, auth_login.shop, 'after')
        sort = MiniTableSort.objects.filter(url='/dashboard/', company=auth_login.company, shop=auth_login.shop, manager=request.user, page='dashboard', item='after').first()
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__user_profile__name_kana', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__user_profile__name_kana', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            elif sort.target == 'date':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            elif sort.target == 'setting':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__flow_tab__number', 'date', 'time', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__flow_tab__number', 'date', 'time', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            elif sort.target == 'line':
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__proxy_flg', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__proxy_flg', 'date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
            else:
                if sort.sort == 1:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
                else:
                    data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
        else:
            data = list(UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', 'flow__flow_tab__number', '-created_at').values(*get_model_field(UserFlowSchedule)).distinct().all()[start:end])
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
        sort = MiniTableSort.objects.filter(url='/dashboard/', company=auth_login.company, shop=auth_login.shop, manager=request.user, page='dashboard', item='line').first()
        new = UserFlowSchedule.objects.filter(id=OuterRef('pk'), created_at__gte=datetime.datetime.now()-datetime.timedelta(days=1)).values("check_flg")
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    data = list(LineUser.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('new', 'user_profile__name_kana', 'created_at').values(*get_model_field(LineUser)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(LineUser.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('new', '-user_profile__name_kana', 'created_at').values(*get_model_field(LineUser)).distinct().all()[start:end])
                else:
                    data = list(LineUser.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('new', 'created_at').values(*get_model_field(LineUser)).distinct().all()[start:end])
            else:
                if sort.sort == 1:
                    data = list(LineUser.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('new', 'created_at').values(*get_model_field(LineUser)).distinct().all()[start:end])
                elif sort.sort == 2:
                    data = list(LineUser.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('new', '-created_at').values(*get_model_field(LineUser)).distinct().all()[start:end])
                else:
                    data = list(LineUser.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('new', 'created_at').values(*get_model_field(LineUser)).distinct().all()[start:end])
        else:
            data = list(LineUser.objects.annotate(new=Subquery(new.values('check_flg')[:1])).filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('new', 'created_at').values(*get_model_field(LineUser)).distinct().all()[start:end])
        if len(data) > 0:
            for data_index, data_item in enumerate(data):
                data[data_index]['profile'] = UserProfile.objects.filter(user__id=data[data_index]['id']).values(*get_model_field(UserProfile)).first()
                data[data_index]['number'] = start + data_index + 1
                if data_item['created_at'] >= datetime.datetime.now() - datetime.timedelta(days=1):
                    data[data_index]['new_flg'] = True
                else:
                    data[data_index]['new_flg'] = False
                data[data_index]['total'] = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('created_at').values(*get_model_field(LineUser)).distinct().count()
    return data



def get_query_data(request, company, shop, page):
    query = Q()
    search = MiniTableSearch.objects.filter(url='/dashboard/', company=company, shop=shop, manager=request.user, page=page).all()
    for search_item in search:
        search_query = Q()
        if search_item.item == 'name':
            search_query.add(Q(**{'flow__user__user_profile__name__icontains': search_item.text}), Q.AND)
        elif search_item.item == 'kana':
            search_query.add(Q(**{'flow__user__user_profile__name_kana__icontains': search_item.text}), Q.AND)
        elif search_item.item == 'phone':
            search_query.add(Q(**{'flow__user__user_profile__phone_number__icontains': search_item.text.replace('-', '')}), Q.AND)
        elif search_item.item == 'email':
            search_query.add(Q(**{'flow__user__user_profile__email__icontains': search_item.text.replace('-', '')}), Q.AND)
        elif search_item.item == 'age_from':
            search_query.add(Q(**{'flow__user__user_profile__age__gte': search_item.text.replace('歳', '')}), Q.AND)
        elif search_item.item == 'age_to':
            search_query.add(Q(**{'flow__user__user_profile__age__lte': search_item.text.replace('歳', '')}), Q.AND)
        elif search_item.item == 'time_from':
            search_query.add(Q(**{'time__gte': search_item.text}), Q.AND)
        elif search_item.item == 'time_to':
            search_query.add(Q(**{'time__lte': search_item.text}), Q.AND)
        elif search_item.item == 'datetime_from':
            date = datetime.datetime.strptime(search_item.text, '%Y/%m/%d %H:%M')
            search_query.add(Q(**{'date__gte': datetime.datetime(date.year, date.month, date.day, 0, 0, 0)}), Q.AND)
            search_query.add(Q(**{'time__gte': datetime.time(date.hour, date.minute, 0)}), Q.AND)
        elif search_item.item == 'datetime_to':
            date = datetime.datetime.strptime(search_item.text, '%Y/%m/%d %H:%M')
            search_query.add(Q(**{'date__lte': datetime.datetime(date.year, date.month, date.day, 0, 0, 0)}), Q.AND)
            search_query.add(Q(**{'time__lte': datetime.time(date.hour, date.minute, 0)}), Q.AND)
        elif search_item.item == 'create_from':
            date = datetime.datetime.strptime(search_item.text, '%Y/%m/%d')
            search_query.add(Q(**{'created_at__gte': datetime.datetime(date.year, date.month, date.day, 0, 0, 0)}), Q.AND)
        elif search_item.item == 'create_to':
            date = datetime.datetime.strptime(search_item.text, '%Y/%m/%d')
            search_query.add(Q(**{'created_at__lte': datetime.datetime(date.year, date.month, date.day, 23, 59, 59)}), Q.AND)
        elif search_item.item == 'sex':
            search_query.add(Q(**{'flow__user__user_profile__sex': search_item.text}), Q.AND)
        elif search_item.item == 'member':
            if search_item.text == '1':
                search_query.add(Q(**{'flow__user__member_flg': True}), Q.AND)
            elif search_item.text == '2':
                search_query.add(Q(**{'flow__user__member_flg': False}), Q.AND)
        elif search_item.item == 'change':
            if search_item.text == '1':
                search_query.add(~Q(**{'number': 1}), Q.AND)
            elif search_item.text == '2':
                search_query.add(Q(**{'number': 1}), Q.AND)
        elif search_item.item == 'flow':
            search_flow = search_item.text.split(",")
            flow_list = list()
            for flow in HeadFlow.objects.order_by('-created_at').all():
                flow_tab_list = flow.description.split('→')
                for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
                    if str(flow_tab_index) in search_flow:
                        flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                        if not flow_chart_name in flow_list:
                            flow_list.append(flow_chart_name)
            search_query.add(Q(**{'flow__flow_tab__name__in': flow_list}), Q.AND)
        elif search_item.item == 'manager':
            search_manager = search_item.text.split(",")
            search_query.add(Q(**{'manager__display_id__in': search_manager}), Q.AND)
        elif search_item.item == 'facility':
            search_facility = search_item.text.split(",")
            search_query.add(Q(**{'offline_facility__display_id__in': search_facility}), Q.OR)
            search_query.add(Q(**{'online_facility__display_id__in': search_facility}), Q.OR)
        elif search_item.item == 'place':
            search_place = search_item.text.split(",")
            search_query.add(Q(**{'offline__offline__display_id__in': search_place}), Q.OR)
            search_query.add(Q(**{'online__online__display_id__in': search_place}), Q.OR)
        query.add(search_query, Q.AND)
    return query



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