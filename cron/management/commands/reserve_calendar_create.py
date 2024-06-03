from django.core.management.base import BaseCommand
from django.db.models import Q

from flow.models import UserFlowSchedule
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveOfflineSetting, ReserveOnlineSetting, ReserveCalendarDate, ReserveCalendarTime, ReserveTempCalendar,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu
)
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthShop

import datetime
import pandas
import uuid

class Command(BaseCommand):
    def handle(self, *args, **options):
        ReserveCalendarDate.objects.all().delete()
        for shop in AuthShop.objects.filter(status__gte=2, delete_flg=False).all():
            for offline in ShopOffline.objects.filter(shop=shop).order_by('created_at').all():
                for offline_setting in ReserveOfflineSetting.objects.filter(offline=offline).all():
                    manager_list = list()
                    facility_list = list()
                    for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=offline_setting).all():
                        manager_list.append(manager_menu_item.manager)
                    for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=offline_setting).order_by('facility__order').all():
                        facility_list.append(facility_menu_item.facility)

                    all_date = ReserveCalendarDate.objects.filter(offline=offline_setting).order_by('date').all()
                    for all_date_item in ReceptionOfflinePlace.objects.filter(offline=offline, number=1).order_by('reception_date').all():
                        date = all_date_item.reception_date
                        if datetime.datetime(date.year, date.month, date.day, 23, 59, 59) >= datetime.datetime.now():
                            ReserveCalendarDate.objects.filter(date=date, offline=offline_setting).all().delete()
                            reserve_calendar_date = ReserveCalendarDate.objects.create(
                                id = str(uuid.uuid4()),
                                shop = shop,
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
                                        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
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
            
            for online in ShopOnline.objects.filter(shop=shop).order_by('created_at').all():
                for online_setting in ReserveOnlineSetting.objects.filter(online=online).all():
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
                                shop = shop,
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
                                        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
                                            if schedule.join == 0 or schedule.join == 1:
                                                date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                                                temp_user = None
                                                end_flg = False
                                                if schedule.flow:
                                                    end_flg = schedule.flow.end_flg
                                                    temp_user = schedule.flow.user
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
        self.stdout.write(self.style.SUCCESS('reserve calendar create successfully!!'))