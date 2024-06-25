from django.db import models
from django.db.models import Q
from django.shortcuts import redirect

from view import ShopView

from flow.models import HeadFlow, UserFlowSchedule
from reserve.models import ReserveOfflineFacility, ReserveOnlineFacility
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthLogin, AuthUser, ManagerProfile
from table.models import MiniTableSearch, MiniTableNumber, MiniTableSort
from talk.models import TalkRead
from user.models import LineUser, UserProfile

from itertools import chain

import datetime
import re

class IndexView(ShopView):
    def get(self, request, **kwargs):
        return redirect('/dashboard/')

class DashboardView(ShopView):
    template_name = 'dashboard/index.html'
    title = 'ダッシュボード'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()

        context['search'] = get_search_data(self.request, auth_login.company, auth_login.shop)
        context['condition'] = get_condition_data(auth_login.shop, context['search'])
        
        now = datetime.datetime.now()
        after = now + datetime.timedelta(days=1)
        context['today_user_count'] = LineUser.objects.filter(shop=auth_login.shop, created_at__range=(now.replace(hour=0, minute=0, second=0, microsecond=0), now.replace(hour=23, minute=59, second=59, microsecond=0)), delete_flg=False).count()

        query = get_query_data(self.request, auth_login.company, auth_login.shop, 'today')
        context['today_reserve_table'] = get_table_data(self, auth_login.shop, 'dashboard', 'today', UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time').count())
        context['today_reserve_count'] = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).count()
        context['today_reserve_sort'] = MiniTableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user, page='dashboard', item='today').first()
        context['today_reserve_list'] = list()
        today_reserve_list = list()
        if context['today_reserve_sort']:
            if context['today_reserve_sort'].target == 'name':
                if context['today_reserve_sort'].sort == 1:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__user_profile__name_kana', 'date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
                elif context['today_reserve_sort'].sort == 2:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__user_profile__name_kana', 'date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
                else:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
            elif context['today_reserve_sort'].target == 'date':
                if context['today_reserve_sort'].sort == 1:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
                elif context['today_reserve_sort'].sort == 2:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', '-created_at').all()[:context['today_reserve_table']['number']]
                else:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
            elif context['today_reserve_sort'].target == 'setting':
                if context['today_reserve_sort'].sort == 1:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__flow_tab__number', 'date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
                elif context['today_reserve_sort'].sort == 2:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__flow_tab__number', 'date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
                else:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
            elif context['today_reserve_sort'].target == 'line':
                if context['today_reserve_sort'].sort == 1:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__proxy_flg', 'date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
                elif context['today_reserve_sort'].sort == 2:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__proxy_flg', 'date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
                else:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
            else:
                if context['today_reserve_sort'].sort == 1:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
                elif context['today_reserve_sort'].sort == 2:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', '-created_at').all()[:context['today_reserve_table']['number']]
                else:
                    today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
        else:
            today_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['today_reserve_table']['number']]
        for schedule in today_reserve_list:
            if schedule.date:
                schedule.flow.user.profile = UserProfile.objects.filter(user=schedule.flow.user).first()
                schedule.flow.user.flow = schedule.flow
                schedule.flow.user.schedule = schedule
                schedule.flow.user.reserve = get_reserve_date(schedule)
                context['today_reserve_list'].append(schedule.flow.user)

        query = get_query_data(self.request, auth_login.company, auth_login.shop, 'new')
        context['new_reserve_table'] = get_table_data(self, auth_login.shop, 'dashboard', 'new', UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).count())
        context['new_reserve_count'] = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).count()
        context['new_reserve_sort'] = MiniTableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user, page='dashboard', item='new').first()
        context['new_reserve_list'] = list()
        new_reserve_list = list()
        if context['new_reserve_sort']:
            if context['new_reserve_sort'].target == 'name':
                if context['new_reserve_sort'].sort == 1:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__user_profile__name_kana', 'date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
                elif context['new_reserve_sort'].sort == 2:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__user_profile__name_kana', 'date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
                else:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
            elif context['new_reserve_sort'].target == 'date':
                if context['new_reserve_sort'].sort == 1:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
                elif context['new_reserve_sort'].sort == 2:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', '-created_at').all()[:context['new_reserve_table']['number']]
                else:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
            elif context['new_reserve_sort'].target == 'setting':
                if context['new_reserve_sort'].sort == 1:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__flow_tab__number', 'date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
                elif context['new_reserve_sort'].sort == 2:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__flow_tab__number', 'date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
                else:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
            elif context['new_reserve_sort'].target == 'line':
                if context['new_reserve_sort'].sort == 1:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__proxy_flg', 'date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
                elif context['new_reserve_sort'].sort == 2:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__proxy_flg', 'date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
                else:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
            else:
                if context['new_reserve_sort'].sort == 1:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
                elif context['new_reserve_sort'].sort == 2:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', '-created_at').all()[:context['new_reserve_table']['number']]
                else:
                    new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
        else:
            new_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, check_flg=False, date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['new_reserve_table']['number']]
        for schedule in new_reserve_list:
            if schedule.date:
                schedule.flow.user.profile = UserProfile.objects.filter(user=schedule.flow.user).first()
                schedule.flow.user.flow = schedule.flow
                schedule.flow.user.schedule = schedule
                schedule.flow.user.reserve = get_reserve_date(schedule)

                if schedule.number > 1:
                    prev_schedule = UserFlowSchedule.objects.filter(flow=schedule.flow, number=schedule.number-1, temp_flg=False).exclude(number=0).first()
                    if prev_schedule and prev_schedule.date:
                        schedule.flow.user.reserve = get_reserve_date(prev_schedule) + ' → ' + schedule.flow.user.reserve

                context['new_reserve_list'].append(schedule.flow.user)

        query = get_query_data(self.request, auth_login.company, auth_login.shop, 'after')
        context['after_reserve_table'] = get_table_data(self, auth_login.shop, 'dashboard', 'after', UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).count())
        context['after_reserve_sort'] = MiniTableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user, page='dashboard', item='after').first()
        context['after_reserve_list'] = list()
        after_reserve_list = list()
        if context['after_reserve_sort']:
            if context['after_reserve_sort'].target == 'name':
                if context['after_reserve_sort'].sort == 1:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__user_profile__name_kana', 'date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
                elif context['after_reserve_sort'].sort == 2:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__user_profile__name_kana', 'date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
                else:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
            elif context['after_reserve_sort'].target == 'date':
                if context['after_reserve_sort'].sort == 1:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
                elif context['after_reserve_sort'].sort == 2:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', '-created_at').all()[:context['after_reserve_table']['number']]
                else:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
            elif context['after_reserve_sort'].target == 'setting':
                if context['after_reserve_sort'].sort == 1:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__flow_tab__number', 'date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
                elif context['after_reserve_sort'].sort == 2:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__flow_tab__number', 'date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
                else:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
            elif context['after_reserve_sort'].target == 'line':
                if context['after_reserve_sort'].sort == 1:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('flow__user__proxy_flg', 'date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
                elif context['after_reserve_sort'].sort == 2:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-flow__user__proxy_flg', 'date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
                else:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
            else:
                if context['after_reserve_sort'].sort == 1:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
                elif context['after_reserve_sort'].sort == 2:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('-date', '-time', '-created_at').all()[:context['after_reserve_table']['number']]
                else:
                    after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
        else:
            after_reserve_list = UserFlowSchedule.objects.filter(query, flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0), date__isnull=False, temp_flg=False).exclude(Q(number=0)|Q(join=2)).order_by('date', 'time', '-created_at').all()[:context['after_reserve_table']['number']]
        for schedule in after_reserve_list:
            if schedule.date:
                schedule.flow.user.profile = UserProfile.objects.filter(user=schedule.flow.user).first()
                schedule.flow.user.flow = schedule.flow
                schedule.flow.user.schedule = schedule
                schedule.flow.user.reserve = get_reserve_date(schedule)
                context['after_reserve_list'].append(schedule.flow.user)

        context['new_line_table'] = get_table_data(self, auth_login.shop, 'dashboard', 'line', LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('created_at').count())
        context['new_line_sort'] = MiniTableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user, page='dashboard', item='line').first()
        context['new_line_list'] = list()
        new_line_list = list()
        after_reserve_list = list()
        if context['new_line_sort']:
            if context['new_line_sort'].target == 'name':
                if context['new_line_sort'].sort == 1:
                    new_line_list = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('user_profile__name_kana', 'created_at').all()[:context['new_line_table']['number']]
                elif context['new_line_sort'].sort == 2:
                    new_line_list = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('-user_profile__name_kana', 'created_at').all()[:context['new_line_table']['number']]
                else:
                    new_line_list = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('created_at').all()[:context['new_line_table']['number']]
            else:
                if context['new_line_sort'].sort == 1:
                    new_line_list = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('created_at').all()[:context['new_line_table']['number']]
                elif context['new_line_sort'].sort == 2:
                    new_line_list = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('-created_at').all()[:context['new_line_table']['number']]
                else:
                    new_line_list = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('created_at').all()[:context['new_line_table']['number']]
        else:
            new_line_list = LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).order_by('created_at').all()[:context['new_line_table']['number']]
        for user in new_line_list:
            user.profile = UserProfile.objects.filter(user=user).first()
            context['new_line_list'].append(user)

        context['message_required_count'] = 0
        talk_read = TalkRead.objects.filter(user__delete_flg=False, manager=self.request.user, user__talk_manager__manager=self.request.user, user__talk_status__status=1).aggregate(sum_read_count=models.Sum('read_count'))
        if talk_read and talk_read['sum_read_count']:
            context['message_required_count'] = talk_read['sum_read_count']

        context['age_list'] = [i for i in range(101)]
        return context



def get_table_data(self, shop, page, item, count):
    number = 5
    if MiniTableNumber.objects.filter(url=self.request.path, shop=shop, manager=self.request.user, page=page, item=item).exists():
        number = MiniTableNumber.objects.filter(url=self.request.path, shop=shop, manager=self.request.user, page=page, item=item).first().number
    count = count
    count_start = 1
    if number > count:
        count_end = count
    else:
        count_end = number
    if count_end == 0:
        count_start = 0
    return {
        'number': number,
        'count': count,
        'count_start': count_start,
        'count_end': count_end,
    }



def get_search_data(request, company, shop):
    today = {}
    for search_item in MiniTableSearch.objects.filter(url=request.path, company=company, shop=shop, manager=request.user, page='today').order_by('created_at').all():
        today[search_item.item] = search_item.text
        if search_item.item == 'age_from':
            if 'age' in today:
                today['age'] = search_item.text + today['age']
            else:
                today['age'] = search_item.text + ' ～ '
        if search_item.item == 'age_to':
            if 'age' in today:
                today['age'] = today['age'] + search_item.text
            else:
                today['age'] = ' ～ ' + search_item.text
        if search_item.item == 'time_from':
            if 'time' in today:
                today['time'] = search_item.text + today['time']
            else:
                today['time'] = search_item.text + ' ～ '
        if search_item.item == 'time_to':
            if 'time' in today:
                today['time'] = today['time'] + search_item.text
            else:
                today['time'] = ' ～ ' + search_item.text
        if search_item.item == 'flow':
            flow_list = list()
            for flow in HeadFlow.objects.order_by('-created_at').all():
                flow_tab_list = flow.description.split('→')
                for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
                    if flow_tab_index == 0:
                        if not 'ブロック' in flow_list:
                            flow_list.append('ブロック')
                    else:
                        flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                        if not flow_chart_name in flow_list:
                            flow_list.append(flow_chart_name)
            for flow_index, flow_value in enumerate(search_item.text.split(",")):
                if flow_index == 0:
                    today['flow_all'] = flow_list[int(flow_value)]
                else:
                    today['flow_all'] = today['flow_all'] + ', ' + flow_list[int(flow_value)]
        if search_item.item == 'manager':
            today['manager_list'] = list()
            for manager_index, manager_value in enumerate(search_item.text.split(",")):
                today['manager_list'].append(manager_value)
                manager_profile = ManagerProfile.objects.filter(manager=AuthUser.objects.filter(display_id=manager_value).first()).first()
                if manager_index == 0:
                    if AuthUser.objects.filter(display_id=manager_value).exists():
                        today['manager_all'] = manager_profile.family_name + manager_profile.first_name
                else:
                    if AuthUser.objects.filter(display_id=manager_value).exists():
                        today['manager_all'] = today['manager_all'] + ', ' + manager_profile.family_name + manager_profile.first_name
        if search_item.item == 'facility':
            today['facility_list'] = list()
            for facility_index, facility_value in enumerate(search_item.text.split(",")):
                today['facility_list'].append(facility_value)
                if facility_index == 0:
                    if ReserveOfflineFacility.objects.filter(display_id=facility_value).exists():
                        today['facility_all'] = ReserveOfflineFacility.objects.filter(display_id=facility_value).first().name
                    if ReserveOnlineFacility.objects.filter(display_id=facility_value).exists():
                        today['facility_all'] = ReserveOnlineFacility.objects.filter(display_id=facility_value).first().name
                else:
                    if ReserveOfflineFacility.objects.filter(display_id=facility_value).exists():
                        today['facility_all'] = today['facility_all'] + ', ' + ReserveOfflineFacility.objects.filter(display_id=facility_value).first().name
                    if ReserveOnlineFacility.objects.filter(display_id=facility_value).exists():
                        today['facility_all'] = today['facility_all'] + ', ' + ReserveOnlineFacility.objects.filter(display_id=facility_value).first().name
        if search_item.item == 'place':
            today['place_list'] = list()
            for place_index, place_value in enumerate(search_item.text.split(",")):
                today['place_list'].append(place_value)
                if place_index == 0:
                    if ShopOffline.objects.filter(display_id=place_value).exists():
                        today['place_all'] = ShopOffline.objects.filter(display_id=place_value).first().name
                    if ShopOnline.objects.filter(display_id=place_value).exists():
                        today['place_all'] = ShopOnline.objects.filter(display_id=place_value).first().name
                else:
                    if ShopOffline.objects.filter(display_id=place_value).exists():
                        today['place_all'] = today['place_all'] + ', ' + ShopOffline.objects.filter(display_id=facility_value).first().name
                    if ShopOnline.objects.filter(display_id=place_value).exists():
                        today['place_all'] = today['place_all'] + ', ' + ShopOnline.objects.filter(display_id=facility_value).first().name
        
    new = {}
    for search_item in MiniTableSearch.objects.filter(url=request.path, company=company, shop=shop, manager=request.user, page='new').order_by('created_at').all():
        new[search_item.item] = search_item.text
        if search_item.item == 'age_from':
            if 'age' in new:
                new['age'] = search_item.text + new['age']
            else:
                new['age'] = search_item.text + ' ～ '
        if search_item.item == 'age_to':
            if 'age' in new:
                new['age'] = new['age'] + search_item.text
            else:
                new['age'] = ' ～ ' + search_item.text
        if search_item.item == 'datetime_from':
            if 'datetime' in new:
                new['datetime'] = search_item.text + new['datetime']
            else:
                new['datetime'] = search_item.text + ' ～ '
        if search_item.item == 'datetime_to':
            if 'datetime' in new:
                new['datetime'] = new['datetime'] + search_item.text
            else:
                new['datetime'] = ' ～ ' + search_item.text
        if search_item.item == 'create_from':
            if 'create' in new:
                new['create'] = search_item.text + new['create']
            else:
                new['create'] = search_item.text + ' ～ '
        if search_item.item == 'create_to':
            if 'create' in new:
                new['create'] = new['create'] + search_item.text
            else:
                new['create'] = ' ～ ' + search_item.text
        if search_item.item == 'flow':
            flow_list = list()
            for flow in HeadFlow.objects.order_by('-created_at').all():
                flow_tab_list = flow.description.split('→')
                for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
                    if flow_tab_index == 0:
                        if not 'ブロック' in flow_list:
                            flow_list.append('ブロック')
                    else:
                        flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                        if not flow_chart_name in flow_list:
                            flow_list.append(flow_chart_name)
            for flow_index, flow_value in enumerate(search_item.text.split(",")):
                if flow_index == 0:
                    new['flow_all'] = flow_list[int(flow_value)]
                else:
                    new['flow_all'] = new['flow_all'] + ', ' + flow_list[int(flow_value)]
        if search_item.item == 'manager':
            new['manager_list'] = list()
            for manager_index, manager_value in enumerate(search_item.text.split(",")):
                new['manager_list'].append(manager_value)
                manager_profile = ManagerProfile.objects.filter(manager=AuthUser.objects.filter(display_id=manager_value).first()).first()
                if manager_index == 0:
                    if AuthUser.objects.filter(display_id=manager_value).exists():
                        new['manager_all'] = manager_profile.family_name + manager_profile.first_name
                else:
                    if AuthUser.objects.filter(display_id=manager_value).exists():
                        new['manager_all'] = new['manager_all'] + ', ' + manager_profile.family_name + manager_profile.first_name
        if search_item.item == 'facility':
            new['facility_list'] = list()
            for facility_index, facility_value in enumerate(search_item.text.split(",")):
                new['facility_list'].append(facility_value)
                if facility_index == 0:
                    if ReserveOfflineFacility.objects.filter(display_id=facility_value).exists():
                        new['facility_all'] = ReserveOfflineFacility.objects.filter(display_id=facility_value).first().name
                    if ReserveOnlineFacility.objects.filter(display_id=facility_value).exists():
                        new['facility_all'] = ReserveOnlineFacility.objects.filter(display_id=facility_value).first().name
                else:
                    if ReserveOfflineFacility.objects.filter(display_id=facility_value).exists():
                        new['facility_all'] = new['facility_all'] + ', ' + ReserveOfflineFacility.objects.filter(display_id=facility_value).first().name
                    if ReserveOnlineFacility.objects.filter(display_id=facility_value).exists():
                        new['facility_all'] = new['facility_all'] + ', ' + ReserveOnlineFacility.objects.filter(display_id=facility_value).first().name
        if search_item.item == 'place':
            new['place_list'] = list()
            for place_index, place_value in enumerate(search_item.text.split(",")):
                new['place_list'].append(place_value)
                if place_index == 0:
                    if ShopOffline.objects.filter(display_id=place_value).exists():
                        new['place_all'] = ShopOffline.objects.filter(display_id=place_value).first().name
                    if ShopOnline.objects.filter(display_id=place_value).exists():
                        new['place_all'] = ShopOnline.objects.filter(display_id=place_value).first().name
                else:
                    if ShopOffline.objects.filter(display_id=place_value).exists():
                        new['place_all'] = new['place_all'] + ', ' + ShopOffline.objects.filter(display_id=facility_value).first().name
                    if ShopOnline.objects.filter(display_id=place_value).exists():
                        new['place_all'] = new['place_all'] + ', ' + ShopOnline.objects.filter(display_id=facility_value).first().name
    
    after = {}
    for search_item in MiniTableSearch.objects.filter(url=request.path, company=company, shop=shop, manager=request.user, page='after').order_by('created_at').all():
        after[search_item.item] = search_item.text
        if search_item.item == 'age_from':
            if 'age' in after:
                after['age'] = search_item.text + after['age']
            else:
                after['age'] = search_item.text + ' ～ '
        if search_item.item == 'age_to':
            if 'age' in after:
                after['age'] = after['age'] + search_item.text
            else:
                after['age'] = ' ～ ' + search_item.text
        if search_item.item == 'datetime_from':
            if 'datetime' in after:
                after['datetime'] = search_item.text + after['datetime']
            else:
                after['datetime'] = search_item.text + ' ～ '
        if search_item.item == 'datetime_to':
            if 'datetime' in after:
                after['datetime'] = after['datetime'] + search_item.text
            else:
                after['datetime'] = ' ～ ' + search_item.text
        if search_item.item == 'create_from':
            if 'create' in after:
                after['create'] = search_item.text + after['create']
            else:
                after['create'] = search_item.text + ' ～ '
        if search_item.item == 'create_to':
            if 'create' in after:
                after['create'] = after['create'] + search_item.text
            else:
                after['create'] = ' ～ ' + search_item.text
        if search_item.item == 'flow':
            flow_list = list()
            for flow in HeadFlow.objects.order_by('-created_at').all():
                flow_tab_list = flow.description.split('→')
                for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
                    if flow_tab_index == 0:
                        if not 'ブロック' in flow_list:
                            flow_list.append('ブロック')
                    else:
                        flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                        if not flow_chart_name in flow_list:
                            flow_list.append(flow_chart_name)
            for flow_index, flow_value in enumerate(search_item.text.split(",")):
                if flow_index == 0:
                    after['flow_all'] = flow_list[int(flow_value)]
                else:
                    after['flow_all'] = after['flow_all'] + ', ' + flow_list[int(flow_value)]
        if search_item.item == 'manager':
            after['manager_list'] = list()
            for manager_index, manager_value in enumerate(search_item.text.split(",")):
                after['manager_list'].append(manager_value)
                manager_profile = ManagerProfile.objects.filter(manager=AuthUser.objects.filter(display_id=manager_value).first()).first()
                if manager_index == 0:
                    if AuthUser.objects.filter(display_id=manager_value).exists():
                        after['manager_all'] = manager_profile.family_name + manager_profile.first_name
                else:
                    if AuthUser.objects.filter(display_id=manager_value).exists():
                        after['manager_all'] = after['manager_all'] + ', ' + manager_profile.family_name + manager_profile.first_name
        if search_item.item == 'facility':
            after['facility_list'] = list()
            for facility_index, facility_value in enumerate(search_item.text.split(",")):
                after['facility_list'].append(facility_value)
                if facility_index == 0:
                    if ReserveOfflineFacility.objects.filter(display_id=facility_value).exists():
                        after['facility_all'] = ReserveOfflineFacility.objects.filter(display_id=facility_value).first().name
                    if ReserveOnlineFacility.objects.filter(display_id=facility_value).exists():
                        after['facility_all'] = ReserveOnlineFacility.objects.filter(display_id=facility_value).first().name
                else:
                    if ReserveOfflineFacility.objects.filter(display_id=facility_value).exists():
                        after['facility_all'] = after['facility_all'] + ', ' + ReserveOfflineFacility.objects.filter(display_id=facility_value).first().name
                    if ReserveOnlineFacility.objects.filter(display_id=facility_value).exists():
                        after['facility_all'] = after['facility_all'] + ', ' + ReserveOnlineFacility.objects.filter(display_id=facility_value).first().name
        if search_item.item == 'place':
            after['place_list'] = list()
            for place_index, place_value in enumerate(search_item.text.split(",")):
                after['place_list'].append(place_value)
                if place_index == 0:
                    if ShopOffline.objects.filter(display_id=place_value).exists():
                        after['place_all'] = ShopOffline.objects.filter(display_id=place_value).first().name
                    if ShopOnline.objects.filter(display_id=place_value).exists():
                        after['place_all'] = ShopOnline.objects.filter(display_id=place_value).first().name
                else:
                    if ShopOffline.objects.filter(display_id=place_value).exists():
                        after['place_all'] = after['place_all'] + ', ' + ShopOffline.objects.filter(display_id=facility_value).first().name
                    if ShopOnline.objects.filter(display_id=place_value).exists():
                        after['place_all'] = after['place_all'] + ', ' + ShopOnline.objects.filter(display_id=facility_value).first().name
    return {
        'today': today,
        'new': new,
        'after': after,
    }

def get_condition_data(shop, search):
    today = {}
    flow_list = list()
    for flow in HeadFlow.objects.order_by('-created_at').all():
        flow_tab_list = flow.description.split('→')
        for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
            if flow_tab_index != 0:
                flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                if not flow_chart_name in flow_list:
                    flow_list.append(flow_chart_name)
    today['flow_list'] = {}
    for flow_index, flow_item in enumerate(flow_list):
        if 'flow' in search['today'] and str(flow_index+1) in search['today']['flow']:
            today['flow_list'][flow_item] = True
        else:
            today['flow_list'][flow_item] = False
    today['manager_list'] = AuthUser.objects.filter(shop=shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all()
    for manager_index, manager_item in enumerate(today['manager_list']):
        if 'manager_list' in search['today'] and str(manager_item.display_id) in search['today']['manager_list']:
            today['manager_list'][manager_index].check = True
        else:
            today['manager_list'][manager_index].check = False
        today['manager_list'][manager_index].profile = ManagerProfile.objects.filter(manager_id=manager_item.id).first()
    today['facility_list'] = list()
    today['place_list'] = list()
    for online_offline_item in list(chain(ShopOffline.objects.filter(shop=shop).order_by('created_at').all(), ShopOnline.objects.filter(shop=shop).order_by('created_at').all())):
        today['place_list'].append(online_offline_item)
        if ShopOffline.objects.filter(id=online_offline_item.id).exists():
            for facility_index, facility_item in enumerate(ReserveOfflineFacility.objects.filter(offline=online_offline_item).order_by('number').all()):
                today['facility_list'].append(facility_item)
                if 'facility_list' in search['today'] and str(facility_item.display_id) in search['today']['facility_list']:
                    today['facility_list'][facility_index].check = True
                else:
                    today['facility_list'][facility_index].check = False
        if ShopOnline.objects.filter(id=online_offline_item.id).exists():
            for facility_item in ReserveOnlineFacility.objects.filter(online=online_offline_item).order_by('number').all():
                today['facility_list'].append(facility_item)
                if 'facility_list' in search['today'] and str(facility_item.display_id) in search['today']['facility_list']:
                    today['facility_list'][facility_index].check = True
                else:
                    today['facility_list'][facility_index].check = False
    
    new = {}
    flow_list = list()
    for flow in HeadFlow.objects.order_by('-created_at').all():
        flow_tab_list = flow.description.split('→')
        for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
            if flow_tab_index != 0:
                flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                if not flow_chart_name in flow_list:
                    flow_list.append(flow_chart_name)
    new['flow_list'] = {}
    for flow_index, flow_item in enumerate(flow_list):
        if 'flow' in search['new'] and str(flow_index+1) in search['new']['flow']:
            new['flow_list'][flow_item] = True
        else:
            new['flow_list'][flow_item] = False
    new['manager_list'] = AuthUser.objects.filter(shop=shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all()
    for manager_index, manager_item in enumerate(new['manager_list']):
        if 'manager_list' in search['new'] and str(manager_item.display_id) in search['new']['manager_list']:
            new['manager_list'][manager_index].check = True
        else:
            new['manager_list'][manager_index].check = False
        new['manager_list'][manager_index].profile = ManagerProfile.objects.filter(manager_id=manager_item.id).first()
    new['facility_list'] = list()
    new['place_list'] = list()
    for online_offline_item in list(chain(ShopOffline.objects.filter(shop=shop).order_by('created_at').all(), ShopOnline.objects.filter(shop=shop).order_by('created_at').all())):
        new['place_list'].append(online_offline_item)
        if ShopOffline.objects.filter(id=online_offline_item.id).exists():
            for facility_index, facility_item in enumerate(ReserveOfflineFacility.objects.filter(offline=online_offline_item).order_by('number').all()):
                new['facility_list'].append(facility_item)
                if 'facility_list' in search['new'] and str(facility_item.display_id) in search['new']['facility_list']:
                    new['facility_list'][facility_index].check = True
                else:
                    new['facility_list'][facility_index].check = False
        if ShopOnline.objects.filter(id=online_offline_item.id).exists():
            for facility_item in ReserveOnlineFacility.objects.filter(online=online_offline_item).order_by('number').all():
                new['facility_list'].append(facility_item)
                if 'facility_list' in search['new'] and str(facility_item.display_id) in search['new']['facility_list']:
                    new['facility_list'][facility_index].check = True
                else:
                    new['facility_list'][facility_index].check = False
    
    after = {}
    flow_list = list()
    for flow in HeadFlow.objects.order_by('-created_at').all():
        flow_tab_list = flow.description.split('→')
        for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
            if flow_tab_index != 0:
                flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                if not flow_chart_name in flow_list:
                    flow_list.append(flow_chart_name)
    after['flow_list'] = {}
    for flow_index, flow_item in enumerate(flow_list):
        if 'flow' in search['after'] and str(flow_index+1) in search['after']['flow']:
            after['flow_list'][flow_item] = True
        else:
            after['flow_list'][flow_item] = False
    after['manager_list'] = AuthUser.objects.filter(shop=shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all()
    for manager_index, manager_item in enumerate(after['manager_list']):
        if 'manager_list' in search['after'] and str(manager_item.display_id) in search['after']['manager_list']:
            after['manager_list'][manager_index].check = True
        else:
            after['manager_list'][manager_index].check = False
        after['manager_list'][manager_index].profile = ManagerProfile.objects.filter(manager_id=manager_item.id).first()
    after['facility_list'] = list()
    after['place_list'] = list()
    for online_offline_item in list(chain(ShopOffline.objects.filter(shop=shop).order_by('created_at').all(), ShopOnline.objects.filter(shop=shop).order_by('created_at').all())):
        after['place_list'].append(online_offline_item)
        if ShopOffline.objects.filter(id=online_offline_item.id).exists():
            for facility_index, facility_item in enumerate(ReserveOfflineFacility.objects.filter(offline=online_offline_item).order_by('number').all()):
                after['facility_list'].append(facility_item)
                if 'facility_list' in search['after'] and str(facility_item.display_id) in search['after']['facility_list']:
                    after['facility_list'][facility_index].check = True
                else:
                    after['facility_list'][facility_index].check = False
        if ShopOnline.objects.filter(id=online_offline_item.id).exists():
            for facility_item in ReserveOnlineFacility.objects.filter(online=online_offline_item).order_by('number').all():
                after['facility_list'].append(facility_item)
                if 'facility_list' in search['after'] and str(facility_item.display_id) in search['after']['facility_list']:
                    after['facility_list'][facility_index].check = True
                else:
                    after['facility_list'][facility_index].check = False

    return {
        'today': today,
        'new': new,
        'after': after,
    }



def get_query_data(request, company, shop, page):
    query = Q()
    search = MiniTableSearch.objects.filter(url=request.path, company=company, shop=shop, manager=request.user, page=page).all()
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
        elif search_item.item == 'line':
            if search_item.text == '1':
                search_query.add(Q(**{'flow__user__proxy_flg': False}), Q.AND)
            elif search_item.text == '2':
                search_query.add(Q(**{'flow__user__proxy_flg': True}), Q.AND)
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
    date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
    if schedule.online:
        add_date = date + datetime.timedelta(minutes=schedule.online.time)
    elif schedule.offline:
        add_date = date + datetime.timedelta(minutes=schedule.offline.time)
    if schedule.date.weekday() == 0:
        week = '(月)'
    elif schedule.date.weekday() == 1:
        week = '(火)'
    elif schedule.date.weekday() == 2:
        week = '(水)'
    elif schedule.date.weekday() == 3:
        week = '(木)'
    elif schedule.date.weekday() == 4:
        week = '(金)'
    elif schedule.date.weekday() == 5:
        week = '(土)'
    elif schedule.date.weekday() == 6:
        week = '(日)'
    reserve_data = str(date.month) + '/' + str(date.day) + week + ' ' + str(date.hour) + ':' + str(date.minute).zfill(2) + '～' + str(add_date.hour) + ':' + str(add_date.minute).zfill(2)
    return reserve_data