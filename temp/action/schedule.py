from django.db.models import Q
from django.http import JsonResponse

from flow.models import ShopFlowTab, UserFlow, UserFlowSchedule
from reception.models import (
    ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
)
from reserve.models import (
    ReserveBasic, ReserveOfflineSetting, ReserveOnlineSetting, ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflineFacility, ReserveOnlineFacility, ReserveStartDate, ReserveUserStartDate,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu, ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
)
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthLogin, AuthUser, ManagerProfile
from user.models import LineUser

from common import create_code, get_model_field

import calendar
import datetime
import pandas
import uuid

def get(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(display_id=request.POST.get('user_id'), shop=auth_login.shop).first()

    setting = None
    if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).values(*get_model_field(ReserveOfflineSetting)).first()
        setting['type'] = 1
    elif ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).values(*get_model_field(ReserveOnlineSetting)).first()
        setting['type'] = 2
    
    course = None
    if request.POST.get('course_id'):
        if setting['type'] == 1:
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
        elif setting['type'] == 2:
            course = ReserveOnlineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
    if course:
        course_data = course
    else:
        course_data = ReserveBasic.objects.filter(shop=auth_login.shop).first()
        
    if request.POST.get("year") and request.POST.get("month") and request.POST.get("day"):
        current = datetime.datetime(int(request.POST.get("year")), int(request.POST.get("month")), int(request.POST.get("day")))
    else:
        current = datetime.datetime.now()
        if setting['type'] == 1:
            user_start_date = ReserveUserStartDate.objects.filter(user=user, offline__id=setting['id']).first()
            if user_start_date:
                now = datetime.datetime.now()
                if user_start_date.date and now <= user_start_date.date:
                    current = user_start_date.date
            else:
                if course:
                    reserve_start_date = ReserveStartDate.objects.filter(offline__id=setting['id'], offline_course=course).first()
                    if reserve_start_date:
                        now = datetime.datetime.now()
                        if reserve_start_date.first_date and now <= reserve_start_date.first_date:
                            current = reserve_start_date.first_date
                        elif reserve_start_date.second_date:
                            current = reserve_start_date.second_date
                else:
                    reserve_start_date = ReserveStartDate.objects.filter(offline__id=setting['id'], offline_course=None).first()
                    if reserve_start_date:
                        now = datetime.datetime.now()
                        if reserve_start_date.first_date and now <= reserve_start_date.first_date:
                            current = reserve_start_date.first_date
                        elif reserve_start_date.second_date:
                            current = reserve_start_date.second_date
        elif setting['type'] == 2:
            user_start_date = ReserveUserStartDate.objects.filter(user=user, online__id=setting['id']).first()
            if user_start_date:
                now = datetime.datetime.now()
                if user_start_date.date and now <= user_start_date.date:
                    current = user_start_date.date
            else:
                if course:
                    reserve_start_date = ReserveStartDate.objects.filter(online__id=setting['id'], online_course=course).first()
                    if reserve_start_date:
                        now = datetime.datetime.now()
                        if reserve_start_date.first_date and now <= reserve_start_date.first_date:
                            current = reserve_start_date.first_date
                        elif reserve_start_date.second_date:
                            current = reserve_start_date.second_date
                else:
                    reserve_start_date = ReserveStartDate.objects.filter(online__id=setting['id'], online_course=None).first()
                    if reserve_start_date:
                        now = datetime.datetime.now()
                        if reserve_start_date.first_date and now <= reserve_start_date.first_date:
                            current = reserve_start_date.first_date
                        elif reserve_start_date.second_date:
                            current = reserve_start_date.second_date
    prev = current - datetime.timedelta(days=14)
    next = current + datetime.timedelta(days=14)

    days = None
    week_day = list()
    week_flg = False
    for week in calendar.Calendar().monthdatescalendar(current.year, current.month):
        if week_flg:
            days = days + week
            week_flg = False
        if current.date() in week:
            days = week
            week_flg = True
    if week_flg:
        current_next = current + datetime.timedelta(days=7)
        for week in calendar.Calendar().monthdatescalendar(current_next.year, current_next.month):
            if current_next.date() in week:
                days = days + week
                week_flg = False
    
    online_offline = None
    manager_list = list()
    facility_list = list()
    if setting:
        if setting['type'] == 1:
            for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline__id=setting['id']).all():
                manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline__id=setting['id']).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)
            online_offline = ShopOffline.objects.filter(id=setting['offline']).values(*get_model_field(ShopOffline)).first()
        elif setting['type'] == 2:
            for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online__id=setting['id']).all():
                manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online__id=setting['id']).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)
            online_offline = ShopOnline.objects.filter(id=setting['online']).values(*get_model_field(ShopOnline)).first()

    time = {
        'from': None,
        'to': None
    }
    for day in days:
        if setting['type'] == 1:
            reception = ReceptionOfflinePlace.objects.filter(offline__id=online_offline['id'], reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).all()
        elif setting['type'] == 2:
            reception = ReceptionOnlinePlace.objects.filter(online__id=online_offline['id'], reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).all()
        if len(reception) == 0:
            reception_from = None
            reception_to = None
            reception_flg = True
        else:
            for reception_item in reception:
                if not reception_item.reception_flg:
                    if not time['from'] or ( reception_item.reception_from and time['from'] > reception_item.reception_from ):
                        time['from'] = reception_item.reception_from
                    if not time['to'] or ( reception_item.reception_to and time['to'] < reception_item.reception_to ):
                        time['to'] = reception_item.reception_to
                reception_from = time['from']
                reception_to = time['to']
                reception_flg = reception_item.reception_flg
        week_day.append({
            'year': day.year,
            'month': day.month,
            'day': day.day,
            'reception_from': reception_from,
            'reception_to': reception_to,
            'reception_flg': reception_flg,
        })

        if not reception_flg:
            if not time['from'] or ( reception_from and time['from'] > reception_from ):
                time['from'] = reception_from
            if not time['to'] or ( reception_to and time['to'] < reception_to ):
                time['to'] = reception_to
    
    reserve_data = ReserveBasic.objects.filter(shop=auth_login.shop).first()
    send_schedule = list()
    reception_data = list()
    week_schedule = list()
    week_time = list()
    unit_time = '60min'
    if setting['unit']:
        if setting['unit'] == 60:
            unit_time = '60min'
        elif setting['unit'] == 30:
            unit_time = '30min'
        elif setting['unit'] == 15:
            unit_time = '15min'
    elif reserve_data:
        if reserve_data.unit == 60:
            unit_time = '60min'
        elif reserve_data.unit == 30:
            unit_time = '30min'
        elif reserve_data.unit == 15:
            unit_time = '15min'
    if time['from'] and time['to']:
        for times in pandas.date_range(start=datetime.datetime(current.year, current.month, current.day, time['from'].hour, time['from'].minute, 0), end=datetime.datetime(current.year, current.month, current.day, time['to'].hour, time['to'].minute, 0), freq='15min'):
            schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
            week_time.append({
                'time': schedule_time
            })
            week_schedule.append({
                'week': week_day,
                'time': schedule_time,
            })

            for schedule_week_value in week_day:
                for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=schedule_week_value['year'], date__month=schedule_week_value['month'], date__day=schedule_week_value['day'], time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
                    if schedule.join == 0 or schedule.join == 1:
                        date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                        end_flg = False
                        if schedule.flow:
                            end_flg = schedule.flow.end_flg
                        if schedule.online:
                            reception_data.append({
                                'from': date,
                                'to': date + datetime.timedelta(minutes=schedule.online.time),
                                'setting': schedule.online,
                                'course': schedule.online_course,
                                'facility': schedule.online_facility,
                                'manager': schedule.manager,
                                'question': schedule.question,
                                'meeting': schedule.meeting,
                                'end_flg': end_flg,
                            })
                        elif schedule.offline:
                            reception_data.append({
                                'from': date,
                                'to': date + datetime.timedelta(minutes=schedule.offline.time),
                                'setting': schedule.offline,
                                'course': schedule.offline_course,
                                'facility': schedule.offline_facility,
                                'manager': schedule.manager,
                                'question': schedule.question,
                                'meeting': None,
                                'end_flg': end_flg,
                            })

        for times in pandas.date_range(start=datetime.datetime(current.year, current.month, current.day, time['from'].hour, time['from'].minute, 0), end=datetime.datetime(current.year, current.month, current.day, time['to'].hour, time['to'].minute, 0), freq=unit_time):
            schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
            send_week = list()
            for schedule_week_value in week_day:
                reception_flg = True
                manager_count = len(manager_list)
                facility_count = len(facility_list)
                reception_manager_list = list()
                reception_facility_list = list()
                for manager in manager_list:
                    schedule_datetime = datetime.datetime(schedule_week_value['year'], schedule_week_value['month'], schedule_week_value['day'], int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                    schedule_datetime = schedule_datetime + datetime.timedelta(minutes=setting['time'])
                    if setting['type'] == 1:
                        reception_place = ReceptionOfflinePlace.objects.filter(offline__id=online_offline['id'], reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=False).first()
                        reception_manager = ReceptionOfflineManager.objects.filter(offline__id=online_offline['id'], manager=manager, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                            if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline__id=setting['id']).exists():
                                reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline__id=setting['id']).first()
                                if not reception_offline_manager_setting.flg:
                                    reception_manager = None
                    if setting['type'] == 2:
                        reception_place = ReceptionOnlinePlace.objects.filter(online__id=online_offline['id'], reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=False).first()
                        reception_manager = ReceptionOnlineManager.objects.filter(online__id=online_offline['id'], manager=manager, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                            if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online__id=setting['id']).exists():
                                reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online__id=setting['id']).first()
                                if not reception_online_manager_setting.flg:
                                    reception_manager = None

                    if reception_place and reception_manager and schedule_week_value['day'] == schedule_datetime.day:
                        if len(reception_data) > 0 :
                            people_number = 0
                            people_count = setting['people']
                            same_count = setting['facility']

                            schedule_date = datetime.datetime(schedule_week_value['year'], schedule_week_value['month'], schedule_week_value['day'], int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                            schedule_add_date = schedule_date + datetime.timedelta(minutes=setting['time'])

                            count_flg = True
                            for reception in reception_data:
                                if schedule_add_date > reception['from'] and reception['to'] > schedule_date:
                                    if manager_count <= 0 or facility_count <= 0:
                                        break
                                    else:
                                        if reception['setting']:
                                            if reception['setting'].id == setting['id']:
                                                if schedule_date == reception['from']:
                                                    if count_flg:
                                                        if reception['facility'] and reception['facility'].count < people_count:
                                                            same_count = same_count - 1
                                                            if same_count == 0:
                                                                if people_count > reception['facility'].count:
                                                                    people_count = reception['facility'].count
                                                            else:
                                                                people_total_count = reception['facility'].count
                                                                while same_count > 0:
                                                                    people_number = people_number + 1
                                                                    people_total_count = people_total_count + facility_list[people_number].count
                                                                    if facility_list[people_number] and not facility_list[people_number] in reception_facility_list:
                                                                        facility_count = facility_count - 1
                                                                        reception_facility_list.append(facility_list[people_number])
                                                                    same_count = same_count - 1
                                                                if people_count > people_total_count:
                                                                    people_count = people_total_count
                                                        count_flg = False
                                                    people_count = people_count - 1
                                                    if people_count <= 0:
                                                        if reception['manager'] and not reception['manager'] in reception_manager_list:
                                                            manager_count = manager_count - 1
                                                            reception_manager_list.append(reception['manager'])
                                                        if reception['facility'] and not reception['facility'] in reception_facility_list:
                                                            facility_count = facility_count - 1
                                                            reception_facility_list.append(reception['facility'])

                                                        people_number = people_number + 1
                                                        people_count = setting['people']
                                                        if facility_count > 0 and facility_list[people_number].count < people_count:
                                                            people_count = facility_list[people_number].count
                                                else:
                                                    if reception['manager'] and not reception['manager'] in reception_manager_list:
                                                        manager_count = manager_count - 1
                                                        reception_manager_list.append(reception['manager'])
                                                    if reception['facility'] and not reception['facility'] in reception_facility_list:
                                                        facility_count = facility_count - 1
                                                        reception_facility_list.append(reception['facility'])
                                            else:
                                                if reception['manager'] and not reception['manager'] in reception_manager_list:
                                                    manager_count = manager_count - 1
                                                    reception_manager_list.append(reception['manager'])
                                                if reception['facility'] and not reception['facility'] in reception_facility_list:
                                                    facility_count = facility_count - 1
                                                    reception_facility_list.append(reception['facility'])
                            if manager_count > 0 and facility_count > 0:
                                reception_flg = False
                        else:
                            schedule_date = datetime.datetime(schedule_week_value['year'], schedule_week_value['month'], schedule_week_value['day'], int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                            if manager_count > 0 and facility_count > 0:
                                reception_flg = False
                    else:
                        if not manager in reception_manager_list:
                            manager_count = manager_count - 1
                            reception_manager_list.append(manager)
                
                if manager_count <= 0 or facility_count <= 0:
                    reception_flg = True
                send_week.append({
                    'year': schedule_week_value['year'],
                    'month': schedule_week_value['month'],
                    'day': schedule_week_value['day'],
                    'reception_flg': reception_flg,
                })
            add_time = datetime.datetime(schedule_week_value['year'], schedule_week_value['month'], schedule_week_value['day'], int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0) + datetime.timedelta(minutes=setting['time'])
            send_schedule.append({
                'week': send_week,
                'time': schedule_time,
                'add_time': str(add_time.hour) + ':' + str(add_time.minute).ljust(2, '0'),
            })
    
    start_date = datetime.datetime.now()
    if course_data:
        if course_data.deadline == 1 and course_data.on_time and course_data.on_time != 0 and course_data.on_time != 1:
            start_date = start_date + datetime.timedelta(minutes=course_data.on_time)
        elif course_data.deadline == 2 and course_data.any_day and course_data.any_day != 0 and course_data.any_time and course_data.any_time != 0:
            if course_data.method == 0 or course_data.method == 1:
                if start_date.hour >= course_data.any_time:
                    start_date = start_date + datetime.timedelta(days=course_data.any_day+1)
                    start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                else:
                    start_date = start_date + datetime.timedelta(days=course_data.any_day)
                    start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
            elif course_data.method == 2:
                if course_data.business_mon_day or course_data.business_tue_day or course_data.business_wed_day or course_data.business_thu_day or course_data.business_fri_day or course_data.business_sat_day or course_data.business_sun_day:
                    count_date = datetime.datetime.now()
                    count = course_data.any_day
                    while count > 0:
                        count_date = count_date + datetime.timedelta(days=1)
                        if count_date.weekday() == 0:
                            if course_data.business_mon_day:
                                count = count - 1
                        elif count_date.weekday() == 1:
                            if course_data.business_tue_day:
                                count = count - 1
                        elif count_date.weekday() == 2:
                            if course_data.business_wed_day:
                                count = count - 1
                        elif count_date.weekday() == 3:
                            if course_data.business_thu_day:
                                count = count - 1
                        elif count_date.weekday() == 4:
                            if course_data.business_fri_day:
                                count = count - 1
                        elif count_date.weekday() == 5:
                            if course_data.business_sat_day:
                                count = count - 1
                        elif count_date.weekday() == 6:
                            if course_data.business_sun_day:
                                count = count - 1
                    start_date = datetime.datetime(count_date.year, count_date.month, count_date.day, 0, 0, 0)
                else:
                    if start_date.hour >= course_data.any_time:
                        start_date = start_date + datetime.timedelta(days=course_data.any_day+1)
                        start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                    else:
                        start_date = start_date + datetime.timedelta(days=course_data.any_day)
                        start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
    
    if setting and setting['advance']:
        import logging
        logger = logging.getLogger('development')
        logger.info(setting)
        if setting['type'] == 1:
            advance_setting = ReserveOfflineSetting.objects.filter(display_id=setting['advance']).first()
            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, offline=advance_setting, temp_flg=False).exclude(number=0).order_by('-number').first()
            if advance_schedule and advance_schedule.date and advance_schedule.time:
                advance_date = datetime.datetime(advance_schedule.date.year, advance_schedule.date.month, advance_schedule.date.day, advance_schedule.time.hour, advance_schedule.time.minute, 0)
                advance_date = advance_date + datetime.timedelta(minutes=advance_setting.time)
                if advance_date > start_date:
                    start_date = advance_date
        elif setting['type'] == 2:
            advance_setting = ReserveOfflineSetting.objects.filter(display_id=setting['advance']).first()
            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, online=advance_setting, temp_flg=False).exclude(number=0).order_by('-number').first()
            if advance_schedule and advance_schedule.date and advance_schedule.time:
                advance_date = datetime.datetime(advance_schedule.date.year, advance_schedule.date.month, advance_schedule.date.day, advance_schedule.time.hour, advance_schedule.time.minute, 0)
                advance_date = advance_date + datetime.timedelta(minutes=advance_setting.time)
                if advance_date > start_date:
                    start_date = advance_date

    start_date = {
        'year': start_date.year,
        'month': start_date.month,
        'day': start_date.day,
        'hour': start_date.hour,
        'minute': start_date.minute,
    }

    end_date = None
    if course_data and course_data.start != 0:
        end_date = datetime.datetime.now() +  datetime.timedelta(days=(course_data.start*7)+1)
        end_date = {
            'year': end_date.year,
            'month': end_date.month,
            'day': end_date.day,
            'hour': 0,
            'minute': 0,
        }
    if setting['type'] == 1:
        advance_setting = ReserveOfflineSetting.objects.filter(advance=setting['display_id']).first()
        advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, offline=advance_setting, temp_flg=False).exclude(number=0).order_by('-number').first()
        if advance_schedule and advance_schedule.date and advance_schedule.time:
            advance_date = datetime.datetime(advance_schedule.date.year, advance_schedule.date.month, advance_schedule.date.day, advance_schedule.time.hour, advance_schedule.time.minute, 0)
            end_date = {
                'year': advance_date.year,
                'month': advance_date.month,
                'day': advance_date.day,
                'hour': advance_date.hour,
                'minute': advance_date.minute,
            }
    elif setting['type'] == 2:
        advance_setting = ReserveOnlineSetting.objects.filter(advance=setting['display_id']).first()
        advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, online=advance_setting, temp_flg=False).exclude(number=0).order_by('-number').first()
        if advance_schedule and advance_schedule.date and advance_schedule.time:
            advance_date = datetime.datetime(advance_schedule.date.year, advance_schedule.date.month, advance_schedule.date.day, advance_schedule.time.hour, advance_schedule.time.minute, 0)
            end_date = {
                'year': advance_date.year,
                'month': advance_date.month,
                'day': advance_date.day,
                'hour': advance_date.hour,
                'minute': advance_date.minute,
            }
    
    course = None
    if request.POST.get('course_id'):
        if setting['type'] == 1:
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).values(*get_model_field(ReserveOfflineCourse)).first()
        elif setting['type'] == 2:
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).values(*get_model_field(ReserveOfflineCourse)).first()
    if course:
        reserve_data = course
    else:
        reserve_data = ReserveBasic.objects.filter(shop=auth_login.shop).values(*get_model_field(ReserveBasic)).first()

    data = {
        'online_offline': online_offline,
        'setting': setting,
        'year': current.year,
        'month': current.month,
        'day': current.day,
        'start': str(days[0].month) + '月' + str(days[0].day) + '日',
        'end': str(days[-1].month) + '月' + str(days[-1].day) + '日',
        'prev_year': prev.year,
        'prev_month': prev.month,
        'prev_day': prev.day,
        'next_year': next.year,
        'next_month': next.month,
        'next_day': next.day,
        'week_day': week_day,
        'week_time': week_time,
        'week_schedule': send_schedule,
        'start_date': start_date,
        'end_date': end_date,
        'reserve_data': reserve_data,
    }
    return JsonResponse( data, safe=False )

def send(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(display_id=request.POST.get('user_id')).first()

    if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        manager_list = list()
        facility_list = list()
        schedule_datetime = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        schedule_add_datetime = schedule_datetime + datetime.timedelta(minutes=setting.time)
        if setting:
            for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=setting).all():
                reception_manager = ReceptionOfflineManager.objects.filter(offline=setting.offline, manager=manager_menu_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).exists():
                            reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).first()
                            if reception_offline_manager_setting.flg:
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)
                
        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).all():
            if schedule.join != 2:
                schedule_list.append(schedule)

        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        manager_count = len(manager_list)
        facility_count = len(facility_list)
        reception_manager_list = list()
        reception_facility_list = list()
        count_flg = True
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule_item.offline.time)

            people_number = 0
            people_count = setting.people
            same_count = setting.facility
            if add_date > schedule_date and schedule_add_date > date:
                if manager_count <= 0 or facility_count <= 0:
                    break
                else:
                    if schedule_item.offline:
                        if schedule_item.offline == setting:
                            if schedule_date == date:
                                if count_flg:
                                    if schedule_item.offline_facility and schedule_item.offline_facility.count < people_count:
                                        same_count = same_count - 1
                                        if same_count == 0:
                                            if people_count > schedule_item.offline_facility.count:
                                                people_count = schedule_item.offline_facility.count
                                        else:
                                            people_total_count = schedule_item.offline_facility.count
                                            while same_count > 0:
                                                people_number = people_number + 1
                                                people_total_count = people_total_count + facility_list[people_number].count
                                                if facility_list[people_number] and not facility_list[people_number] in reception_facility_list:
                                                    facility_count = facility_count - 1
                                                    reception_facility_list.append(facility_list[people_number])
                                                same_count = same_count - 1
                                            if people_count > people_total_count:
                                                people_count = people_total_count
                                    count_flg = False
                                people_count = people_count - 1
                                if people_count <= 0:
                                    if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                        manager_count = manager_count - 1
                                        reception_manager_list.append(schedule_item.manager)
                                    if schedule_item.offline_facility in facility_list and not schedule_item.offline_facility in reception_facility_list:
                                        facility_count = facility_count - 1
                                        reception_facility_list.append(schedule_item.offline_facility)

                                    people_number = people_number + 1
                                    people_count = setting.people
                                    if facility_count > 0 and facility_list[people_number].count < people_count:
                                        people_count = facility_list[people_number].count
                            else:
                                if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                    manager_count = manager_count - 1
                                    reception_manager_list.append(schedule_item.manager)
                                if schedule_item.offline_facility in facility_list and not schedule_item.offline_facility in reception_facility_list:
                                    facility_count = facility_count - 1
                                    reception_facility_list.append(schedule_item.offline_facility)
                        else:
                            if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                manager_count = manager_count - 1
                                reception_manager_list.append(schedule_item.manager)
                            if schedule_item.offline_facility in facility_list and not schedule_item.offline_facility in reception_facility_list:
                                facility_count = facility_count - 1
                                reception_facility_list.append(schedule_item.offline_facility)

    if ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        manager_list = list()
        facility_list = list()
        schedule_datetime = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        schedule_add_datetime = schedule_datetime + datetime.timedelta(minutes=setting.time)
        if setting:
            for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=setting).all():
                reception_manager = ReceptionOnlineManager.objects.filter(online=setting.online, manager=manager_menu_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).exists():
                            reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).first()
                            if reception_online_manager_setting.flg:
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)

        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).all():
            if schedule.join != 2:
                schedule_list.append(schedule)

        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        manager_count = len(manager_list)
        facility_count = len(facility_list)
        reception_manager_list = list()
        reception_facility_list = list()
        count_flg = True
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.offline.time)

            people_number = 0
            people_count = setting.people
            same_count = setting.facility
            if add_date > schedule_date and schedule_add_date > date:
                if manager_count <= 0 or facility_count <= 0:
                    break
                else:
                    if schedule_item.online:
                        if schedule_item.online == setting:
                            if schedule_date == date:
                                if count_flg:
                                    if schedule_item.online_facility and schedule_item.online_facility.count < people_count:
                                        same_count = same_count - 1
                                        if same_count == 0:
                                            if people_count > schedule_item.online_facility.count:
                                                people_count = schedule_item.online_facility.count
                                        else:
                                            people_total_count = schedule_item.online_facility.count
                                            while same_count > 0:
                                                people_number = people_number + 1
                                                people_total_count = people_total_count + facility_list[people_number].count
                                                if facility_list[people_number] and not facility_list[people_number] in reception_facility_list:
                                                    facility_count = facility_count - 1
                                                    reception_facility_list.append(facility_list[people_number])
                                                same_count = same_count - 1
                                            if people_count > people_total_count:
                                                people_count = people_total_count
                                    count_flg = False
                                people_count = people_count - 1
                                if people_count <= 0:
                                    if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                        manager_count = manager_count - 1
                                        reception_manager_list.append(schedule_item.manager)
                                    if schedule_item.online_facility in facility_list and not schedule_item.online_facility in reception_facility_list:
                                        facility_count = facility_count - 1
                                        reception_facility_list.append(schedule_item.online_facility)

                                    people_number = people_number + 1
                                    people_count = setting.people
                                    if facility_count > 0 and facility_list[people_number].count < people_count:
                                        people_count = facility_list[people_number].count
                            else:
                                if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                    manager_count = manager_count - 1
                                    reception_manager_list.append(schedule_item.manager)
                                if schedule_item.online_facility in facility_list and not schedule_item.online_facility in reception_facility_list:
                                    facility_count = facility_count - 1
                                    reception_facility_list.append(schedule_item.online_facility)
                        else:
                            if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                manager_count = manager_count - 1
                                reception_manager_list.append(schedule_item.manager)
                            if schedule_item.online_facility in facility_list and not schedule_item.online_facility in reception_facility_list:
                                facility_count = facility_count - 1
                                reception_facility_list.append(schedule_item.online_facility)

    if manager_count <= 0 or facility_count <= 0:
        return JsonResponse( {'error': True}, safe=False )

    manager = None
    facility = None
    target_flow_tab = None
    if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user).first()
        setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        for menu in ReserveOfflineFlowMenu.objects.filter(shop=auth_login.shop, offline=setting).all():
            flow_tab = ShopFlowTab.objects.filter(flow=user_flow.flow, flow__shop=auth_login.shop, name=menu.flow).first()
            if not target_flow_tab or target_flow_tab.number > flow_tab.number:
                target_flow_tab = flow_tab

        people_count = setting.people
        manager_list = list()
        facility_list = list()
        if setting:
            for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=setting).all():
                reception_manager = ReceptionOfflineManager.objects.filter(offline=setting.offline, manager=manager_menu_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).exists():
                            reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).first()
                            if reception_offline_manager_setting.flg:
                                manager_menu_item.manager.count = people_count
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_menu_item.manager.count = people_count
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_menu_item.manager.count = people_count
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)
        
        user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user, flow_tab=target_flow_tab).first()
        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day'), temp_flg=False).exclude(Q(number=0)|Q(join=2)).all():
            schedule_list.append(schedule)

        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        reception_manager_list = list()
        reception_facility_list = list()
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule_item.offline.time)

            if add_date > schedule_date and schedule_add_date > date:
                if schedule_item.offline == setting:
                    if schedule_date == date:
                        for manager_item in manager_list:
                            if manager_item == schedule_item.manager:
                                manager_item.count = manager_item.count - 1
                                if manager_item.count <= 0 and schedule_item.manager:
                                    reception_manager_list.append(schedule_item.manager.id)
                        for facility_item in facility_list:
                            if facility_item == schedule_item.offline_facility:
                                facility_item.count = facility_item.count - 1
                                if facility_item.count <= 0:
                                    reception_facility_list.append(facility_item.id)
                    else:
                        if schedule_item.manager:
                            reception_manager_list.append(schedule_item.manager.id)
                        reception_facility_list.append(schedule_item.offline_facility.id)
                else:
                    if schedule_item.manager:
                        reception_manager_list.append(schedule_item.manager.id)
                    reception_facility_list.append(schedule_item.offline_facility.id)

        for manager_item in ReserveOfflineManagerMenu.objects.filter(shop=auth_login.shop, offline=setting).order_by('manager__created_at').values(*get_model_field(ReserveOfflineManagerMenu)).all():
            reception_manager = ReceptionOfflineManager.objects.filter(offline=setting.offline, manager__id=manager_item['manager'], reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
            if reception_manager:
                if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).exists():
                        reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).first()
                        if reception_offline_manager_setting.flg:
                            if not manager_item['manager'] in reception_manager_list:
                                manager = AuthUser.objects.filter(id=manager_item['manager']).values(*get_model_field(AuthUser)).first()
                                manager['profile'] = ManagerProfile.objects.filter(manager__id=manager['id']).values(*get_model_field(ManagerProfile)).first()
                                break
                    else:
                        if not manager_item['manager'] in reception_manager_list:
                            manager = AuthUser.objects.filter(id=manager_item['manager']).values(*get_model_field(AuthUser)).first()
                            manager['profile'] = ManagerProfile.objects.filter(manager__id=manager['id']).values(*get_model_field(ManagerProfile)).first()
                            break
                else:
                    if not manager_item['manager'] in reception_manager_list:
                        manager = AuthUser.objects.filter(id=manager_item['manager']).values(*get_model_field(AuthUser)).first()
                        manager['profile'] = ManagerProfile.objects.filter(manager__id=manager['id']).values(*get_model_field(ManagerProfile)).first()
                        break
        for facility_item in ReserveOfflineFacilityMenu.objects.filter(shop=auth_login.shop, offline=setting).values(*get_model_field(ReserveOfflineFacilityMenu)).all():
            if not facility_item['facility'] in reception_facility_list:
                facility = ReserveOfflineFacility.objects.filter(id=facility_item['facility']).values(*get_model_field(ReserveOfflineFacility)).first()
                break

        user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow).order_by('-number').first()
        UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).all().delete()
        UserFlowSchedule.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, UserFlowSchedule),
            flow = user_flow,
            number = 0,
            date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
            time = request.POST.get('hour') + ':' + request.POST.get('minute'),
            join = 0,
            offline = setting,
            offline_course = user_flow_schedule.offline_course,
            offline_facility = ReserveOfflineFacility.objects.filter(id=facility['id']).first(),
            manager = AuthUser.objects.filter(id=manager['id']).first(),
            temp_flg = True,
        )

    if ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user).first()
        setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        for menu in ReserveOnlineFlowMenu.objects.filter(shop=auth_login.shop, online=setting).all():
            flow_tab = ShopFlowTab.objects.filter(flow=user_flow.flow, flow__shop=auth_login.shop, name=menu.flow).first()
            if not target_flow_tab or target_flow_tab.number > flow_tab.number:
                target_flow_tab = flow_tab
        
        people_count = setting.people
        manager_list = list()
        facility_list = list()
        schedule_datetime = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        schedule_add_datetime = schedule_datetime + datetime.timedelta(minutes=setting.time)
        if setting:
            for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=setting).all():
                reception_manager = ReceptionOnlineManager.objects.filter(online=setting.online, manager=manager_menu_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).exists():
                            reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).first()
                            if reception_online_manager_setting.flg:
                                manager_menu_item.manager.count = people_count
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_menu_item.manager.count = people_count
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_menu_item.manager.count = people_count
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)
        
        user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user, flow_tab=target_flow_tab).first()
        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day'), temp_flg=False).exclude(Q(number=0)|Q(join=2)).all():
            schedule_list.append(schedule)

        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        reception_manager_list = list()
        reception_facility_list = list()
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule_item.online.time)

            if add_date > schedule_date and schedule_add_date > date:
                if schedule_item.online == setting:
                    if schedule_date == date:
                        for manager_item in manager_list:
                            if manager_item == schedule_item.manager:
                                manager_item.count = manager_item.count - 1
                                if manager_item.count <= 0 and schedule_item.manager:
                                    reception_manager_list.append(schedule_item.manager.id)
                        for facility_item in facility_list:
                            if facility_item == schedule_item.online_facility:
                                facility_item.count = facility_item.count - 1
                                if facility_item.count <= 0:
                                    reception_facility_list.append(facility_item.id)
                    else:
                        if schedule_item.manager:
                            reception_manager_list.append(schedule_item.manager.id)
                        reception_facility_list.append(schedule_item.online_facility.id)
                else:
                    if schedule_item.manager:
                        reception_manager_list.append(schedule_item.manager.id)
                    reception_facility_list.append(schedule_item.online_facility.id)

        for manager_item in ReserveOnlineManagerMenu.objects.filter(shop=auth_login.shop, online=setting).order_by('manager__created_at').values(*get_model_field(ReserveOnlineManagerMenu)).all():
            reception_manager = ReceptionOnlineManager.objects.filter(online=setting.online, manager=manager_item['manager'], reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
            if reception_manager:
                if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).exists():
                        reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).first()
                        if reception_online_manager_setting.flg:
                            if not manager_item['manager'] in reception_manager_list:
                                manager = AuthUser.objects.filter(id=manager_item['manager']).values(*get_model_field(AuthUser)).first()
                                manager['profile'] = ManagerProfile.objects.filter(manager__id=manager['id']).values(*get_model_field(ManagerProfile)).first()
                                break
                    else:
                        if not manager_item['manager'] in reception_manager_list:
                            manager = AuthUser.objects.filter(id=manager_item['manager']).values(*get_model_field(AuthUser)).first()
                            manager['profile'] = ManagerProfile.objects.filter(manager__id=manager['id']).values(*get_model_field(ManagerProfile)).first()
                            break
                else:
                    if not manager_item['manager'] in reception_manager_list:
                        manager = AuthUser.objects.filter(id=manager_item['manager']).values(*get_model_field(AuthUser)).first()
                        manager['profile'] = ManagerProfile.objects.filter(manager__id=manager['id']).values(*get_model_field(ManagerProfile)).first()
                        break
        for facility_item in ReserveOnlineFacilityMenu.objects.filter(shop=auth_login.shop, online=setting).values(*get_model_field(ReserveOnlineFacilityMenu)).all():
            if not facility_item['facility'] in reception_facility_list:
                facility = ReserveOnlineFacility.objects.filter(id=facility_item['facility']).values(*get_model_field(ReserveOnlineFacility)).first()
                break
        
        user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow).order_by('-number').first()
        UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).all().delete()
        UserFlowSchedule.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, UserFlowSchedule),
            flow = user_flow,
            number = 0,
            date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
            time = request.POST.get('hour') + ':' + request.POST.get('minute'),
            join = 0,
            online = setting,
            online_course = user_flow_schedule.online_course,
            online_facility = ReserveOnlineFacility.objects.filter(id=facility['id']).first(),
            manager = AuthUser.objects.filter(id=manager['id']).first(),
            temp_flg = True,
        )

    return JsonResponse( {'manager': manager, 'facility': facility}, safe=False )