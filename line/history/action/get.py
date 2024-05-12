from django.http import JsonResponse

from flow.models import UserFlowSchedule
from question.models import UserQuestion, UserQuestionItem, UserQuestionItemChoice
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager
from reserve.models import (
    ReserveBasic, ReserveOfflineSetting, ReserveOnlineSetting, ReserveOfflineCourse, ReserveOnlineCourse, ReserveStartDate,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu
)
from setting.models import ShopOffline, ShopOnline, ShopOfflineTime, ShopOnlineTime
from sign.models import AuthShop
from user.models import LineUser

from common import get_model_field

import calendar
import datetime
import pandas

def date(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).first()

    if ShopOffline.objects.filter(display_id=request.POST.get('place_id')).exists():
        offline = ShopOffline.objects.filter(display_id=request.POST.get('place_id')).values(*get_model_field(ShopOffline)).first()
        offline['type'] = 1
        offline['time'] = list(ShopOfflineTime.objects.filter(offline__id=offline['id']).order_by('week').values(*get_model_field(ShopOfflineTime)).all())
        online_offline = offline
    if ShopOnline.objects.filter(display_id=request.POST.get('place_id')).exists():
        online = ShopOnline.objects.filter(display_id=request.POST.get('place_id')).values(*get_model_field(ShopOnline)).first()
        online['type'] = 2
        online['time'] = list(ShopOnlineTime.objects.filter(online__id=online['id']).order_by('week').values(*get_model_field(ShopOnlineTime)).all())
        online_offline = online

    setting = None
    if online_offline['type'] == 1:
        setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).values(*get_model_field(ReserveOfflineSetting)).first()
    elif online_offline['type'] == 2:
        setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).values(*get_model_field(ReserveOnlineSetting)).first()

    course = None
    if request.POST.get('course_id'):
        if online_offline['type'] == 1:
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
        elif online_offline['type'] == 2:
            course = ReserveOnlineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
    if course:
        course_data = course
    else:
        course_data = ReserveBasic.objects.filter(shop=shop).first()

    if request.POST.get("year") and request.POST.get("month") and request.POST.get("day"):
        current = datetime.datetime(int(request.POST.get("year")), int(request.POST.get("month")), int(request.POST.get("day")))
    else:
        current = datetime.datetime.now()
        if online_offline['type'] == 1:
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
        elif online_offline['type'] == 2:
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

    reserve_data = ReserveBasic.objects.filter(shop=shop).first()
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

    send_schedule = list()
    reception_data = list()
    week_schedule = list()
    week_time = list()
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
                    if online_offline['type'] == 1:
                        reception_place = ReceptionOfflinePlace.objects.filter(offline__id=online_offline['id'], reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=False).first()
                        reception_manager = ReceptionOfflineManager.objects.filter(offline__id=online_offline['id'], manager=manager, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                    if online_offline['type'] == 2:
                        reception_place = ReceptionOnlinePlace.objects.filter(online__id=online_offline['id'], reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=False).first()
                        reception_manager = ReceptionOnlineManager.objects.filter(online__id=online_offline['id'], manager=manager, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
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
                                                            if same_count > 0:
                                                                people_number = people_number + 1
                                                                facility_count = facility_count - 1
                                                                if facility_list[people_number]:
                                                                    people_count = people_count + facility_list[people_number].count
                                                            else:
                                                                people_count = reception['facility'].count
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
        if online_offline['type'] == 1:
            advance_setting = ReserveOfflineSetting.objects.filter(display_id=setting['advance']).first()
            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, offline=advance_setting).order_by('-number').first()
            if advance_schedule and advance_schedule.date and advance_schedule.time:
                advance_date = datetime.datetime(advance_schedule.date.year, advance_schedule.date.month, advance_schedule.date.day, advance_schedule.time.hour, advance_schedule.time.minute, 0)
                start_date = advance_date + datetime.timedelta(minutes=advance_setting.time)
        elif online_offline['type'] == 2:
            advance_setting = ReserveOfflineSetting.objects.filter(display_id=setting['advance']).first()
            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, online=advance_setting).order_by('-number').first()
            if advance_schedule and advance_schedule.date and advance_schedule.time:
                advance_date = datetime.datetime(advance_schedule.date.year, advance_schedule.date.month, advance_schedule.date.day, advance_schedule.time.hour, advance_schedule.time.minute, 0)
                start_date = advance_date + datetime.timedelta(minutes=advance_setting.time)

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
    if online_offline['type'] == 1:
        advance_setting = ReserveOfflineSetting.objects.filter(advance=setting['display_id']).first()
        advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, offline=advance_setting).first()
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
        advance_schedule = UserFlowSchedule.objects.filter(flow__user=user, online=advance_setting).first()
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
        'course': course,
        'setting': setting,
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
    }
    return JsonResponse( data, safe=False )

def question(request):
    question = UserQuestion.objects.filter(display_id=request.POST.get('question_id')).values(*get_model_field(UserQuestion)).first()
    question['item'] = list(UserQuestionItem.objects.filter(question=question['id']).order_by('number').values(*get_model_field(UserQuestionItem)).all())
    for question_item_index, question_item in enumerate(question['item']):
        if question_item['type'] == 99:
            question['item'][question_item_index]['choice'] = list(UserQuestionItemChoice.objects.filter(question=question_item['id']).order_by('number').values(*get_model_field(UserQuestionItemChoice)).all())
    question['age_list'] = [i for i in range(101)]
    return JsonResponse( question, safe=False )