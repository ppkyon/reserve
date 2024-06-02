from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse

from flow.models import UserFlowSchedule
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveCalendarDate, ReserveCalendarTime, ReserveTempCalendar,
    ReserveOfflineSetting, ReserveOnlineSetting, ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu
)
from setting.models import ShopOffline, ShopOnline, ManagerOffline, ManagerOfflineTime, ManagerOnline, ManagerOnlineTime
from sign.models import AuthUser, ManagerProfile, AuthLogin

from common import create_code, create_password

import datetime
import environ
import os
import pandas
import uuid

env = environ.Env()
env.read_env('.env')

def add(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    code = create_code(12, AuthUser)
    password = create_password()
    user = AuthUser.objects.create(
        id = str(uuid.uuid4()),
        display_id = code,
        company = auth_login.company,
        shop = auth_login.shop,
        email = 'atelle' + str(code) + '@atelle' + str(code) + '.jp',
        password = make_password(password),
        authority = request.POST.get("authority"),
        status = 1,
        author = request.user.id,
    )
    ManagerProfile.objects.create(
        id = str(uuid.uuid4()),
        manager = user,
        family_name = request.POST.get('family_name'),
        first_name = request.POST.get('first_name'),
        family_name_kana = request.POST.get('family_name_kana'),
        first_name_kana = request.POST.get('first_name_kana'),
        password = password,
    )
    
    return JsonResponse( {}, safe=False )

def add_check(request):
    return JsonResponse( {'check': True}, safe=False )

def save(request):
    manager = AuthUser.objects.filter(display_id=request.POST.get('id')).first()
    if ManagerProfile.objects.filter(manager=manager).exists():
        profile = ManagerProfile.objects.filter(manager=manager).first()
        profile.family_name = request.POST.get('family_name')
        profile.first_name = request.POST.get('first_name')
        profile.family_name_kana = request.POST.get('family_name_kana')
        profile.first_name_kana = request.POST.get('first_name_kana')
        profile.age = request.POST.get('age')
        profile.sex = request.POST.get('sex')
        profile.phone_number = request.POST.get('phone_number').replace('-', '')
        profile.department = request.POST.get('department')
        profile.job = request.POST.get('job')
        profile.work = request.POST.get('work')

        old_image = profile.image
        if "image_file" in request.FILES:
            profile.image = request.FILES['image_file']
        profile.save()

        if old_image and "image_file" in request.FILES:
            os.remove(old_image.url[1:])
            
        if request.POST.get('family_name') and request.POST.get('first_name') and ( manager.status == 2 or manager.status == 1 ):
            manager = AuthUser.objects.filter(id=manager.id).first()
            manager.status = 3
            manager.save()
        elif ( not request.POST.get('family_name') or not request.POST.get('first_name') ) and manager.status == 3:
            manager = AuthUser.objects.filter(id=manager.id).first()
            manager.status = 2
            manager.save()
    else:
        image = None
        if "image_file" in request.FILES:
            image = request.FILES['image_file']

        ManagerProfile.objects.create(
            id = str(uuid.uuid4()),
            manager = manager,
            family_name = request.POST.get('family_name'),
            first_name = request.POST.get('first_name'),
            family_name_kana = request.POST.get('family_name_kana'),
            first_name_kana = request.POST.get('first_name_kana'),
            image = image,
            age = request.POST.get('age'),
            sex = request.POST.get('sex'),
            phone_number = request.POST.get('phone_number').replace('-', ''),
            department = request.POST.get('department'),
            job = request.POST.get('job'),
            work = request.POST.get('work'),
        )

        if request.POST.get('family_name') and request.POST.get('first_name') and manager.status == 2:
            manager = AuthUser.objects.filter(id=manager.id).first()
            manager.status = 3
            manager.save()
    
    if request.POST.get('setting'):
        setting = None
        if ShopOffline.objects.filter(display_id=request.POST.get('setting')).exists():
            setting = ShopOffline.objects.filter(display_id=request.POST.get('setting')).first()
            if ManagerOffline.objects.filter(manager=manager, offline=setting).exists():
                setting = ManagerOffline.objects.filter(manager=manager, offline=setting).first()
            else:
                setting = ManagerOffline.objects.create(
                    id = str(uuid.uuid4()),
                    manager = manager,
                    offline = setting,
                )
            ManagerOfflineTime.objects.filter(offline=setting).all().delete()
            for i in range(8):
                number = 1
                for j in range(int(request.POST.get('time_count_'+str(i+1)))):
                    target = str(i+1) + '_' + str(j+1)
                    if ( request.POST.get('time_from_'+target) and request.POST.get('time_to_'+target) ) or ( request.POST.get('time_check_'+str(i+1)) == '1' and number == 1 ):
                        time_from = None
                        if request.POST.get('time_from_'+target):
                            time_from = request.POST.get('time_from_'+target)
                        time_to = None
                        if request.POST.get('time_to_'+target):
                            time_to = request.POST.get('time_to_'+target)
                        holiday_flg = False
                        if request.POST.get('time_check_'+str(i+1)) == '1':
                            holiday_flg = True
                        calendar_flg = False
                        if request.POST.get('calendar_check_'+str(i+1)) == '1':
                            calendar_flg = True

                        ManagerOfflineTime.objects.create(
                            id = str(uuid.uuid4()),
                            offline = setting,
                            week = i + 1,
                            number = number,
                            time_from = time_from,
                            time_to = time_to,
                            holiday_flg = holiday_flg,
                            calendar_flg = calendar_flg,
                        )
                        number = number + 1
        if ShopOnline.objects.filter(display_id=request.POST.get('interview')).exists():
            setting = ShopOnline.objects.filter(display_id=request.POST.get('setting')).first()
            if ManagerOnline.objects.filter(manager=manager, online=setting).exists():
                setting = ManagerOnline.objects.filter(manager=manager, online=setting).first()
            else:
                setting = ManagerOnline.objects.create(
                    id = str(uuid.uuid4()),
                    manager = manager,
                    online = setting,
                )
            ManagerOnlineTime.objects.filter(online=setting).all().delete()
            for i in range(8):
                number = 1
                for j in range(int(request.POST.get('time_count_'+str(i+1)))):
                    target = str(i+1) + '_' + str(j+1)
                    if ( request.POST.get('time_from_'+target) and request.POST.get('time_to_'+target) ) or ( request.POST.get('time_check_'+str(i+1)) == '1' and number == 1 ):
                        time_from = None
                        if request.POST.get('time_from_'+target):
                            time_from = request.POST.get('time_from_'+target)
                        time_to = None
                        if request.POST.get('time_to_'+target):
                            time_to = request.POST.get('time_to_'+target)
                        holiday_flg = False
                        if request.POST.get('time_check_'+str(i+1)) == '1':
                            holiday_flg = True
                        calendar_flg = False
                        if request.POST.get('calendar_check_'+str(i+1)) == '1':
                            calendar_flg = True

                        ManagerOnlineTime.objects.create(
                            id = str(uuid.uuid4()),
                            online = setting,
                            week = i + 1,
                            number = number,
                            time_from = time_from,
                            time_to = time_to,
                            holiday_flg = holiday_flg,
                            calendar_flg = calendar_flg,
                        )
                        number = number + 1
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def delete(request):
    manager = AuthUser.objects.filter(display_id=request.POST.get('id')).first()
    manager.delete_flg = True
    manager.save()

    ReserveOfflineManagerMenu.objects.filter(manager=manager).all().delete()
    ReserveOnlineManagerMenu.objects.filter(manager=manager).all().delete()
    for reception_offline_manager in ReceptionOfflineManager.objects.filter(manager=manager).all():
        ReceptionOfflineManagerSetting.objects.filter(manager=reception_offline_manager).all().delete()
    ReceptionOfflineManager.objects.filter(manager=manager).all().delete()
    for reception_online_manager in ReceptionOnlineManager.objects.filter(manager=manager).all():
        ReceptionOnlineManagerSetting.objects.filter(manager=reception_online_manager).all().delete()
    ReceptionOnlineManager.objects.filter(manager=manager).all().delete()

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
    ReserveCalendarDate.objects.exclude(Q(shop=auth_login.shop), Q(offline__display_id__in=offline_list)|Q(online__display_id__in=online_list)).all().delete()

    return JsonResponse( {}, safe=False )



def save_authority(request):
    manager = AuthUser.objects.filter(display_id=request.POST.get('id')).first()
    manager.authority = request.POST.get('authority')
    manager.save()
    return JsonResponse( {}, safe=False )