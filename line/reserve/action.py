from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from PIL import Image

from flow.models import ShopFlowTab, ShopFlowItem, ShopFlowRichMenu, UserFlow, UserFlowSchedule
from question.models import ShopQuestion, ShopQuestionItem, ShopQuestionItemChoice, UserQuestion, UserQuestionItem, UserQuestionItemChoice
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager
from reserve.models import (
    ReserveBasic, ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflinePlace, ReserveOnlinePlace, ReserveOfflineSetting, ReserveOnlineSetting,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu, ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
)
from setting.models import ShopOffline, ShopOnline, ShopOfflineTime, ShopOnlineTime
from sign.models import AuthShop
from user.models import LineUser, UserProfile

from itertools import chain

from common import create_code, get_model_field
from flow.action.go import go

import base64
import calendar
import cv2
import datetime
import environ
import io
import os
import pandas
import urllib.parse
import urllib.request
import uuid

env = environ.Env()
env.read_env('.env')

def check(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).first()

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

    course_flg = False
    question_flg = False
    setting_list = list()
    user_flow = UserFlow.objects.filter(user=user, end_flg=False).first()
    if user_flow:
        for flow_tab in ShopFlowTab.objects.filter(flow=user_flow.flow).order_by('number').all():
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
                                setting_list.append(setting_item)
                    elif online_offline_item['type'] == 2:
                        setting = list(ReserveOnlineSetting.objects.filter(online__id=online_offline_item['id']).values(*get_model_field(ReserveOfflineSetting)).all())
                        for setting_item in setting:
                            if ReserveOnlineFlowMenu.objects.filter(online__id=setting_item['id'], flow=flow_tab.name).exists():
                                if setting_item['course_flg']:
                                    course_flg = True
                                if setting_item['question']:
                                    question_flg = True
                                setting_list.append(setting_item)

    if place_flg:
        data = {
            'offline_place': ReserveOfflinePlace.objects.filter(shop=shop).values(*get_model_field(ReserveOfflinePlace)).first(),
            'online_place': ReserveOnlinePlace.objects.filter(shop=shop).values(*get_model_field(ReserveOnlinePlace)).first(),
            'offline_list': online_offline_list,
            'online_offline_list': offline_list,
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
                                        if reception['interview']:
                                            if reception['interview'].id == setting['id']:
                                                if schedule_date == reception['from']:
                                                    if count_flg:
                                                        if reception['facility'] and reception['facility'].count < people_count:
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



def get_course(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    course = list()
    if ShopOffline.objects.filter(display_id=request.POST.get('id')).exists():
        course = list(ReserveOfflineCourse.objects.filter(shop=shop).values(*get_model_field(ReserveOfflineCourse)).all())
    if ShopOnline.objects.filter(display_id=request.POST.get('id')).exists():
        course = list(ReserveOnlineCourse.objects.filter(shop=shop).values(*get_model_field(ReserveOnlineCourse)).all())
    return JsonResponse( course, safe=False )

def get_date(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).first()

    if request.POST.get('id'):
        if ShopOffline.objects.filter(display_id=request.POST.get('id')).exists():
            offline_list = list(ShopOffline.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(ShopOffline)).all())
            for offline_index, offline_item in enumerate(offline_list):
                offline_list[offline_index]['type'] = 1
                offline_list[offline_index]['time'] = list(ShopOfflineTime.objects.filter(offline__id=offline_item['id']).order_by('week').values(*get_model_field(ShopOfflineTime)).all())
            online_offline_list = offline_list
        if ShopOnline.objects.filter(display_id=request.POST.get('id')).exists():
            online_list = list(ShopOnline.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(ShopOnline)).all())
            for online_index, online_item in enumerate(online_list):
                online_list[online_index]['type'] = 2
                online_list[online_index]['time'] = list(ShopOnlineTime.objects.filter(online__id=online_item['id']).order_by('week').values(*get_model_field(ShopOnlineTime)).all())
            online_offline_list = online_list
    else:
        offline_list = list(ShopOffline.objects.filter(shop=shop).order_by('created_at').values(*get_model_field(ShopOffline)).all())
        for offline_index, offline_item in enumerate(offline_list):
            offline_list[offline_index]['type'] = 1
            offline_list[offline_index]['time'] = list(ShopOfflineTime.objects.filter(offline__id=offline_item['id']).order_by('week').values(*get_model_field(ShopOfflineTime)).all())
        online_list = list(ShopOnline.objects.filter(shop=shop).order_by('created_at').values(*get_model_field(ShopOnline)).all())
        for online_index, online_item in enumerate(online_list):
            online_list[online_index]['type'] = 2
            online_list[online_index]['time'] = list(ShopOnlineTime.objects.filter(online__id=online_item['id']).order_by('week').values(*get_model_field(ShopOnlineTime)).all())
        online_offline_list = list(chain(offline_list, online_list))

    question_flg = False
    setting_list = list()
    user_flow = UserFlow.objects.filter(user=user, end_flg=False).first()
    if user_flow:
        for flow_tab in ShopFlowTab.objects.filter(flow=user_flow.flow).order_by('number').all():
            check_flow = UserFlow.objects.filter(user=user, flow_tab=flow_tab).first()
            if not check_flow or not check_flow.end_flg:
                for online_offline_item in online_offline_list:
                    if online_offline_item['type'] == 1:
                        setting = list(ReserveOfflineSetting.objects.filter(offline__id=online_offline_item['id']).values(*get_model_field(ReserveOfflineSetting)).all())
                        for setting_item in setting:
                            if ReserveOfflineFlowMenu.objects.filter(offline__id=setting_item['id'], flow=flow_tab.name).exists():
                                if setting_item['question']:
                                    question_flg = True
                                setting_list.append(setting_item)
                    elif online_offline_item['type'] == 2:
                        setting = list(ReserveOnlineSetting.objects.filter(online__id=online_offline_item['id']).values(*get_model_field(ReserveOfflineSetting)).all())
                        for setting_item in setting:
                            if ReserveOnlineFlowMenu.objects.filter(online__id=setting_item['id'], flow=flow_tab.name).exists():
                                if setting_item['question']:
                                    question_flg = True
                                setting_list.append(setting_item)
    
    online_offline = None
    for online_offline_item in online_offline_list:
        online_offline = online_offline_item
    setting = None
    for setting_item in setting_list:
        if not setting:
            if request.POST.get('setting_id'):
                if setting_item['display_id'] == int(request.POST.get('setting_id')):
                    setting = setting_item
            else:
                setting = setting_item
    
    
    if request.POST.get("year") and request.POST.get("month") and request.POST.get("day"):
        current = datetime.datetime(int(request.POST.get("year")), int(request.POST.get("month")), int(request.POST.get("day")))
    else:
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
    if setting:
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
    
    course = None
    if request.POST.get('course_id'):
        if online_offline['type'] == 1:
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
        elif online_offline['type'] == 2:
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
    if course:
        course_data = course
    else:
        course_data = ReserveBasic.objects.filter(shop=shop).first()
    
    reserve_data = ReserveBasic.objects.filter(shop=shop).first()
    send_schedule = list()
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
                                        if reception['interview']:
                                            if reception['interview'].id == setting['id']:
                                                if schedule_date == reception['from']:
                                                    if count_flg:
                                                        if reception['facility'] and reception['facility'].count < people_count:
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
        }
    
    course = None
    if request.POST.get('course_id'):
        if online_offline['type'] == 1:
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).values(*get_model_field(ReserveOfflineCourse)).first()
        elif online_offline['type'] == 2:
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).values(*get_model_field(ReserveOfflineCourse)).first()
    if course:
        reserve_data = course
    else:
        reserve_data = ReserveBasic.objects.filter(shop=shop).values(*get_model_field(ReserveBasic)).first()

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
        'reserve_data': reserve_data,
        'question_flg': question_flg,
    }
    return JsonResponse( data, safe=False )

def get_question(request):
    if request.POST.get('setting_id'):
        if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
            setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        if ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
            setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        question = None
        if setting and setting.question:
            question = ShopQuestion.objects.filter(id=setting.question.id).values(*get_model_field(ShopQuestion)).first()
            question['item'] = list(ShopQuestionItem.objects.filter(question__id=question['id']).order_by('number').values(*get_model_field(ShopQuestionItem)).all())
            for question_index, question_item in enumerate(question['item']):
                if question_item['type'] == 99:
                    question['item'][question_index]['choice'] = list(ShopQuestionItemChoice.objects.filter(question_item__id=question_item['id']).values(*get_model_field(ShopQuestionItemChoice)).all())
            if question:
                return JsonResponse( {'check': True, 'question': question, 'age_list': [i for i in range(101)]}, safe=False )
        else:
            return JsonResponse( {'check': False, 'question': None, 'age_list': [i for i in range(101)]}, safe=False )
    return JsonResponse( {'check': False, 'question': None, 'age_list': [i for i in range(101)]}, safe=False )



def send(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).first()

    if UserProfile.objects.filter(user=user).exists():
        user_profile = UserProfile.objects.filter(user=user).first()
    else:
        user_profile = UserProfile.objects.create(
            id = str(uuid.uuid4()),
            user = user,
        )
    user.updated_at = datetime.datetime.now()
    user.save()
    
    question = None
    if request.POST.get('question_id'):
        question = ShopQuestion.objects.filter(display_id=request.POST.get('question_id')).first()
        user_question = UserQuestion.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, UserQuestion),
            user = user,
            question = question,
        )
        
        for shop_question_index, shop_question_item in enumerate(ShopQuestionItem.objects.filter(question=question).order_by('number').all()):
            if request.POST.get('type_'+str(shop_question_index+1)) == '1':
                if request.POST.get('text_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))),
                    )
                    user_profile.name = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1)))
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        text = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '2':
                if request.POST.get('text_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))),
                    )
                    user_profile.name_kana = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1)))
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        text = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '3':
                if request.POST.get('value_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        value = urllib.parse.unquote(request.POST.get('value_'+str(shop_question_index+1))).replace('歳', ''),
                    )
                    user_profile.age = urllib.parse.unquote(request.POST.get('value_'+str(shop_question_index+1))).replace('歳', '')
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        value = 0,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '4':
                if request.POST.get('value_'+str(shop_question_index+1)):
                    if request.POST.get('value_'+str(shop_question_index+1)):
                        UserQuestionItem.objects.create(
                            id = str(uuid.uuid4()),
                            user = user_question,
                            question = shop_question_item,
                            value = 0,
                        )
                    elif urllib.parse.unquote(request.POST.get('value_'+str(shop_question_index+1))) == '男性':
                        UserQuestionItem.objects.create(
                            id = str(uuid.uuid4()),
                            user = user_question,
                            question = shop_question_item,
                            value = 1,
                        )
                        user_profile.sex = 1
                    elif urllib.parse.unquote(request.POST.get('value_'+str(shop_question_index+1))) == '女性':
                        UserQuestionItem.objects.create(
                            id = str(uuid.uuid4()),
                            user = user_question,
                            question = shop_question_item,
                            value = 2,
                        )
                        user_profile.sex = 2
                    user_profile.save()
            elif request.POST.get('type_'+str(shop_question_index+1)) == '5':
                if request.POST.get('text_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))).replace( '-', ''),
                    )
                    user_profile.phone_number = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))).replace( '-', '')
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        text = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '6':
                if request.POST.get('email_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        email = urllib.parse.unquote(request.POST.get('email_'+str(shop_question_index+1))),
                    )
                    user_profile.email = urllib.parse.unquote(request.POST.get('email_'+str(shop_question_index+1)))
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        email = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '7':
                if request.POST.get('date_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        date = urllib.parse.unquote(request.POST.get('date_'+str(shop_question_index+1))).replace( '/', '-'),
                    )
                    today = datetime.date.today()
                    birthday = datetime.datetime.strptime(urllib.parse.unquote(request.POST.get('date_'+str(shop_question_index+1))).replace( '/', '-'), '%Y-%m-%d')
                    user_profile.age = (int(today.strftime("%Y%m%d")) - int(birthday.strftime("%Y%m%d"))) // 10000
                    user_profile.birth = urllib.parse.unquote(request.POST.get('date_'+str(shop_question_index+1))).replace( '/', '-')
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        date = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '8':
                if request.POST.get('text_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))),
                    )
                    user_profile.address = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1)))
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        text = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '9':
                if request.POST.get('image_'+str(shop_question_index+1)):
                    if ';base64,' in request.POST.get('image_'+str(shop_question_index+1)):
                        format, imgstr = request.POST.get('image_'+str(shop_question_index+1)).split(';base64,') 
                        ext = format.split('/')[-1]
                        data = ContentFile(base64.b64decode(request.POST.get('image_url_'+str(shop_question_index+1)).replace( ' ', '+' )), name='temp.' + ext)
                    else:
                        data = request.POST.get('image_url_'+str(shop_question_index+1))
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        image = data,
                    )
                    user_profile.image = data
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        image = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '10':
                if request.POST.get('image_'+str(shop_question_index+1)):
                    if ';base64,' in request.POST.get('image_'+str(shop_question_index+1)):
                        format, imgstr = request.POST.get('image_'+str(shop_question_index+1)).split(';base64,') 
                        ext = format.split('/')[-1]
                        data = ContentFile(base64.b64decode(request.POST.get('image_url_'+str(shop_question_index+1)).replace( ' ', '+' )), name='temp.' + ext)
                    else:
                        data = request.POST.get('image_url_'+str(shop_question_index+1))
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        image = data,
                    )
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        image = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '11':
                if request.POST.get('video_'+str(shop_question_index+1)):
                    if ';base64,' in request.POST.get('video_'+str(shop_question_index+1)):
                        format, imgstr = request.POST.get('video_'+str(shop_question_index+1)).split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(request.POST.get('video_'+str(shop_question_index+1)).replace( ' ', '+' )), name='temp.' + ext)
                    else:
                        data = request.POST.get('video_url_'+str(shop_question_index+1))
                    user_question_item = UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        video = data,
                        video_thumbnail = None,
                    )

                    if env('AWS_FLG') == 'True':
                        video_name = './static/' + str(uuid.uuid4()).replace('-', '') + '.mp4'
                        urllib.request.urlretrieve(user_question_item.video.url, video_name)
                        cap = cv2.VideoCapture(video_name)
                    else:
                        cap = cv2.VideoCapture(user_question_item.video.url[1:])
                    res, thumbnail = cap.read()
                    image = Image.fromarray(cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB))
                    image_io = io.BytesIO()
                    image.save(image_io, format="JPEG")
                    image_file = InMemoryUploadedFile(image_io, field_name=None, name=str(uuid.uuid4()).replace('-', '') + '.jpg', content_type="image/jpeg", size=image_io.getbuffer().nbytes, charset=None)
                    
                    user_question_item.video_thumbnail = image_file
                    user_question_item.save()

                    cap.release()
                    if env('AWS_FLG') == 'True':
                        os.remove(video_name)
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        user = user_question,
                        question = shop_question_item,
                        video = None,
                        video_thumbnail = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '99':
                user_question_item = UserQuestionItem.objects.create(
                    id = str(uuid.uuid4()),
                    user = user_question,
                    question = shop_question_item,
                )
                if request.POST.get('choice_type_'+str(shop_question_index+1)) == '1':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('text_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1)):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1))),
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                text = None,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '2':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('choice_value_'+str(shop_question_index+1)) == str(shop_question_choice_item.number):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                text = 1,
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                text = 0,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '3':
                    choice_value = request.POST.getlist('choice_value_'+str(shop_question_index+1)+'%5B%5D')
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if str(shop_question_choice_item.number) in choice_value:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                text = 1,
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                text = 0,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '4':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('choice_text_'+str(shop_question_index+1)) == shop_question_choice_item.text:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                text = 1,
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                text = 0,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '5':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('date_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1)):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                date = urllib.parse.unquote(request.POST.get('date_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1))).replace( '/', '-'),
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                date = None,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '6':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('time_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1)):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                time = urllib.parse.unquote(request.POST.get('time_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1))),
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                time = None,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '7':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('date_time_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1)):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                date = urllib.parse.unquote(request.POST.get('date_time_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1))).replace( '/', '-'),
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                user = user_question_item,
                                question = shop_question_choice_item,
                                date = None,
                            )

    target_flow_tab = None
    if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        for menu in ReserveOfflineFlowMenu.objects.filter(shop=shop, offline=setting).all():
            flow_tab = ShopFlowTab.objects.filter(name=menu.flow).first()
            if not target_flow_tab or target_flow_tab.number > flow_tab.number:
                target_flow_tab = flow_tab
                
        target_flg = False
        target_flow_item = None
        target_rich_menu = None
        for flow_item in ShopFlowItem.objects.filter(flow_tab=target_flow_tab).all():
            if flow_item.type == 7:
                target_rich_menu = ShopFlowRichMenu.objects.filter(flow=flow_item).first()
                target_rich_menu = target_rich_menu.rich_menu
            if target_flg:
                target_flow_item = flow_item
            if flow_item.type == 54:
                target_flg = True
    
        if UserFlow.objects.filter(user=user, flow_tab=target_flow_tab).exists():
            user_flow = UserFlow.objects.filter(user=user, flow_tab=target_flow_tab).first()
            user_flow.flow = target_flow_tab.flow
            user_flow.flow_tab = target_flow_tab
            user_flow.flow_item = target_flow_item
            user_flow.name = target_flow_tab.name
            user_flow.richmenu = target_rich_menu
            user_flow.end_flg = False
            user_flow.save()
        else:
            user_flow = UserFlow.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                user = user,
                number = UserFlow.objects.filter(user=user).count() + 1,
                flow = target_flow_tab.flow,
                flow_tab = target_flow_tab,
                flow_item = target_flow_item,
                name = target_flow_tab.name,
                richmenu = target_rich_menu,
                end_flg = False,
            )
        
        course = None
        if request.POST.get('course_id'):
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()

        if UserFlowSchedule.objects.filter(flow=user_flow).exists():
            user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow).order_by('number').first()
            user_flow_schedule.number = 1
            user_flow_schedule.date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day')
            user_flow_schedule.time = request.POST.get('hour') + ':' + request.POST.get('minute')
            user_flow_schedule.join = 0
            user_flow_schedule.offline = setting
            user_flow_schedule.offline_course = course
            user_flow_schedule.question = question
            user_flow_schedule.save()
        else:
            UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                flow = user_flow,
                number = 1,
                date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
                time = request.POST.get('hour') + ':' + request.POST.get('minute'),
                join = 0,
                offline = setting,
                offline_course = course,
                question = question,
            )

    if ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        for menu in ReserveOnlineFlowMenu.objects.filter(shop=shop, online=setting).all():
            flow_tab = ShopFlowTab.objects.filter(name=menu.flow).first()
            if not target_flow_tab or target_flow_tab.number > flow_tab.number:
                target_flow_tab = flow_tab
        
        target_flg = False
        target_flow_item = None
        target_rich_menu = None
        for flow_item in ShopFlowItem.objects.filter(flow_tab=target_flow_tab).all():
            if flow_item.type == 7:
                target_rich_menu = ShopFlowRichMenu.objects.filter(flow=flow_item).first()
                target_rich_menu = target_rich_menu.rich_menu
            if target_flg:
                target_flow_item = flow_item
            if flow_item.type == 54:
                target_flg = True
        
        if UserFlow.objects.filter(user=user, flow_tab=target_flow_tab).exists():
            user_flow = UserFlow.objects.filter(user=user, flow_tab=target_flow_tab).first()
            user_flow.flow = target_flow_tab.flow
            user_flow.flow_tab = target_flow_tab
            user_flow.flow_item = target_flow_item
            user_flow.name = target_flow_tab.name
            user_flow.richmenu = target_rich_menu
            user_flow.end_flg = False
            user_flow.save()
        else:
            user_flow = UserFlow.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                user = user,
                number = UserFlow.objects.filter(user=user).count() + 1,
                flow = target_flow_tab.flow,
                flow_tab = target_flow_tab,
                flow_item = target_flow_item,
                name = target_flow_tab.name,
                richmenu = target_rich_menu,
                end_flg = False,
            )
        
        course = None
        if request.POST.get('course_id'):
            course = ReserveOnlineCourse.objects.filter(display_id=request.POST.get('course_id')).first()

        if UserFlowSchedule.objects.filter(flow=user_flow).exists():
            user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow).order_by('number').first()
            user_flow_schedule.number = 1
            user_flow_schedule.date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day')
            user_flow_schedule.time = request.POST.get('hour') + ':' + request.POST.get('minute')
            user_flow_schedule.join = 0
            user_flow_schedule.online = setting
            user_flow_schedule.online_course = course
            user_flow_schedule.question = question
            user_flow_schedule.save()
        else:
            UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                flow = user_flow,
                number = 1,
                date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
                time = request.POST.get('hour') + ':' + request.POST.get('minute'),
                join = 0,
                online = setting,
                online_course = course,
                question = question,
            )

    user_flow = UserFlow.objects.filter(user=user, flow_tab=target_flow_tab).first()
    for flow_item in ShopFlowItem.objects.filter(flow_tab=user_flow.flow_tab, x__gte=user_flow.flow_item.x, y__gte=user_flow.flow_item.y).order_by('y', 'x').all():
        if go(user, user_flow.flow, user_flow.flow_tab, flow_item):
            break
    return JsonResponse( {}, safe=False )