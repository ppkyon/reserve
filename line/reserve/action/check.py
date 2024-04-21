from django.db.models import Q
from django.http import JsonResponse

from flow.models import ShopFlowTab, UserFlow, UserFlowSchedule
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager
from reserve.models import (
    ReserveBasic, ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflinePlace, ReserveOnlinePlace, ReserveOfflineSetting, ReserveOnlineSetting,
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
        user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow, number=UserFlowSchedule.objects.filter(flow=user_flow).count()).first()
        if user_flow_schedule and ( user_flow_schedule.join == 0 or user_flow_schedule.join == 1 ):
            if user_flow_schedule.offline:
                end_offline_setting.append(user_flow_schedule.offline.id)
            if user_flow_schedule.online:
                end_online_setting.append(user_flow_schedule.online.id)

    offline_list = list(ShopOffline.objects.filter(shop=shop).order_by('created_at').values(*get_model_field(ShopOffline)).all())
    for offline_index, offline_item in enumerate(offline_list):
        offline_list[offline_index]['type'] = 1
        offline_list[offline_index]['time'] = list(ShopOfflineTime.objects.filter(offline__id=offline_item['id']).order_by('week').values(*get_model_field(ShopOfflineTime)).all())
    online_list = list(ShopOnline.objects.filter(shop=shop).order_by('created_at').all())
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
    user_flow = UserFlow.objects.filter(user=user, end_flg=False).first()
    if user_flow:
        for flow_tab in ShopFlowTab.objects.filter(Q(flow=user_flow.flow), member_query).order_by('number').all():
            check_flow = UserFlow.objects.filter(user=user, flow_tab=flow_tab).first()
            if not check_flow or not check_flow.end_flg:
                for online_offline_item in online_offline_list:
                    if online_offline_item['type'] == 1:
                        setting = list(ReserveOfflineSetting.objects.filter(offline__id=online_offline_item['id']).values(*get_model_field(ReserveOfflineSetting)).all())
                        for setting_item in setting:
                            if ReserveOfflineFlowMenu.objects.filter(offline__id=setting_item['id'], flow=flow_tab.name).exists():
                                if setting_item['course_flg']:
                                    course_flg = True
                                if setting_item['question']:
                                    question_flg = True
                                if not setting_item['id'] in end_offline_setting:
                                    setting_list.append(setting_item)
                    elif online_offline_item['type'] == 2:
                        setting = list(ReserveOnlineSetting.objects.filter(online__id=online_offline_item['id']).values(*get_model_field(ReserveOfflineSetting)).all())
                        for setting_item in setting:
                            if ReserveOnlineFlowMenu.objects.filter(online__id=setting_item['id'], flow=flow_tab.name).exists():
                                if setting_item['course_flg']:
                                    course_flg = True
                                if setting_item['question']:
                                    question_flg = True
                                if not setting_item['id'] in end_online_setting:
                                    setting_list.append(setting_item)

    if place_flg:
        if len(setting_list) > 0:
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
        else:
            data = {
                'error_flg': True,
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
        if len(setting_list) > 0:
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
        else:
            data = {
                'error_flg': True,
            }                     
        return JsonResponse( data, safe=False )
    
    current = datetime.datetime.now()
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
            reception = ReceptionOfflinePlace.objects.filter(offline__id=online_offline['id'], reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).first()
        elif online_offline['type'] == 2:
            reception = ReceptionOnlinePlace.objects.filter(online__id=online_offline['id'], reception_date__year=day.year, reception_date__month=day.month, reception_date__day=day.day).first()
        if reception:
            reception_from = reception.reception_from
            reception_to = reception.reception_to
            reception_flg = reception.reception_flg
        else:
            reception_from = None
            reception_to = None
            reception_flg = True
        
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
    reception_data = list()
    week_schedule = list()
    week_time = list()
    unit_time = '60min'
    if reserve_data:
        if reserve_data.unit == 60:
            unit_time = '60min'
        elif reserve_data.unit == 30:
            unit_time = '30min'
        elif reserve_data.unit == 15:
            unit_time = '15min'
    if time['from'] and time['to']:
        for time in pandas.date_range(start=datetime.datetime(current.year, current.month, current.day, time['from'].hour, time['from'].minute, 0), end=datetime.datetime(current.year, current.month, current.day, time['to'].hour, time['to'].minute, 0), freq=unit_time):
            schedule_time = str(time.hour)+':'+str(time.minute).ljust(2, '0')
            week_time.append({
                'time': schedule_time
            })
            week_schedule.append({
                'week': week_day,
                'time': schedule_time,
            })

            for schedule_week_value in week_day:
                for schedule in UserFlowSchedule.objects.filter(flow__user__shop=shop, date__year=schedule_week_value['year'], date__month=schedule_week_value['month'], date__day=schedule_week_value['day'], time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
                    if schedule.join == 0 or schedule.join == 1:
                        date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
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
                                'end_flg': schedule.flow.end_flg,
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
                                'end_flg': schedule.flow.end_flg,
                            })
            
            send_week = list()
            for schedule_week_value in week_day:
                reception_flg = True
                for manager in manager_list:
                    schedule_datetime = datetime.datetime(schedule_week_value['year'], schedule_week_value['month'], schedule_week_value['day'], int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                    schedule_datetime = schedule_datetime + datetime.timedelta(minutes=setting['time'])
                    if online_offline['type'] == 1:
                        reception_place = ReceptionOfflinePlace.objects.filter(offline__id=online_offline['id'], reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=False).first()
                        reception_manager = ReceptionOfflineManager.objects.filter(offline__id=online_offline['id'], manager=manager, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                    if online_offline['type'] == 2:
                        reception_place = ReceptionOnlinePlace.objects.filter(online__id=online_offline['id'], reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=False).first()
                        reception_manager = ReceptionOnlineManager.objects.filter(online__id=online_offline['id'], manager=manager, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                    if reception_place and reception_manager and reception_flg and schedule_week_value['day'] == schedule_datetime.day:
                        manager_count = len(manager_list)
                        facility_count = len(facility_list)

                        if len(reception_data) > 0 :
                            people_number = 0
                            people_count = setting['people']
                            same_count = setting['facility']

                            schedule_date = datetime.datetime(schedule_week_value['year'], schedule_week_value['month'], schedule_week_value['day'], int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                            schedule_add_date = schedule_date + datetime.timedelta(minutes=setting['time'])

                            reception_manager_list = list()
                            reception_facility_list = list()
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
                                                            if same_count > 0:
                                                                people_number = people_number + 1
                                                                facility_count = facility_count - 1
                                                                if facility_list[people_number] and reception['facility'].count + facility_list[people_number].count < people_count:
                                                                    people_count = reception['facility'].count + facility_list[people_number].count
                                                            else:
                                                                people_count = reception['facility'].count
                                                        count_flg = False
                                                    people_count = people_count - 1
                                                    if people_count <= 0:
                                                        manager_count = manager_count - 1
                                                        facility_count = facility_count - 1

                                                        people_number = people_number + 1
                                                        people_count = setting['people']
                                                        if facility_count > 0 and facility_list[people_number].count < people_count:
                                                            people_count = facility_list[people_number].count
                                                else:
                                                    manager_count = manager_count - 1
                                                    facility_count = facility_count - 1
                                            else:
                                                if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                    manager_count = manager_count - 1
                                                if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                    facility_count = facility_count - 1
                                if reception['manager'] and not reception['manager'] in reception_manager_list:
                                    reception_manager_list.append(reception['manager'])
                                if reception['facility'] and not reception['facility'] in reception_facility_list:
                                    reception_facility_list.append(reception['facility'])
                            if manager_count > 0 and facility_count > 0:
                                reception_flg = False
                                break
                        else:
                            schedule_date = datetime.datetime(schedule_week_value['year'], schedule_week_value['month'], schedule_week_value['day'], int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                            if manager_count > 0 and facility_count > 0:
                                reception_flg = False
                                break
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