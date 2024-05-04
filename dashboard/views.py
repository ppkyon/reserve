from django.db import models
from django.shortcuts import redirect

from view import ShopView

from flow.models import UserFlowSchedule
from sign.models import AuthLogin
from talk.models import TalkRead
from user.models import LineUser, UserProfile

import datetime

class IndexView(ShopView):
    def get(self, request, **kwargs):
        return redirect('/dashboard/')

class DashboardView(ShopView):
    template_name = 'dashboard/index.html'
    title = 'ダッシュボード'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        
        now = datetime.datetime.now()
        after = now + datetime.timedelta(days=1)
        context['today_user_count'] = LineUser.objects.filter(shop=auth_login.shop, created_at__range=(now.replace(hour=0, minute=0, second=0, microsecond=0), now.replace(hour=23, minute=59, second=59, microsecond=0)), delete_flg=False).count()

        context['today_reserve_count'] = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0)).exclude(join=2).count()
        context['today_reserve_list'] = list()
        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date=now.replace(hour=0, minute=0, second=0, microsecond=0)).exclude(join=2).all():
            if schedule.date:
                schedule.flow.user.profile = UserProfile.objects.filter(user=schedule.flow.user).first()
                schedule.flow.user.flow = schedule.flow
                schedule.flow.user.schedule = schedule
                schedule.flow.user.reserve = get_reserve_date(schedule)
                context['today_reserve_list'].append(schedule.flow.user)

        context['new_reserve_count'] = UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, created_at__range=(now.replace(hour=0, minute=0, second=0, microsecond=0), now.replace(hour=23, minute=59, second=59, microsecond=0)), check_flg=False).exclude(join=2).count()
        context['new_reserve_list'] = list()
        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, created_at__range=(now.replace(hour=0, minute=0, second=0, microsecond=0), now.replace(hour=23, minute=59, second=59, microsecond=0)), check_flg=False).exclude(join=2).all():
            if schedule.date:
                schedule.flow.user.profile = UserProfile.objects.filter(user=schedule.flow.user).first()
                schedule.flow.user.flow = schedule.flow
                schedule.flow.user.schedule = schedule
                schedule.flow.user.reserve = get_reserve_date(schedule)

                if schedule.number > 1:
                    prev_schedule = UserFlowSchedule.objects.filter(flow=schedule.flow, number=schedule.number-1).first()
                    if prev_schedule and prev_schedule.date:
                        schedule.flow.user.reserve = get_reserve_date(prev_schedule) + ' → ' + schedule.flow.user.reserve

                context['new_reserve_list'].append(schedule.flow.user)

        context['after_reserve_list'] = list()
        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__gte=after.replace(hour=0, minute=0, second=0, microsecond=0)).exclude(join=2).all():
            if schedule.date:
                schedule.flow.user.profile = UserProfile.objects.filter(user=schedule.flow.user).first()
                schedule.flow.user.flow = schedule.flow
                schedule.flow.user.schedule = schedule
                schedule.flow.user.reserve = get_reserve_date(schedule)
                context['after_reserve_list'].append(schedule.flow.user)

        context['new_line_list'] = list()
        for user in LineUser.objects.filter(shop=auth_login.shop, member_flg=False, proxy_flg=False, check_flg=False, delete_flg=False).all():
            user.profile = UserProfile.objects.filter(user=user).first()
            context['new_line_list'].append(user)

        context['message_required_count'] = 0
        talk_read = TalkRead.objects.filter(user__delete_flg=False, manager=self.request.user, user__talk_manager__manager=self.request.user, user__talk_status__status=1).aggregate(sum_read_count=models.Sum('read_count'))
        if talk_read and talk_read['sum_read_count']:
            context['message_required_count'] = talk_read['sum_read_count']
        return context



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