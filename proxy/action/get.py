from django.db.models import Q
from django.http import JsonResponse

from flow.models import ShopFlow, ShopFlowTab, UserFlowSchedule
from question.models import ShopQuestion, ShopQuestionItem, ShopQuestionItemChoice
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager
from reserve.models import (
    ReserveBasic, ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflineSetting, ReserveOnlineSetting,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu, ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
)
from setting.models import ShopOffline, ShopOnline, ShopOfflineTime, ShopOnlineTime
from sign.models import AuthLogin

from itertools import chain

from common import get_model_field

import calendar
import datetime
import pandas

def course(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    course = list()
    if ShopOffline.objects.filter(display_id=request.POST.get('id')).exists():
        course = list(ReserveOfflineCourse.objects.filter(shop=auth_login.shop).values(*get_model_field(ReserveOfflineCourse)).all())
    if ShopOnline.objects.filter(display_id=request.POST.get('id')).exists():
        course = list(ReserveOnlineCourse.objects.filter(shop=auth_login.shop).values(*get_model_field(ReserveOnlineCourse)).all())
    return JsonResponse( course, safe=False )

def date(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

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
        offline_list = list(ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').values(*get_model_field(ShopOffline)).all())
        for offline_index, offline_item in enumerate(offline_list):
            offline_list[offline_index]['type'] = 1
            offline_list[offline_index]['time'] = list(ShopOfflineTime.objects.filter(offline__id=offline_item['id']).order_by('week').values(*get_model_field(ShopOfflineTime)).all())
        online_list = list(ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').values(*get_model_field(ShopOnline)).all())
        for online_index, online_item in enumerate(online_list):
            online_list[online_index]['type'] = 2
            online_list[online_index]['time'] = list(ShopOnlineTime.objects.filter(online__id=online_item['id']).order_by('week').values(*get_model_field(ShopOnlineTime)).all())
        online_offline_list = list(chain(offline_list, online_list))

    flow = None
    if ShopFlow.objects.filter(shop=auth_login.shop, period_from__lte=datetime.datetime.now(), period_to__isnull=True, delete_flg=False).exists():
        flow = ShopFlow.objects.filter(shop=auth_login.shop, period_from__lte=datetime.datetime.now(), period_to__isnull=True, delete_flg=False).first()
    elif ShopFlow.objects.filter(shop=auth_login.shop, period_to__gte=datetime.datetime.now(), period_from__isnull=True, delete_flg=False).exists():
        flow = ShopFlow.objects.filter(shop=auth_login.shop, period_to__gte=datetime.datetime.now(), period_from__isnull=True, delete_flg=False).first()
    elif ShopFlow.objects.filter(shop=auth_login.shop, period_from__lte=datetime.datetime.now(), period_to__gte=datetime.datetime.now(), delete_flg=False).exists():
        flow = ShopFlow.objects.filter(shop=auth_login.shop, period_from__lte=datetime.datetime.now(), period_to__gte=datetime.datetime.now(), delete_flg=False).first()
        
    question_flg = False
    setting_list = list()
    if flow:
        for flow_tab in ShopFlowTab.objects.filter(Q(flow=flow), Q(Q(member=0)|Q(member=2))).order_by('number').all():
            for online_offline_item in online_offline_list:
                if online_offline_item['type'] == 1:
                    setting = list(ReserveOfflineSetting.objects.filter(offline__id=online_offline_item['id']).values(*get_model_field(ReserveOfflineSetting)).all())
                    for setting_item in setting:
                        if ReserveOfflineFlowMenu.objects.filter(offline__id=setting_item['id'], flow=flow_tab.name).exists():
                            if setting_item['question']:
                                question_flg = True
                            setting_list.append(setting_item)
                elif online_offline_item['type'] == 2:
                    setting = list(ReserveOnlineSetting.objects.filter(online__id=online_offline_item['id']).values(*get_model_field(ReserveOnlineSetting)).all())
                    for setting_item in setting:
                        if ReserveOnlineFlowMenu.objects.filter(online__id=setting_item['id'], flow=flow_tab.name).exists():
                            if setting_item['question']:
                                question_flg = True
                            setting_list.append(setting_item)
    
    online_offline = None
    for online_offline_item in online_offline_list:
        online_offline = online_offline_item
        break
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
    
    course = None
    if request.POST.get('course_id'):
        if online_offline['type'] == 1:
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
        elif online_offline['type'] == 2:
            course = ReserveOnlineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
    if course:
        course_data = course
    else:
        course_data = ReserveBasic.objects.filter(shop=auth_login.shop).first()
    
    reserve_data = ReserveBasic.objects.filter(shop=auth_login.shop).first()
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

            for schedule_week_value in week_day:
                for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__year=schedule_week_value['year'], date__month=schedule_week_value['month'], date__day=schedule_week_value['day'], time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
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
        reserve_data = ReserveBasic.objects.filter(shop=auth_login.shop).values(*get_model_field(ReserveBasic)).first()

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

def question(request):
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