from django.db.models import Q
from django.http import JsonResponse

from flow.models import ShopFlowTab, UserFlow, UserFlowSchedule
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace
from reserve.models import (
    ReserveBasic, ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflinePlace, ReserveOnlinePlace, ReserveOfflineSetting, ReserveOnlineSetting,
    ReserveStartDate, ReserveUserStartDate, ReserveCalendarDate, ReserveCalendarTime, ReserveTempCalendar,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu, ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
)
from setting.models import ShopOffline, ShopOnline, ShopOfflineTime, ShopOnlineTime
from sign.models import AuthShop
from user.models import LineUser

from itertools import chain

from common import get_model_field

import calendar
import datetime
import pandas

def check(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).first()

    end_offline_setting = list()
    end_online_setting = list()
    for user_flow in UserFlow.objects.filter(user=user).all():
        user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow, number=UserFlowSchedule.objects.filter(flow=user_flow, temp_flg=False).exclude(number=0).count()).first()
        if user_flow_schedule and ( user_flow_schedule.join == 0 or user_flow_schedule.join == 1 ) and user_flow_schedule.date and user_flow_schedule.number != 0:
            if user_flow_schedule.offline:
                end_offline_setting.append(user_flow_schedule.offline.id)
            if user_flow_schedule.online:
                end_online_setting.append(user_flow_schedule.online.id)

    offline_list = list(ShopOffline.objects.filter(shop=shop).order_by('created_at').values(*get_model_field(ShopOffline)).all())
    for offline_index, offline_item in enumerate(offline_list):
        offline_list[offline_index]['type'] = 1
        offline_list[offline_index]['time'] = list(ShopOfflineTime.objects.filter(offline__id=offline_item['id']).order_by('week').values(*get_model_field(ShopOfflineTime)).all())
    online_list = list(ShopOnline.objects.filter(shop=shop).order_by('created_at').values(*get_model_field(ShopOnline)).all())
    for online_index, online_item in enumerate(online_list):
        online_list[online_index]['type'] = 2
        online_list[online_index]['time'] = list(ShopOnlineTime.objects.filter(online__id=online_item['id']).order_by('week').values(*get_model_field(ShopOnlineTime)).all())
    online_offline_list = list(chain(offline_list, online_list))
    
    if len(online_offline_list) == 0:
        data = {
            'error_flg': True,
        }
        return JsonResponse( data, safe=False )

    place_flg = False
    if len(online_offline_list) > 1:
        place_flg = True

    member_query = Q(member=2)
    if user.member_flg:
        member_query.add(Q(member=1), Q.OR)
    else:
        member_query.add(Q(member=0), Q.OR)

    course_flg = False
    question_flg = False
    setting_list = list()
    user_flow = UserFlow.objects.filter(user=user).first()
    if user_flow:
        for flow_tab in ShopFlowTab.objects.filter(Q(flow=user_flow.flow), member_query).order_by('number').all():
            check_flow = UserFlow.objects.filter(user=user, flow_tab=flow_tab).first()
            if not check_flow or not check_flow.end_flg:
                for online_offline_item in online_offline_list:
                    if online_offline_item['type'] == 1:
                        setting = list(ReserveOfflineSetting.objects.filter(offline__id=online_offline_item['id'], display_flg=True).values(*get_model_field(ReserveOfflineSetting)).all())
                        for setting_item in setting:
                            if ReserveOfflineFlowMenu.objects.filter(offline__id=setting_item['id'], flow=flow_tab.name).exists():
                                if setting_item['course_flg']:
                                    course_flg = True
                                if setting_item['question']:
                                    question_flg = True
                                if not setting_item['id'] in end_offline_setting:
                                    if setting_item['advance']:
                                        advance_setting = ReserveOfflineSetting.objects.filter(display_id=setting_item['advance']).first()
                                        if advance_setting:
                                            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, offline=advance_setting, temp_flg=False).exclude(number=0).first()
                                            if advance_schedule and advance_schedule.date and advance_schedule.time:
                                                setting_list.append(setting_item)
                                        else:
                                            setting_list.append(setting_item)
                                    else:
                                        setting_list.append(setting_item)
                    elif online_offline_item['type'] == 2:
                        setting = list(ReserveOnlineSetting.objects.filter(online__id=online_offline_item['id'], display_flg=True).values(*get_model_field(ReserveOnlineSetting)).all())
                        for setting_item in setting:
                            if ReserveOnlineFlowMenu.objects.filter(online__id=setting_item['id'], flow=flow_tab.name).exists():
                                if setting_item['course_flg']:
                                    course_flg = True
                                if setting_item['question']:
                                    question_flg = True
                                if not setting_item['id'] in end_online_setting:
                                    if setting_item['advance']:
                                        advance_setting = ReserveOnlineSetting.objects.filter(display_id=setting_item['advance']).first()
                                        if advance_setting:
                                            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, online=advance_setting, temp_flg=False).exclude(number=0).first()
                                            if advance_schedule and advance_schedule.date and advance_schedule.time:
                                                setting_list.append(setting_item)
                                        else:
                                            setting_list.append(setting_item)
                                    else:
                                        setting_list.append(setting_item)
    if len(setting_list) == 0:
        data = {
            'error_flg': True,
        }
        return JsonResponse( data, safe=False )

    if place_flg:
        data = {
            'offline_place': ReserveOfflinePlace.objects.filter(shop=shop).values(*get_model_field(ReserveOfflinePlace)).first(),
            'online_place': ReserveOnlinePlace.objects.filter(shop=shop).values(*get_model_field(ReserveOnlinePlace)).first(),
            'online_offline_list': online_offline_list,
            'offline_list': offline_list,
            'online_list': online_list,
            'place_flg': place_flg,
            'course_flg': course_flg,
            'question_flg': question_flg,
            'error_flg': False,
        }
        return JsonResponse( data, safe=False )

    online_offline = None
    for online_offline_item in online_offline_list:
        online_offline = online_offline_item
    setting = None
    for setting_item in setting_list:
        if not setting:
            setting = setting_item

    if course_flg:
        course_list = list()
        if online_offline['type'] == 1:
            course_list = list(ReserveOfflineCourse.objects.filter(shop=shop).values(*get_model_field(ReserveOfflineCourse)).all())
        if online_offline['type'] == 2:
            course_list = list(ReserveOnlineCourse.objects.filter(shop=shop).values(*get_model_field(ReserveOnlineCourse)).all())

        data = {
            'online_offline': online_offline,
            'setting': setting,
            'course_list': course_list,
            'place_flg': place_flg,
            'course_flg': course_flg,
            'question_flg': question_flg,
        }                         
        return JsonResponse( data, safe=False )
    
    current = datetime.datetime.now()
    if online_offline['type'] == 1:
        user_start_date = ReserveUserStartDate.objects.filter(user=user, offline__id=setting['id']).first()
        if user_start_date:
            now = datetime.datetime.now()
            if user_start_date.date and now <= user_start_date.date:
                current = user_start_date.date
        else:
            reserve_start_date = ReserveStartDate.objects.filter(offline__id=setting['id'], offline_course=None).first()
            if reserve_start_date:
                now = datetime.datetime.now()
                if reserve_start_date.first_date and now <= reserve_start_date.first_date:
                    current = reserve_start_date.first_date
                elif reserve_start_date.second_date:
                    current = reserve_start_date.second_date
    elif online_offline['type'] == 2:
        user_start_date = ReserveUserStartDate.objects.filter(user=user, online__id=setting['id']).first()
        if user_start_date:
            now = datetime.datetime.now()
            if user_start_date.date and now <= user_start_date.date:
                current = user_start_date.date
        else:
            reserve_start_date = ReserveStartDate.objects.filter(online__id=setting['id'], online_course=None).first()
            if reserve_start_date:
                now = datetime.datetime.now()
                if reserve_start_date.first_date and now <= reserve_start_date.first_date:
                    current = reserve_start_date.first_date
                elif reserve_start_date.second_date:
                    current = reserve_start_date.second_date
    prev = current - datetime.timedelta(days=7)
    next = current + datetime.timedelta(days=7)

    days = None
    week_day = list()
    for week in calendar.Calendar().monthdatescalendar(current.year, current.month):
        if current.date() in week:
            days = week

    manager_list = list()
    facility_list = list()
    if online_offline['type'] == 1:
        for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline__id=setting['id']).all():
            manager_list.append(manager_menu_item.manager)
        for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline__id=setting['id']).order_by('facility__order').all():
            facility_list.append(facility_menu_item.facility)
    elif online_offline['type'] == 2:
        for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online__id=setting['id']).all():
            manager_list.append(manager_menu_item.manager)
        for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online__id=setting['id']).order_by('facility__order').all():
            facility_list.append(facility_menu_item.facility)

    time = {
        'from': None,
        'to': None
    }
    for day in days:
        if online_offline['type'] == 1:
            reception = ReceptionOfflinePlace.objects.filter(offline__id=online_offline['id'], reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).all()
        elif online_offline['type'] == 2:
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
    
    send_schedule = list()
    reserve_data = ReserveBasic.objects.filter(shop=shop).first()
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
        for times in pandas.date_range(start=datetime.datetime(current.year, current.month, current.day, time['from'].hour, time['from'].minute, 0), end=datetime.datetime(current.year, current.month, current.day, time['to'].hour, time['to'].minute, 0), freq=unit_time):
            schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
            send_week = list()
            for schedule_week_value in week_day:
                if online_offline['type'] == 1:
                    calendar_date = ReserveCalendarDate.objects.filter(shop=shop, offline__id=setting['id'], date__year=schedule_week_value['year'], date__month=schedule_week_value['month'], date__day=schedule_week_value['day']).first()
                    calendar_time = ReserveCalendarTime.objects.filter(calendar=calendar_date, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).first()
                    if calendar_time:
                        if calendar_date.flg:
                            send_week.append({
                                'year': schedule_week_value['year'],
                                'month': schedule_week_value['month'],
                                'day': schedule_week_value['day'],
                                'reception_flg': True,
                            })
                        else:
                            reserve_count = calendar_time.count
                            if ReserveTempCalendar.objects.filter(calendar=calendar_time, user=user).exists():
                                reserve_count = reserve_count + 1
                            if reserve_count > 0:
                                send_week.append({
                                    'year': schedule_week_value['year'],
                                    'month': schedule_week_value['month'],
                                    'day': schedule_week_value['day'],
                                    'reception_flg': False,
                                })
                            else:
                                send_week.append({
                                    'year': schedule_week_value['year'],
                                    'month': schedule_week_value['month'],
                                    'day': schedule_week_value['day'],
                                    'reception_flg': True,
                                })
                    else:
                        send_week.append({
                            'year': schedule_week_value['year'],
                            'month': schedule_week_value['month'],
                            'day': schedule_week_value['day'],
                            'reception_flg': True,
                        })
                elif online_offline['type'] == 2:
                    calendar_date = ReserveCalendarDate.objects.filter(shop=shop, online__id=setting['id'], date__year=schedule_week_value['year'], date__month=schedule_week_value['month'], date__day=schedule_week_value['day']).first()
                    calendar_time = ReserveCalendarTime.objects.filter(calendar=calendar_date, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).first()
                    if calendar_time:
                        if calendar_date.flg:
                            send_week.append({
                                'year': schedule_week_value['year'],
                                'month': schedule_week_value['month'],
                                'day': schedule_week_value['day'],
                                'reception_flg': True,
                            })
                        else:
                            reserve_count = calendar_time.count
                            if ReserveTempCalendar.objects.filter(calendar=calendar_time, user=user).exists():
                                reserve_count = reserve_count + 1
                            if reserve_count > 0:
                                send_week.append({
                                    'year': schedule_week_value['year'],
                                    'month': schedule_week_value['month'],
                                    'day': schedule_week_value['day'],
                                    'reception_flg': False,
                                })
                            else:
                                send_week.append({
                                    'year': schedule_week_value['year'],
                                    'month': schedule_week_value['month'],
                                    'day': schedule_week_value['day'],
                                    'reception_flg': True,
                                })
                    else:
                        send_week.append({
                            'year': schedule_week_value['year'],
                            'month': schedule_week_value['month'],
                            'day': schedule_week_value['day'],
                            'reception_flg': True,
                        })
            add_time = datetime.datetime(schedule_week_value['year'], schedule_week_value['month'], schedule_week_value['day'], int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0) + datetime.timedelta(minutes=setting['time'])
            send_schedule.append({
                'week': send_week,
                'time': schedule_time,
                'add_time': str(add_time.hour) + ':' + str(add_time.minute).ljust(2, '0'),
            })
    
    start_date = datetime.datetime.now()
    if reserve_data:
        if reserve_data.deadline == 1 and reserve_data.on_time and reserve_data.on_time != 0 and reserve_data.on_time != 1:
            start_date = start_date + datetime.timedelta(minutes=reserve_data.on_time)
        elif reserve_data.deadline == 2 and reserve_data.any_day and reserve_data.any_day != 0 and reserve_data.any_time and reserve_data.any_time != 0:
            if reserve_data.method == 0 or reserve_data.method == 1:
                if start_date.hour >= reserve_data.any_time:
                    start_date = start_date + datetime.timedelta(days=reserve_data.any_day+1)
                    start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                else:
                    start_date = start_date + datetime.timedelta(days=reserve_data.any_day)
                    start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
            elif reserve_data.method == 2:
                if reserve_data.business_mon_day or reserve_data.business_tue_day or reserve_data.business_wed_day or reserve_data.business_thu_day or reserve_data.business_fri_day or reserve_data.business_sat_day or reserve_data.business_sun_day:
                    count_date = datetime.datetime.now()
                    count = reserve_data.any_day
                    while count > 0:
                        count_date = count_date + datetime.timedelta(days=1)
                        if count_date.weekday() == 0:
                            if reserve_data.business_mon_day:
                                count = count - 1
                        elif count_date.weekday() == 1:
                            if reserve_data.business_tue_day:
                                count = count - 1
                        elif count_date.weekday() == 2:
                            if reserve_data.business_wed_day:
                                count = count - 1
                        elif count_date.weekday() == 3:
                            if reserve_data.business_thu_day:
                                count = count - 1
                        elif count_date.weekday() == 4:
                            if reserve_data.business_fri_day:
                                count = count - 1
                        elif count_date.weekday() == 5:
                            if reserve_data.business_sat_day:
                                count = count - 1
                        elif count_date.weekday() == 6:
                            if reserve_data.business_sun_day:
                                count = count - 1
                    start_date = datetime.datetime(count_date.year, count_date.month, count_date.day, 0, 0, 0)
                else:
                    if start_date.hour >= reserve_data.any_time:
                        start_date = start_date + datetime.timedelta(days=reserve_data.any_day+1)
                        start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
                    else:
                        start_date = start_date + datetime.timedelta(days=reserve_data.any_day)
                        start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)

    if setting and setting['advance']:
        if online_offline['type'] == 1:
            advance_setting = ReserveOfflineSetting.objects.filter(display_id=setting['advance']).first()
            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, offline=advance_setting, temp_flg=False).exclude(number=0).order_by('-number').first()
            if advance_schedule and advance_schedule.date and advance_schedule.time:
                advance_date = datetime.datetime(advance_schedule.date.year, advance_schedule.date.month, advance_schedule.date.day, advance_schedule.time.hour, advance_schedule.time.minute, 0)
                advance_date = advance_date + datetime.timedelta(minutes=advance_setting.time)
                if advance_date > start_date:
                    start_date = advance_date
        elif online_offline['type'] == 2:
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
    if reserve_data and reserve_data.start != 0:
        end_date = datetime.datetime.now() +  datetime.timedelta(days=(reserve_data.start*7)+1)
        end_date = {
            'year': end_date.year,
            'month': end_date.month,
            'day': end_date.day,
            'hour': 0,
            'minute': 0,
        }
    if online_offline['type'] == 1:
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
    elif online_offline['type'] == 2:
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

    if len(setting_list) > 0:
        data = {
            'online_offline': online_offline,
            'setting': setting,
            'setting_list': setting_list,
            'year': current.year,
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
            'reserve_data': ReserveBasic.objects.filter(shop=shop).values(*get_model_field(ReserveBasic)).first(),
            'place_flg': place_flg,
            'course_flg': course_flg,
            'question_flg': question_flg,
        }
        return JsonResponse( data, safe=False )
    else:
        data = {
            'error_flg': True,
        }
        return JsonResponse( data, safe=False )