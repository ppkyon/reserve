from django.db.models import Q
from django.http import JsonResponse

from flow.models import UserFlowSchedule
from question.models import ShopQuestion
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveOfflineSetting, ReserveOnlineSetting, ReserveOnlineMeeting, ReserveCalendarDate, ReserveCalendarTime, ReserveTempCalendar,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu
)
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthLogin

from common import create_code

import datetime
import pandas
import uuid

def save(request):
    random_list = list()
    for i in range(int(request.POST.get('count'))):
        random_list.append(request.POST.get('random_'+str( i + 1 )))

    for delete_item in ReserveOnlineSetting.objects.filter(online=ShopOnline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all():
        ReserveOnlineMeeting.objects.filter(online=delete_item).all().delete()
    ReserveOnlineSetting.objects.filter(online=ShopOnline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all().delete()
    ReserveOfflineSetting.objects.filter(offline=ShopOffline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all().delete()
    
    change_list = list()
    for i in range(int(request.POST.get('count'))):
        if request.POST.get('course_flg_'+str(i+1)) == '1':
            course_flg = True
        else:
            course_flg = False
        if request.POST.get('display_flg_'+str(i+1)) == '1':
            display_flg = True
        else:
            display_flg = False

        question = None
        if request.POST.get('question_'+str(i+1)):
            question = ShopQuestion.objects.filter(display_id=request.POST.get('question_'+str(i+1))).first()

        if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('random_'+str(i+1))).exists():
            offline = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('random_'+str(i+1))).first()
            offline.number = ( i + 1 )
            offline.title = request.POST.get('title_'+str( i + 1 ))
            offline.name = request.POST.get('name_'+str( i + 1 ))
            offline.outline = request.POST.get('outline_'+str( i + 1 ))
            offline.note = request.POST.get('note_'+str( i + 1 ))
            offline.time = request.POST.get('time_'+str( i + 1 ))
            offline.people = request.POST.get('people_'+str( i + 1 ))
            offline.facility = request.POST.get('facility_'+str( i + 1 ))
            offline.question = question
            offline.advance = request.POST.get('advance_'+str( i + 1 ))
            offline.unit = request.POST.get('unit_'+str( i + 1 ))
            offline.course_flg = course_flg
            offline.display_flg = display_flg
            offline.save()
        elif ReserveOnlineSetting.objects.filter(display_id=request.POST.get('random_'+str(i+1))).exists():
            online = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('random_'+str(i+1))).first()
            online.number = ( i + 1 )
            online.title = request.POST.get('title_'+str( i + 1 ))
            online.name = request.POST.get('name_'+str( i + 1 ))
            online.outline = request.POST.get('outline_'+str( i + 1 ))
            online.note = request.POST.get('note_'+str( i + 1 ))
            online.time = request.POST.get('time_'+str( i + 1 ))
            online.people = request.POST.get('people_'+str( i + 1 ))
            online.facility = request.POST.get('facility_'+str( i + 1 ))
            online.question = question
            online.advance = request.POST.get('advance_'+str( i + 1 ))
            online.unit = request.POST.get('unit_'+str( i + 1 ))
            online.course_flg = course_flg
            online.display_flg = display_flg
            online.save()

            ReserveOnlineMeeting.objects.filter(online=online).all().delete()
            for j in range(int(request.POST.get('meeting_count_'+str( i + 1 )))):
                platform_text = None
                if request.POST.get('meeting_platform_text_'+str( i + 1 )+'_'+str( j + 1 )):
                    platform_text = request.POST.get('meeting_platform_text_'+str( i + 1 )+'_'+str( j + 1 ))
                
                start_data = None
                expiration_date = None
                if request.POST.get('meeting_start_'+str( i + 1 )+'_'+str( j + 1 )):
                    start_data = datetime.datetime.strptime(request.POST.get('meeting_start_'+str( i + 1 )+'_'+str( j + 1 )), '%Y/%m/%d')
                    expiration_date = start_data + datetime.timedelta(days=90)
                
                ReserveOnlineMeeting.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOnlineMeeting),
                    online = online,
                    number = ( j + 1 ),
                    name = request.POST.get('meeting_name_'+str( i + 1 )+'_'+str( j + 1 )),
                    url = request.POST.get('meeting_url_'+str( i + 1 )+'_'+str( j + 1 )),
                    platform = request.POST.get('meeting_platform_'+str( i + 1 )+'_'+str( j + 1 )),
                    platform_text = platform_text,
                    start_date = start_data,
                    expiration_date = expiration_date,
                    status = request.POST.get('meeting_status_'+str( i + 1 )+'_'+str( j + 1 )),
                    author = request.user.display_id,
                )
        else:
            if ShopOffline.objects.filter(display_id=request.POST.get('id')).exists():
                offline = ReserveOfflineSetting.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOfflineSetting),
                    offline = ShopOffline.objects.filter(display_id=request.POST.get('id')).first(),
                    number = ( i + 1 ),
                    title = request.POST.get('title_'+str( i + 1 )),
                    name = request.POST.get('name_'+str( i + 1 )),
                    outline = request.POST.get('outline_'+str( i + 1 )),
                    note = request.POST.get('note_'+str( i + 1 )),
                    time = request.POST.get('time_'+str( i + 1 )),
                    people = request.POST.get('people_'+str( i + 1 )),
                    facility = request.POST.get('facility_'+str( i + 1 )),
                    question = question,
                    advance = request.POST.get('advance_'+str( i + 1 )),
                    course_flg = course_flg,
                    display_flg = display_flg,
                )
                change_list.append({
                    'random': request.POST.get('random_'+str(i+1)),
                    'id': offline.display_id,
                })
            if ShopOnline.objects.filter(display_id=request.POST.get('id')).exists():
                online = ReserveOnlineSetting.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOfflineSetting),
                    online = ShopOnline.objects.filter(display_id=request.POST.get('id')).first(),
                    number = ( i + 1 ),
                    title = request.POST.get('title_'+str( i + 1 )),
                    name = request.POST.get('name_'+str( i + 1 )),
                    outline = request.POST.get('outline_'+str( i + 1 )),
                    note = request.POST.get('note_'+str( i + 1 )),
                    time = request.POST.get('time_'+str( i + 1 )),
                    people = request.POST.get('people_'+str( i + 1 )),
                    facility = request.POST.get('facility_'+str( i + 1 )),
                    question = question,
                    advance = request.POST.get('advance_'+str( i + 1 )),
                    course_flg = course_flg,
                    display_flg = display_flg,
                )
                change_list.append({
                    'random': request.POST.get('random_'+str(i+1)),
                    'id': online.display_id,
                })
                for j in range(int(request.POST.get('meeting_count_'+str( i + 1 )))):
                    platform_text = None
                    if request.POST.get('meeting_platform_text_'+str( i + 1 )+'_'+str( j + 1 )):
                        platform_text = request.POST.get('meeting_platform_text_'+str( i + 1 )+'_'+str( j + 1 ))
                    
                    start_data = None
                    expiration_date = None
                    if request.POST.get('meeting_start_'+str( i + 1 )+'_'+str( j + 1 )):
                        start_data = datetime.datetime.strptime(request.POST.get('meeting_start_'+str( i + 1 )+'_'+str( j + 1 )), '%Y/%m/%d')
                        expiration_date = start_data + datetime.timedelta(days=90)
                    
                    ReserveOnlineMeeting.objects.create(
                        id = str(uuid.uuid4()),
                        display_id = create_code(12, ReserveOnlineMeeting),
                        online = online,
                        number = ( j + 1 ),
                        name = request.POST.get('meeting_name_'+str( i + 1 )+'_'+str( j + 1 )),
                        url = request.POST.get('meeting_url_'+str( i + 1 )+'_'+str( j + 1 )),
                        platform = request.POST.get('meeting_platform_'+str( i + 1 )+'_'+str( j + 1 )),
                        platform_text = platform_text,
                        start_date = start_data,
                        expiration_date = expiration_date,
                        status = request.POST.get('meeting_status_'+str( i + 1 )+'_'+str( j + 1 )),
                        author = request.user.display_id,
                    )
    
    for change_item in change_list:
        for offline in ReserveOfflineSetting.objects.filter(advance=change_item['random']).all():
            offline.advance = change_item['id']
            offline.save()
        for online in ReserveOnlineSetting.objects.filter(advance=change_item['random']).all():
            online.advance = change_item['id']
            online.save()
    
    offline_list = list()
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    for offline in ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all():
        for offline_setting in ReserveOfflineSetting.objects.filter(offline=offline).all():
            offline_list.append(offline_setting.display_id)
            manager_list = list()
            facility_list = list()
            for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=offline_setting).all():
                manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=offline_setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)

            all_date = ReserveCalendarDate.objects.filter(offline=offline_setting).order_by('date').all()
            for all_date_item in all_date:
                date = all_date_item.date
                if datetime.datetime(date.year, date.month, date.day, 23, 59, 59) > datetime.datetime.now():
                    ReserveCalendarDate.objects.filter(date=date, offline=offline_setting).all().delete()
                    reserve_calendar_date = ReserveCalendarDate.objects.create(
                        id = str(uuid.uuid4()),
                        shop = auth_login.shop,
                        offline = offline_setting,
                        date = date,
                    )

                    for reception_offline_place in ReceptionOfflinePlace.objects.filter(offline=offline, reception_date__year=date.year, reception_date__month=date.month, reception_date__day=date.day).all():
                        reception_data = list()
                        reserve_calendar_date.flg = reception_offline_place.reception_flg
                        reserve_calendar_date.save()
                        if not reception_offline_place.reception_flg:
                            for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_from.hour, reception_offline_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_to.hour, reception_offline_place.reception_to.minute, 0), freq='15min'):
                                schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
                                    if schedule.join == 0 or schedule.join == 1:
                                        date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                                        end_flg = False
                                        if schedule.flow:
                                            end_flg = schedule.flow.end_flg
                                        if schedule.offline:
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
                                                'temp_user': schedule.flow.user,
                                                'temp_manager': schedule.temp_manager,
                                                'temp_flg': schedule.temp_flg,
                                            })
                                        elif schedule.online:
                                            reception_data.append({
                                                'from': date,
                                                'to': date + datetime.timedelta(minutes=schedule.online.time),
                                                'setting': schedule.online,
                                                'course': schedule.online_course,
                                                'facility': schedule.online_facility,
                                                'manager': schedule.manager,
                                                'question': schedule.question,
                                                'meeting': None,
                                                'end_flg': end_flg,
                                                'temp_user': schedule.flow.user,
                                                'temp_manager': schedule.temp_manager,
                                                'temp_flg': schedule.temp_flg,
                                            })

                            for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_from.hour, reception_offline_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_to.hour, reception_offline_place.reception_to.minute, 0), freq='15min'):
                                schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                
                                reception_flg = True
                                reception_manager_list = list()
                                reception_facility_list = list()
                                temp_manager_list = list()
                                temp_user_list = list()
                                manager_count = len(manager_list)
                                facility_count = len(facility_list)
                                schedule_datetime = datetime.datetime(times.year, times.month, times.day, times.hour, times.minute, 0)
                                schedule_datetime = schedule_datetime + datetime.timedelta(minutes=offline_setting.time)
                                for manager_item in manager_list:
                                    reception_manager = ReceptionOfflineManager.objects.filter(offline=offline, manager=manager_item, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=offline_setting).exists():
                                            reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=offline_setting).first()
                                            if not reception_offline_manager_setting.flg:
                                                reception_manager = None
                                    if reception_manager:
                                        if len(reception_data) > 0 :
                                            people_number = 0
                                            people_count = offline_setting.people
                                            same_count = offline_setting.facility

                                            schedule_date = datetime.datetime(times.year, times.month, times.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                            schedule_add_date = schedule_date + datetime.timedelta(minutes=offline_setting.time)
                                            
                                            count_flg = True
                                            for reception in reception_data:
                                                if schedule_add_date > reception['from'] and reception['to'] > schedule_date:
                                                    if manager_count <= 0 or facility_count <= 0:
                                                        break
                                                    else:
                                                        if reception['setting']:
                                                            if reception['setting'].id == offline_setting.id:
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
                                                                        people_count = offline_setting.people
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
                                                    if reception['temp_flg']:
                                                        if reception['temp_manager']:
                                                            temp_manager_list.append(reception['temp_manager'])
                                                        else:
                                                            temp_user_list.append(reception['temp_user'])
                                            if manager_count > 0 and facility_count > 0:
                                                reception_flg = False
                                        else:
                                            schedule_date = datetime.datetime(date.year, date.month, date.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                            if manager_count > 0 and facility_count > 0:
                                                reception_flg = False
                                    else:
                                        if not manager_item in reception_manager_list:
                                            manager_count = manager_count - 1
                                            reception_manager_list.append(manager_item)
                                if manager_count <= 0 or facility_count <= 0:
                                    reception_flg = True
                                
                                if reception_flg:
                                    reserve_calendar_time = ReserveCalendarTime.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_date,
                                        time = schedule_time,
                                        count = 0,
                                    )
                                else:
                                    if manager_count < facility_count:
                                        reserve_calendar_time = ReserveCalendarTime.objects.create(
                                            id = str(uuid.uuid4()),
                                            calendar = reserve_calendar_date,
                                            time = schedule_time,
                                            count = manager_count,
                                        )
                                    else:
                                        reserve_calendar_time = ReserveCalendarTime.objects.create(
                                            id = str(uuid.uuid4()),
                                            calendar = reserve_calendar_date,
                                            time = schedule_time,
                                            count = facility_count,
                                        )
                                for temp_manager in temp_manager_list:
                                    ReserveTempCalendar.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_time,
                                        user = None,
                                        manager = temp_manager,
                                    )
                                for temp_user in temp_user_list:
                                    ReserveTempCalendar.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_time,
                                        user = temp_user,
                                        manager = None,
                                    )
    
    online_list = list()
    for online in ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all():
        for online_setting in ReserveOnlineSetting.objects.filter(online=online).all():
            online_list.append(offline_setting.display_id)
            manager_list = list()
            facility_list = list()
            for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=online_setting).all():
                manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=online_setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)

            all_date = ReserveCalendarDate.objects.filter(online=online_setting).all()
            for all_date_item in all_date:
                date = all_date_item.date
                if datetime.datetime(date.year, date.month, date.day, 23, 59, 59) > datetime.datetime.now():
                    ReserveCalendarDate.objects.filter(date=date, online=online_setting).all().delete()
                    reserve_calendar_date = ReserveCalendarDate.objects.create(
                        id = str(uuid.uuid4()),
                        shop = auth_login.shop,
                        online = online_setting,
                        date = date,
                    )

                    for reception_online_place in ReceptionOnlinePlace.objects.filter(online=online, reception_date__year=date.year, reception_date__month=date.month, reception_date__day=date.day).all():
                        reception_data = list()
                        reserve_calendar_date.flg = reception_online_place.reception_flg
                        reserve_calendar_date.save()
                        if not reception_online_place.reception_flg:
                            for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_from.hour, reception_online_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_to.hour, reception_online_place.reception_to.minute, 0), freq='15min'):
                                schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
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
                                                'meeting': None,
                                                'end_flg': end_flg,
                                                'temp_user': schedule.flow.user,
                                                'temp_manager': schedule.temp_manager,
                                                'temp_flg': schedule.temp_flg,
                                            })
                                        elif schedule.online:
                                            reception_data.append({
                                                'from': date,
                                                'to': date + datetime.timedelta(minutes=schedule.online.time),
                                                'setting': schedule.online,
                                                'course': schedule.online_course,
                                                'facility': schedule.online_facility,
                                                'manager': schedule.manager,
                                                'question': schedule.question,
                                                'meeting': None,
                                                'end_flg': end_flg,
                                                'temp_user': schedule.flow.user,
                                                'temp_manager': schedule.temp_manager,
                                                'temp_flg': schedule.temp_flg,
                                            })

                            for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_from.hour, reception_online_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_to.hour, reception_online_place.reception_to.minute, 0), freq='15min'):
                                schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                
                                reception_flg = True
                                reception_manager_list = list()
                                reception_facility_list = list()
                                temp_manager_list = list()
                                temp_user_list = list()
                                manager_count = len(manager_list)
                                facility_count = len(facility_list)
                                schedule_datetime = datetime.datetime(times.year, times.month, times.day, times.hour, times.minute, 0)
                                schedule_datetime = schedule_datetime + datetime.timedelta(minutes=online_setting.time)
                                for manager_item in manager_list:
                                    reception_manager = ReceptionOnlineManager.objects.filter(online=online, manager=manager_item, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=online_setting).exists():
                                            reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=online_setting).first()
                                            if not reception_online_manager_setting.flg:
                                                reception_manager = None
                                    if reception_manager:
                                        if len(reception_data) > 0 :
                                            people_number = 0
                                            people_count = online_setting.people
                                            same_count = online_setting.facility

                                            schedule_date = datetime.datetime(times.year, times.month, times.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                            schedule_add_date = schedule_date + datetime.timedelta(minutes=online_setting.time)
                                            
                                            count_flg = True
                                            for reception in reception_data:
                                                if schedule_add_date > reception['from'] and reception['to'] > schedule_date:
                                                    if manager_count <= 0 or facility_count <= 0:
                                                        break
                                                    else:
                                                        if reception['setting']:
                                                            if reception['setting'].id == online_setting.id:
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
                                                                        people_count = online_setting.people
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
                                                    if reception['temp_flg']:
                                                        if reception['temp_manager']:
                                                            temp_manager_list.append(reception['temp_manager'])
                                                        else:
                                                            temp_user_list.append(reception['temp_user'])
                                            if manager_count > 0 and facility_count > 0:
                                                reception_flg = False
                                        else:
                                            schedule_date = datetime.datetime(date.year, date.month, date.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                            if manager_count > 0 and facility_count > 0:
                                                reception_flg = False
                                    else:
                                        if not manager_item in reception_manager_list:
                                            manager_count = manager_count - 1
                                            reception_manager_list.append(manager_item)
                                if manager_count <= 0 or facility_count <= 0:
                                    reception_flg = True
                                
                                if reception_flg:
                                    reserve_calendar_time = ReserveCalendarTime.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_date,
                                        time = schedule_time,
                                        count = 0,
                                    )
                                else:
                                    if manager_count < facility_count:
                                        reserve_calendar_time = ReserveCalendarTime.objects.create(
                                            id = str(uuid.uuid4()),
                                            calendar = reserve_calendar_date,
                                            time = schedule_time,
                                            count = manager_count,
                                        )
                                    else:
                                        reserve_calendar_time = ReserveCalendarTime.objects.create(
                                            id = str(uuid.uuid4()),
                                            calendar = reserve_calendar_date,
                                            time = schedule_time,
                                            count = facility_count,
                                        )
                                for temp_manager in temp_manager_list:
                                    ReserveTempCalendar.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_time,
                                        user = None,
                                        manager = temp_manager,
                                    )
                                for temp_user in temp_user_list:
                                    ReserveTempCalendar.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_time,
                                        user = temp_user,
                                        manager = None,
                                    )
    ReserveCalendarDate.objects.filter(Q(shop=auth_login.shop)).exclude(Q(offline__display_id__in=offline_list)|Q(online__display_id__in=online_list)).all().delete()

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )