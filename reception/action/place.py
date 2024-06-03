from django.db.models import Q
from django.http import JsonResponse

from flow.models import UserFlowSchedule
from reserve.models import (
    ReserveOfflineSetting, ReserveOnlineSetting, ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu,
    ReserveCalendarDate, ReserveCalendarTime, ReserveTempCalendar
)
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from setting.models import ShopOffline, ShopOnline, ShopOfflineTime, ShopOnlineTime
from sign.models import AuthLogin

from common import create_code, get_model_field

import datetime
import pandas
import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    setting = None
    if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
        setting = ShopOffline.objects.filter(display_id=request.POST.get("id")).first()
    if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
        setting = ShopOnline.objects.filter(display_id=request.POST.get("id")).first()

    for i in range(int(request.POST.get('day'))):
        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), (i+1))
        if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
            ReceptionOfflinePlace.objects.filter(offline=setting, reception_date__date=date).all().delete()
            for offline_setting in ReserveOfflineSetting.objects.filter(offline=setting).all():
                ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), offline=offline_setting).all().delete()
        if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
            ReceptionOnlinePlace.objects.filter(online=setting, reception_date__date=date).all().delete()
            for online_setting in ReserveOnlineSetting.objects.filter(online=setting).all():
                ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), online=online_setting).all().delete()

        flg = False
        if request.POST.get('setting_not_' + str(i+1)) == '1':
            flg = True
        count = 0
        number = 1
        for j in range(int(request.POST.get('setting_input_count_'+str(i+1)))):
            target = str(i+1) + '_' + str(j+1)
            if ( request.POST.get('setting_not_' + str(i+1)) == '1' and number == 1 ) or ( request.POST.get('setting_not_' + str(i+1)) == '0' and request.POST.get('setting_from_' + target) and request.POST.get('setting_to_' + target) ):
                if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
                    ReceptionOfflinePlace.objects.create(
                        id = str(uuid.uuid4()),
                        display_id = create_code(12, ReceptionOfflinePlace),
                        offline = setting,
                        number = number,
                        reception_date = date,
                        reception_from = request.POST.get('setting_from_' + target),
                        reception_to = request.POST.get('setting_to_' + target),
                        reception_count = count,
                        reception_flg = flg,
                    )
                if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
                    ReceptionOnlinePlace.objects.create(
                        id = str(uuid.uuid4()),
                        display_id = create_code(12, ReceptionOnlinePlace),
                        online = setting,
                        number = number,
                        reception_date = date,
                        reception_from = request.POST.get('setting_from_' + target),
                        reception_to = request.POST.get('setting_to_' + target),
                        reception_count = count,
                        reception_flg = flg,
                    )

                if flg:
                    ReserveCalendarDate.objects.filter(date=date).all().delete()
                    if datetime.datetime.now() < datetime.datetime(date.year, date.month, date.day, 23, 59, 59):
                        if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
                            for offline_setting in ReserveOfflineSetting.objects.filter(offline=setting).all():
                                ReserveCalendarDate.objects.create(
                                    id = str(uuid.uuid4()),
                                    shop = auth_login.shop,
                                    offline = offline_setting,
                                    date = date,
                                    flg = True,
                                )
                        if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
                            for online_setting in ReserveOnlineSetting.objects.filter(online=setting).all():
                                ReserveCalendarDate.objects.create(
                                    id = str(uuid.uuid4()),
                                    shop = auth_login.shop,
                                    online = online_setting,
                                    date = date,
                                    flg = True,
                                )
                else:
                    reception_data = list()
                    for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, int(request.POST.get('setting_from_' + target)[0:request.POST.get('setting_from_' + target).find(':')]), int(request.POST.get('setting_from_' + target)[request.POST.get('setting_from_' + target).find(':')+1:]), 0), end=datetime.datetime(date.year, date.month, date.day, int(request.POST.get('setting_to_' + target)[0:request.POST.get('setting_to_' + target).find(':')]), int(request.POST.get('setting_to_' + target)[request.POST.get('setting_to_' + target).find(':')+1:]), 0), freq='15min'):
                        schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
                            if schedule.join == 0 or schedule.join == 1:
                                date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                                temp_user = None
                                end_flg = False
                                if schedule.flow:
                                    end_flg = schedule.flow.end_flg
                                    temp_user = schedule.flow.user
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
                                        'temp_user': temp_user,
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
                                        'temp_user': temp_user,
                                        'temp_manager': schedule.temp_manager,
                                        'temp_flg': schedule.temp_flg,
                                    })
                    if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
                        for offline_setting in ReserveOfflineSetting.objects.filter(offline=setting).all():
                            manager_list = list()
                            facility_list = list()
                            for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=offline_setting).all():
                                manager_list.append(manager_menu_item.manager)
                            for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=offline_setting).order_by('facility__order').all():
                                facility_list.append(facility_menu_item.facility)

                            if datetime.datetime.now() < datetime.datetime(date.year, date.month, date.day, 23, 59, 59):
                                if ReserveCalendarDate.objects.filter(offline=offline_setting, date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0)).exists():
                                    reserve_calendar_date = ReserveCalendarDate.objects.filter(offline=offline_setting, date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0)).first()
                                else:
                                    reserve_calendar_date = ReserveCalendarDate.objects.create(
                                        id = str(uuid.uuid4()),
                                        shop = auth_login.shop,
                                        offline = offline_setting,
                                        date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                                        flg = False,
                                    )

                                for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, int(request.POST.get('setting_from_' + target)[0:request.POST.get('setting_from_' + target).find(':')]), int(request.POST.get('setting_from_' + target)[request.POST.get('setting_from_' + target).find(':')+1:]), 0), end=datetime.datetime(date.year, date.month, date.day, int(request.POST.get('setting_to_' + target)[0:request.POST.get('setting_to_' + target).find(':')]), int(request.POST.get('setting_to_' + target)[request.POST.get('setting_to_' + target).find(':')+1:]), 0), freq='15min'):
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
                                        reception_manager = ReceptionOfflineManager.objects.filter(offline=setting, manager=manager_item, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
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
                    
                    if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
                        for online_setting in ReserveOnlineSetting.objects.filter(online=setting).all():
                            manager_list = list()
                            facility_list = list()
                            for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=online_setting).all():
                                manager_list.append(manager_menu_item.manager)
                            for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=online_setting).order_by('facility__order').all():
                                facility_list.append(facility_menu_item.facility)

                            if datetime.datetime.now() < datetime.datetime(date.year, date.month, date.day, 23, 59, 59):
                                if ReserveCalendarDate.objects.filter(online=online_setting, date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0)).exists():
                                    reserve_calendar_date = ReserveCalendarDate.objects.filter(online=online_setting, date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0)).first()
                                else:
                                    reserve_calendar_date = ReserveCalendarDate.objects.create(
                                        id = str(uuid.uuid4()),
                                        shop = auth_login.shop,
                                        online = online_setting,
                                        date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                                        flg = False,
                                    )

                                for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, int(request.POST.get('setting_from_' + target)[0:request.POST.get('setting_from_' + target).find(':')]), int(request.POST.get('setting_from_' + target)[request.POST.get('setting_from_' + target).find(':')+1:]), 0), end=datetime.datetime(date.year, date.month, date.day, int(request.POST.get('setting_to_' + target)[0:request.POST.get('setting_to_' + target).find(':')]), int(request.POST.get('setting_to_' + target)[request.POST.get('setting_to_' + target).find(':')+1:]), 0), freq='15min'):
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
                                        reception_manager = ReceptionOnlineManager.objects.filter(online=setting, manager=manager_item, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
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
                number = number + 1
    return JsonResponse( {}, safe=False )

def save_check(request):
    check = True
    error_list = list()
    for i in range(int(request.POST.get('day'))):
        last_time = None
        for j in range(int(request.POST.get('setting_input_count_'+str(i+1)))):
            target = str(i+1) + '_' + str(j+1)
            if ( request.POST.get('setting_from_'+target) and request.POST.get('setting_to_'+target) ):
                if request.POST.get('setting_from_'+target) >= request.POST.get('setting_to_'+target) or ( last_time and last_time >= request.POST.get('setting_from_'+target)):
                    error_list.append(target)
                    check = False
                last_time = request.POST.get('setting_to_'+target)
            else:
                if request.POST.get('setting_from_'+target) or request.POST.get('setting_to_'+target):
                    error_list.append(target)
                    check = False
    return JsonResponse( {'check': check, 'error_list': error_list}, safe=False )



def get(request):
    setting = None
    if ShopOffline.objects.filter(display_id=request.POST.get("id")).exists():
        setting = ShopOffline.objects.filter(display_id=request.POST.get("id")).values(*get_model_field(ShopOffline)).first()
        setting['time'] = list(ShopOfflineTime.objects.filter(offline__id=setting['id']).order_by('week', 'number').values(*get_model_field(ShopOfflineTime)).all())
    if ShopOnline.objects.filter(display_id=request.POST.get("id")).exists():
        setting = ShopOnline.objects.filter(display_id=request.POST.get("id")).values(*get_model_field(ShopOnline)).first()
        setting['time'] = list(ShopOnlineTime.objects.filter(online__id=setting['id']).order_by('week', 'number').values(*get_model_field(ShopOnlineTime)).all())
    return JsonResponse( setting, safe=False )