
from view import ShopView

from reception.models import ReceptionData, ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager
from setting.models import ShopOffline, ShopOnline, ShopOfflineTime, ShopOnlineTime
from sign.models import AuthLogin, AuthUser, ManagerProfile

from dateutil.relativedelta import relativedelta
from itertools import chain

import calendar
import datetime
import jpholiday

class IndexView(ShopView):
    template_name = 'reception/index.html'
    title = '毎月の受付設定'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['reception'] = ReceptionData.objects.filter(shop=auth_login.shop).first()

        current = datetime.date.today().replace(day=1)
        context['month_list'] = list()
        for i in range(4):
            context['month_list'].append(current + relativedelta(months=(i-1)))
        
        agenda = calendar.Calendar(6)
        context['days_count_list'] = list()
        for month_item in context['month_list']:
            days = agenda.monthdatescalendar(month_item.year, month_item.month)
            days_count = 0
            for week in days:
                week_list = list()
                for day in week:
                    if day.month == month_item.month:
                        days_count = days_count + 1
            context['days_count_list'].append(days_count)
        
        context['offline_list'] = ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for offline_index, offline_item in enumerate(context['offline_list']):
            context['offline_list'][offline_index].type = 1
            context['offline_list'][offline_index].time = ShopOfflineTime.objects.filter(offline=offline_item).order_by('week').all()
        context['online_list'] = ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for online_index, online_item in enumerate(context['online_list']):
            context['online_list'][online_index].type = 2
            context['online_list'][online_index].time = ShopOnlineTime.objects.filter(online=online_item).order_by('week').all()
        context['online_offline_list'] = list(chain(context['offline_list'], context['online_list']))
        for online_offline_index, online_offline_item in enumerate(context['online_offline_list']):
            context['online_offline_list'][online_offline_index].month = list()
            for month_index, month_item in enumerate(context['month_list']):
                reception_count = 0
                reception_status = None
                days = agenda.monthdatescalendar(month_item.year, month_item.month)
                for week in days:
                    for day in week:
                        if day.month == month_item.month:
                            if ShopOffline.objects.filter(id=online_offline_item.id).exists():
                                if ReceptionOfflinePlace.objects.filter(offline=online_offline_item, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day, number=1).exists():
                                    reception_count = reception_count + 1
                            if ShopOnline.objects.filter(id=online_offline_item.id).exists():
                                if ReceptionOnlinePlace.objects.filter(online=online_offline_item, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day, number=1).exists():
                                    reception_count = reception_count + 1
                if reception_count == 0:
                    reception_status = 0
                elif reception_count < context['days_count_list'][month_index]:
                    reception_status = 2
                else:
                    reception_status = 1
                context['online_offline_list'][online_offline_index].month.append({
                    'year': month_item.year,
                    'month': month_item.month,
                    'status': reception_status,
                })
        
        context['manager_list'] = list()
        for month_index, month_item in enumerate(context['month_list']):
            reception_status = None
            for online_offline_item in context['online_offline_list']:
                for manager_item in AuthUser.objects.filter(shop=auth_login.shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all():
                    reception_count = 0
                    days = agenda.monthdatescalendar(month_item.year, month_item.month)
                    for week in days:
                        for day in week:
                            if day.month == month_item.month:
                                if ShopOffline.objects.filter(id=online_offline_item.id).exists():
                                    if ReceptionOfflineManager.objects.filter(offline=online_offline_item, manager=manager_item, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).exists():
                                        reception_count = reception_count + 1
                                if ShopOnline.objects.filter(id=online_offline_item.id).exists():
                                    if ReceptionOnlineManager.objects.filter(online=online_offline_item, manager=manager_item, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).exists():
                                        reception_count = reception_count + 1
                    if reception_count == 0:
                        if reception_status:
                            if reception_status == 1 or reception_status == 2:
                                reception_status = 2
                                break
                            else:
                                reception_status = 0
                        else:
                            reception_status = 0
                    elif reception_count < context['days_count_list'][month_index]:
                        reception_status = 2
                        break
                    else:
                        if reception_status:
                            if reception_status == 1:
                                reception_status = 1
                            else:
                                reception_status = 2
                                break
                        else:
                            reception_status = 1
                        reception_status = 1
                if reception_status == 2:
                    break
            context['manager_list'].append({
                'year': month_item.year,
                'month': month_item.month,
                'status': reception_status,
            })
        
        return context

class PlaceView(ShopView):
    template_name = 'reception/place.html'
    title = '会場の受付設定'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['date'] = datetime.date(int(self.request.GET.get("year")), int(self.request.GET.get("month")), 1)
        if context['date'].month == 1:
            context['prev'] = context['date'].replace(year=context['date'].year-1, month=12, day=1)
        else:
            context['prev'] = context['date'].replace(month=context['date'].month-1, day=1)
        if context['date'].month == 12:
            context['next'] = context['date'].replace(year=context['date'].year+1, month=1, day=1)
        else:
            context['next'] = context['date'].replace(month=context['date'].month+1, day=1)

        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        if ShopOffline.objects.filter(display_id=self.request.GET.get("id")).first():
            context['setting'] = ShopOffline.objects.filter(display_id=self.request.GET.get("id")).first()
        if ShopOnline.objects.filter(display_id=self.request.GET.get("id")).first():
            context['setting'] = ShopOnline.objects.filter(display_id=self.request.GET.get("id")).first()
        context['offline_list'] = ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for offline_index, offline_item in enumerate(context['offline_list']):
            context['offline_list'][offline_index].type = 1
            context['offline_list'][offline_index].time = ShopOfflineTime.objects.filter(offline=offline_item).order_by('week').all()
        context['online_list'] = ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for online_index, online_item in enumerate(context['online_list']):
            context['online_list'][online_index].type = 2
            context['online_list'][online_index].time = ShopOnlineTime.objects.filter(online=online_item).order_by('week').all()
        context['online_offline_list'] = list(chain(context['offline_list'], context['online_list']))

        agenda = calendar.Calendar(6)
        context['days'] = agenda.monthdatescalendar(context['date'].year, context['date'].month)

        context['holiday'] = []
        holidays = jpholiday.month_holidays(context['date'].year, context['date'].month)
        for holidays_item in holidays:
            context['holiday'].append(str(holidays_item[0].month) + '/' + str(holidays_item[0].day))
        holidays = jpholiday.month_holidays(context['prev'].year, context['prev'].month)
        for holidays_item in holidays:
            context['holiday'].append(str(holidays_item[0].month) + '/' + str(holidays_item[0].day))
        holidays = jpholiday.month_holidays(context['next'].year, context['next'].month)
        for holidays_item in holidays:
            context['holiday'].append(str(holidays_item[0].month) + '/' + str(holidays_item[0].day))
        
        context['days_count'] = 0
        if ShopOffline.objects.filter(display_id=self.request.GET.get("id")).first():
            context['reception_count'] = ReceptionOfflinePlace.objects.filter(offline=context['setting'], reception_date__year=context['date'].year, reception_date__month=context['date'].month, number=1).count()
        if ShopOnline.objects.filter(display_id=self.request.GET.get("id")).first():
            context['reception_count'] = ReceptionOnlinePlace.objects.filter(online=context['setting'], reception_date__year=context['date'].year, reception_date__month=context['date'].month, number=1).count()
        context['reception_list'] = list()
        for week in context['days']:
            week_list = list()
            for day in week:
                if day.month == context['date'].month:
                    if ShopOffline.objects.filter(display_id=self.request.GET.get("id")).first():
                        reception = ReceptionOfflinePlace.objects.filter(offline=context['setting'], reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).first()
                    if ShopOnline.objects.filter(display_id=self.request.GET.get("id")).first():
                        reception = ReceptionOnlinePlace.objects.filter(online=context['setting'], reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).first()
                    if reception:
                        reception_time = list()
                        if ShopOffline.objects.filter(display_id=self.request.GET.get("id")).first():
                            for reception_place in ReceptionOfflinePlace.objects.filter(offline=context['setting'], reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).order_by('number').all():
                                reception_time.append({
                                    'number': reception_place.number,
                                    'from': reception_place.reception_from,
                                    'to': reception_place.reception_to,
                                })
                        if ShopOnline.objects.filter(display_id=self.request.GET.get("id")).first():
                            for reception_place in ReceptionOnlinePlace.objects.filter(online=context['setting'], reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).order_by('number').all():
                                reception_time.append({
                                    'number': reception_place.number,
                                    'from': reception_place.reception_from,
                                    'to': reception_place.reception_to,
                                })
                        week_list.append({
                            'year': day.year,
                            'month': day.month,
                            'day': day.day,
                            'time': reception_time,
                            'count': reception.reception_count,
                            'flg': reception.reception_flg,
                        })
                    else:
                        week_list.append({
                            'year': day.year,
                            'month': day.month,
                            'day': day.day,
                            'time': None,
                            'count': None,
                            'flg': None,
                        })
                    context['days_count'] = context['days_count'] + 1
                else:
                    week_list.append({
                        'year': day.year,
                        'month': day.month,
                        'day': day.day,
                        'time': None,
                        'count': None,
                        'flg': None,
                    })
            context['reception_list'].append(week_list)

        return context

class ManagerView(ShopView):
    template_name = 'reception/manager.html'
    title = 'スタッフの受付設定'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['date'] = datetime.date(int(self.request.GET.get("year")), int(self.request.GET.get("month")), 1)
        if context['date'].month == 1:
            context['prev'] = context['date'].replace(year=context['date'].year-1, month=12, day=1)
        else:
            context['prev'] = context['date'].replace(month=context['date'].month-1, day=1)
        if context['date'].month == 12:
            context['next'] = context['date'].replace(year=context['date'].year+1, month=1, day=1)
        else:
            context['next'] = context['date'].replace(month=context['date'].month+1, day=1)
        
        agenda = calendar.Calendar(6)
        context['days'] = agenda.monthdatescalendar(context['date'].year, context['date'].month)
        context['days_count'] = 0
        for week in context['days']:
            for day in week:
                if day.month == context['date'].month:
                    context['days_count'] = context['days_count'] + 1
        
        context['holiday'] = []
        holidays = jpholiday.month_holidays(context['date'].year, context['date'].month)
        for holidays_item in holidays:
            context['holiday'].append(str(holidays_item[0].month) + '/' + str(holidays_item[0].day))
        holidays = jpholiday.month_holidays(context['prev'].year, context['prev'].month)
        for holidays_item in holidays:
            context['holiday'].append(str(holidays_item[0].month) + '/' + str(holidays_item[0].day))
        holidays = jpholiday.month_holidays(context['next'].year, context['next'].month)
        for holidays_item in holidays:
            context['holiday'].append(str(holidays_item[0].month) + '/' + str(holidays_item[0].day))
        
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['manager_list'] = AuthUser.objects.filter(shop=auth_login.shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all()
        for manager_index, manager_value in enumerate(context['manager_list']):
            context['manager_list'][manager_index].profile = ManagerProfile.objects.filter(manager=manager_value).first()

        if ShopOffline.objects.filter(display_id=self.request.GET.get("id")).first():
            context['setting'] = ShopOffline.objects.filter(display_id=self.request.GET.get("id")).first()
        if ShopOnline.objects.filter(display_id=self.request.GET.get("id")).first():
            context['setting'] = ShopOnline.objects.filter(display_id=self.request.GET.get("id")).first()
        context['offline_list'] = ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for offline_index, offline_item in enumerate(context['offline_list']):
            context['offline_list'][offline_index].type = 1
            context['offline_list'][offline_index].time = ShopOfflineTime.objects.filter(offline=offline_item).order_by('week').all()
        context['online_list'] = ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for online_index, online_item in enumerate(context['online_list']):
            context['online_list'][online_index].type = 2
            context['online_list'][online_index].time = ShopOnlineTime.objects.filter(online=online_item).order_by('week').all()
        context['online_offline_list'] = list(chain(context['offline_list'], context['online_list']))

        for online_offline_index, online_offline_item in enumerate(context['online_offline_list']):
            context['online_offline_list'][online_offline_index].manager = AuthUser.objects.filter(shop=auth_login.shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all()
            for manager_index, manager_item in enumerate(context['online_offline_list'][online_offline_index].manager):
                context['online_offline_list'][online_offline_index].manager[manager_index].profile = ManagerProfile.objects.filter(manager_id=manager_item.id).first()
                context['online_offline_list'][online_offline_index].manager[manager_index].reception_list = list()
                context['online_offline_list'][online_offline_index].manager[manager_index].reception_count = 0
                for week in context['days']:
                    for day_index, day in enumerate(week):
                        if day.month == context['date'].month:
                            reception_list = list()
                            if ShopOffline.objects.filter(display_id=self.request.GET.get("id")).first():
                                reception_list = ReceptionOfflineManager.objects.filter(offline=online_offline_item, manager=manager_item, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).order_by('number').all()
                            if ShopOnline.objects.filter(display_id=self.request.GET.get("id")).first():
                                reception_list = ReceptionOnlineManager.objects.filter(online=online_offline_item, manager=manager_item, reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).order_by('number').all()
                            if len(reception_list) > 0:
                                time_list = list()
                                for reception in reception_list:
                                    time_list.append({
                                        'number': reception.number,
                                        'from': reception.reception_from,
                                        'to': reception.reception_to,
                                    })
                                context['online_offline_list'][online_offline_index].manager[manager_index].reception_list.append({
                                    'year': day.year,
                                    'month': day.month,
                                    'day': day.day,
                                    'week': day_index + 1,
                                    'time': time_list,
                                    'flg': reception.reception_flg,
                                })
                                context['online_offline_list'][online_offline_index].manager[manager_index].reception_count = context['online_offline_list'][online_offline_index].manager[manager_index].reception_count + 1
                            else:
                                context['online_offline_list'][online_offline_index].manager[manager_index].reception_list.append({
                                    'year': day.year,
                                    'month': day.month,
                                    'day': day.day,
                                    'week': day_index + 1,
                                    'time': list(),
                                    'flg': None,
                                })

        return context