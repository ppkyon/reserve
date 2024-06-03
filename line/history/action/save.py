from django.db.models import Q
from django.http import JsonResponse

from flow.models import UserFlow, UserFlowSchedule
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflineSetting, ReserveOnlineSetting, ReserveCalendarDate, ReserveCalendarTime, ReserveTempCalendar,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu
)
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthShop
from user.models import LineUser

from common import create_code

import datetime
import pandas
import uuid

def temp(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).first()
    if request.POST.get('setting_id'):
        if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
            setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
            people_count = setting.people
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

            schedule_list = list()
            for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day'), temp_flg=False).exclude(Q(number=0)|Q(join=2)).all():
                schedule_list.append(schedule)

            date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
            add_date = date + datetime.timedelta(minutes=setting.time)

            reception_manager_list = list()
            reception_facility_list = list()
            for schedule_item in schedule_list:
                schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
                schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.offline.time)

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
                            if schedule_item and schedule_item.manager:
                                reception_manager_list.append(schedule_item.manager.id)
                            if schedule_item and schedule_item.offline_facility:
                                reception_facility_list.append(schedule_item.offline_facility.id)
                    else:
                        if schedule_item and schedule_item.manager:
                            reception_manager_list.append(schedule_item.manager.id)
                        if schedule_item and schedule_item.offline_facility:
                            reception_facility_list.append(schedule_item.offline_facility.id)
            
            manager = None
            for manager_item in ReserveOfflineManagerMenu.objects.filter(shop=shop, offline=setting).order_by('manager__created_at').all():
                reception_manager = ReceptionOfflineManager.objects.filter(offline=setting.offline, manager=manager_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).exists():
                            reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).first()
                            if reception_offline_manager_setting.flg:
                                if not manager_item.manager.id in reception_manager_list:
                                    manager = manager_item.manager
                                    break
                        else:
                            if not manager_item.manager.id in reception_manager_list:
                                manager = manager_item.manager
                                break
                    else:
                        if not manager_item.manager.id in reception_manager_list:
                            manager = manager_item.manager
                            break
            facility = None
            for facility_item in ReserveOfflineFacilityMenu.objects.filter(shop=shop, offline=setting).order_by('facility__order').all():
                if not facility_item.facility.id in reception_facility_list:
                    facility = facility_item.facility
                    break
                
            course = None
            if request.POST.get('course_id'):
                course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()

            user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user, name=setting.name).first()
            temp_schedule = UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).first()
            UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).all().delete()
            UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                flow = user_flow,
                number = 0,
                date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
                time = request.POST.get('hour') + ':' + request.POST.get('minute'),
                join = 0,
                offline = setting,
                offline_course = course,
                offline_facility = facility,
                manager = manager,
                temp_flg = True,
            )

            for offline in ShopOffline.objects.filter(shop=shop).order_by('created_at').all():
                for offline_setting in ReserveOfflineSetting.objects.filter(offline=offline).all():
                    manager_list = list()
                    facility_list = list()
                    for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=offline_setting).all():
                        manager_list.append(manager_menu_item.manager)
                    for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=offline_setting).order_by('facility__order').all():
                        facility_list.append(facility_menu_item.facility)

                    for i in range(2):
                        if i == 1:
                            if temp_schedule and temp_schedule.date:
                                date = datetime.datetime(temp_schedule.date.year, temp_schedule.date.month, temp_schedule.date.day, temp_schedule.time.hour, temp_schedule.time.minute, 0)
                            else:
                                continue
                        if not date:
                            continue
                        ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), offline=offline_setting).all().delete()
                        reserve_calendar_date = ReserveCalendarDate.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            offline = offline_setting,
                            date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                        )

                        for reception_offline_place in ReceptionOfflinePlace.objects.filter(offline=offline, reception_date__year=date.year, reception_date__month=date.month, reception_date__day=date.day).all():
                            reception_data = list()
                            reserve_calendar_date.flg = reception_offline_place.reception_flg
                            reserve_calendar_date.save()
                            if not reception_offline_place.reception_flg:
                                for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_from.hour, reception_offline_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_to.hour, reception_offline_place.reception_to.minute, 0), freq='15min'):
                                    schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                    for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
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
        if ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
            setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()

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
            
            schedule_list = list()
            for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day'), temp_flg=False).exclude(Q(number=0)|Q(join=2)).all():
                schedule_list.append(schedule)

            date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
            add_date = date + datetime.timedelta(minutes=setting.time)

            reception_manager_list = list()
            reception_facility_list = list()
            for schedule_item in schedule_list:
                schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
                schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.online.time)

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
                            if schedule_item and schedule_item.manager:
                                reception_manager_list.append(schedule_item.manager.id)
                            if schedule_item and schedule_item.offline_facility:
                                reception_facility_list.append(schedule_item.offline_facility.id)
                    else:
                        if schedule_item and schedule_item.manager:
                            reception_manager_list.append(schedule_item.manager.id)
                        if schedule_item and schedule_item.offline_facility:
                            reception_facility_list.append(schedule_item.offline_facility.id)

            manager = None
            for manager_item in ReserveOnlineManagerMenu.objects.filter(shop=shop, online=setting).order_by('manager__created_at').all():
                reception_manager = ReceptionOnlineManager.objects.filter(online=setting.online, manager=manager_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).exists():
                            reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).first()
                            if reception_online_manager_setting.flg:
                                if not manager_item.manager.id in reception_manager_list:
                                    manager = manager_item.manager
                                    break
                        else:
                            if not manager_item.manager.id in reception_manager_list:
                                manager = manager_item.manager
                                break
                    else:
                        if not manager_item.manager.id in reception_manager_list:
                            manager = manager_item.manager
                            break
            facility = None
            for facility_item in ReserveOnlineFacilityMenu.objects.filter(shop=shop, online=setting).all():
                if not facility_item.facility in reception_facility_list:
                    facility = facility_item.facility
                    break
            
            course = None
            if request.POST.get('course_id'):
                course = ReserveOnlineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
            
            user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user).first()
            temp_schedule = UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).first()
            UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).all().delete()
            UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                flow = user_flow,
                number = 0,
                date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
                time = request.POST.get('hour') + ':' + request.POST.get('minute'),
                join = 0,
                online = setting,
                online_course = course,
                online_facility = facility,
                manager = manager,
                temp_flg = True,
            )

            for online in ShopOnline.objects.filter(shop=shop).order_by('created_at').all():
                for online_setting in ReserveOnlineSetting.objects.filter(online=online).all():
                    manager_list = list()
                    facility_list = list()
                    for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=online_setting).all():
                        manager_list.append(manager_menu_item.manager)
                    for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=online_setting).order_by('facility__order').all():
                        facility_list.append(facility_menu_item.facility)

                    for i in range(2):
                        if i == 1:
                            if temp_schedule and temp_schedule.date:
                                date = datetime.datetime(temp_schedule.date.year, temp_schedule.date.month, temp_schedule.date.day, temp_schedule.time.hour, temp_schedule.time.minute, 0)
                            else:
                                continue
                        if not date:
                            continue
                        ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), online=online_setting).all().delete()
                        reserve_calendar_date = ReserveCalendarDate.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            online = online_setting,
                            date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                        )

                        for reception_online_place in ReceptionOnlinePlace.objects.filter(online=online, reception_date__year=date.year, reception_date__month=date.month, reception_date__day=date.day).all():
                            reception_data = list()
                            reserve_calendar_date.flg = reception_online_place.reception_flg
                            reserve_calendar_date.save()
                            if not reception_online_place.reception_flg:
                                for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_from.hour, reception_online_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_to.hour, reception_online_place.reception_to.minute, 0), freq='15min'):
                                    schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                    for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
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
    return JsonResponse( {}, safe=False )