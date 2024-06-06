from django.core.management.base import BaseCommand
from django.db.models import Q

from flow.models import UserFlowSchedule
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveCalendarDate, ReserveCalendarTime, ReserveTempCalendar, ReserveCalendarUpdate,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu
)

import datetime
import pandas
import uuid

class Command(BaseCommand):
    def handle(self, *args, **options):
        for reserve_calendar_update in ReserveCalendarUpdate.objects.filter(flg=True).order_by('created_at').all():
            if reserve_calendar_update.offline:
                manager_list = list()
                facility_list = list()

                for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=reserve_calendar_update.offline).all():
                    manager_list.append(manager_menu_item.manager)
                for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=reserve_calendar_update.offline).order_by('facility__order').all():
                    facility_list.append(facility_menu_item.facility)

                date = reserve_calendar_update.date
                if datetime.datetime(date.year, date.month, date.day, 23, 59, 59) >= datetime.datetime.now():
                    if ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), offline=reserve_calendar_update.offline).exists():
                        reserve_calendar_date = ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), offline=reserve_calendar_update.offline).first()
                    else:
                        reserve_calendar_date = ReserveCalendarDate.objects.create(
                            id = str(uuid.uuid4()),
                            shop = reserve_calendar_update.offline.offline.shop,
                            offline = reserve_calendar_update.offline,
                            date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                        )

                    time = {
                        'from': None,
                        'to': None
                    }
                    reception = ReceptionOfflinePlace.objects.filter(offline=reserve_calendar_update.offline.offline, reception_date__year=date.year, reception_date__month=date.month, reception_date__day=date.day).all()
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

                    if not reception_flg:
                        if not time['from'] or ( reception_from and time['from'] > reception_from ):
                            time['from'] = reception_from
                        if not time['to'] or ( reception_to and time['to'] < reception_to ):
                            time['to'] = reception_to

                    reserve_calendar_date.flg = reception_flg
                    reserve_calendar_date.save()

                    reception_data = list()
                    if not reception_flg:
                        for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, time['from'].hour, time['from'].minute, 0), end=datetime.datetime(date.year, date.month, date.day, time['to'].hour, time['to'].minute, 0), freq='15min'):
                            schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                            for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=reserve_calendar_update.offline.offline.shop)|Q(temp_manager__shop=reserve_calendar_update.offline.offline.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
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

                        for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, time['from'].hour, time['from'].minute, 0), end=datetime.datetime(date.year, date.month, date.day, time['to'].hour, time['to'].minute, 0), freq=str(reserve_calendar_update.offline.unit)+'min'):
                            schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                            
                            reception_flg = True
                            reception_manager_list = list()
                            reception_facility_list = list()
                            temp_manager_list = list()
                            temp_user_list = list()
                            manager_count = len(manager_list)
                            facility_count = len(facility_list)
                            schedule_datetime = datetime.datetime(times.year, times.month, times.day, times.hour, times.minute, 0)
                            schedule_datetime = schedule_datetime + datetime.timedelta(minutes=reserve_calendar_update.offline.time)
                            for manager_item in manager_list:
                                reception_manager = ReceptionOfflineManager.objects.filter(offline=reserve_calendar_update.offline.offline, manager=manager_item, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                                if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=reserve_calendar_update.offline).exists():
                                        reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=reserve_calendar_update.offline).first()
                                        if not reception_offline_manager_setting.flg:
                                            reception_manager = None
                                if reception_manager:
                                    if len(reception_data) > 0 :
                                        people_number = 0
                                        people_count = reserve_calendar_update.offline.people
                                        same_count = reserve_calendar_update.offline.facility

                                        schedule_date = datetime.datetime(times.year, times.month, times.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                        schedule_add_date = schedule_date + datetime.timedelta(minutes=reserve_calendar_update.offline.time)
                                        
                                        count_flg = True
                                        for reception in reception_data:
                                            if schedule_add_date > reception['from'] and reception['to'] > schedule_date:
                                                if manager_count <= 0 or facility_count <= 0:
                                                    break
                                                else:
                                                    if reception['setting']:
                                                        if reception['setting'].id == reserve_calendar_update.offline.id:
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
                                                                    people_count = reserve_calendar_update.offline.people
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
                                if ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).exists():
                                    reserve_calendar_time = ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).first()
                                    reserve_calendar_time.count = 0
                                    reserve_calendar_time.save()
                                else:
                                    reserve_calendar_time = ReserveCalendarTime.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_date,
                                        time = schedule_time,
                                        count = 0,
                                    )
                            else:
                                if manager_count < facility_count:
                                    if ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).exists():
                                        reserve_calendar_time = ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).first()
                                        reserve_calendar_time.count = manager_count
                                        reserve_calendar_time.save()
                                    else:
                                        reserve_calendar_time = ReserveCalendarTime.objects.create(
                                            id = str(uuid.uuid4()),
                                            calendar = reserve_calendar_date,
                                            time = schedule_time,
                                            count = manager_count,
                                        )
                                else:
                                    if ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).exists():
                                        reserve_calendar_time = ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).first()
                                        reserve_calendar_time.count = facility_count
                                        reserve_calendar_time.save()
                                    else:
                                        reserve_calendar_time = ReserveCalendarTime.objects.create(
                                            id = str(uuid.uuid4()),
                                            calendar = reserve_calendar_date,
                                            time = schedule_time,
                                            count = facility_count,
                                        )
                            ReserveTempCalendar.objects.filter(calendar=reserve_calendar_time).all().delete()
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
            elif reserve_calendar_update.online:
                manager_list = list()
                facility_list = list()
                for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=reserve_calendar_update.online).all():
                    manager_list.append(manager_menu_item.manager)
                for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=reserve_calendar_update.online).order_by('facility__order').all():
                    facility_list.append(facility_menu_item.facility)

                date = reserve_calendar_update.date
                if datetime.datetime(date.year, date.month, date.day, 23, 59, 59) > datetime.datetime.now():
                    if ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), online=reserve_calendar_update.online).exists():
                        reserve_calendar_date = ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), online=reserve_calendar_update.online).first()
                    else:
                        reserve_calendar_date = ReserveCalendarDate.objects.create(
                            id = str(uuid.uuid4()),
                            shop = reserve_calendar_update.online.online.shop,
                            online = reserve_calendar_update.online,
                            date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                        )

                    time = {
                        'from': None,
                        'to': None
                    }
                    reception = ReceptionOnlinePlace.objects.filter(online=reserve_calendar_update.online.online, reception_date__year=date.year, reception_date__month=date.month, reception_date__day=date.day).all()
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

                    if not reception_flg:
                        if not time['from'] or ( reception_from and time['from'] > reception_from ):
                            time['from'] = reception_from
                        if not time['to'] or ( reception_to and time['to'] < reception_to ):
                            time['to'] = reception_to
                            
                    reserve_calendar_date.flg = reception_flg
                    reserve_calendar_date.save()

                    reception_data = list()
                    if not reception_flg:
                        for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, time['from'].hour, time['from'].minute, 0), end=datetime.datetime(date.year, date.month, date.day, time['to'].hour, time['to'].minute, 0), freq='15min'):
                            schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                            for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=reserve_calendar_update.online.online.shop)|Q(temp_manager__shop=reserve_calendar_update.online.online.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
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

                        for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, time['from'].hour, time['from'].minute, 0), end=datetime.datetime(date.year, date.month, date.day, time['to'].hour, time['to'].minute, 0), freq=str(reserve_calendar_update.online.unit)+'min'):
                            schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                            
                            reception_flg = True
                            reception_manager_list = list()
                            reception_facility_list = list()
                            temp_manager_list = list()
                            temp_user_list = list()
                            manager_count = len(manager_list)
                            facility_count = len(facility_list)
                            schedule_datetime = datetime.datetime(times.year, times.month, times.day, times.hour, times.minute, 0)
                            schedule_datetime = schedule_datetime + datetime.timedelta(minutes=reserve_calendar_update.online.time)
                            for manager_item in manager_list:
                                reception_manager = ReceptionOnlineManager.objects.filter(online=reserve_calendar_update.online.online, manager=manager_item, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                                if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=reserve_calendar_update.online).exists():
                                        reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=reserve_calendar_update.online).first()
                                        if not reception_online_manager_setting.flg:
                                            reception_manager = None
                                if reception_manager:
                                    if len(reception_data) > 0 :
                                        people_number = 0
                                        people_count = reserve_calendar_update.online.people
                                        same_count = reserve_calendar_update.online.facility

                                        schedule_date = datetime.datetime(times.year, times.month, times.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                        schedule_add_date = schedule_date + datetime.timedelta(minutes=reserve_calendar_update.online.time)
                                        
                                        count_flg = True
                                        for reception in reception_data:
                                            if schedule_add_date > reception['from'] and reception['to'] > schedule_date:
                                                if manager_count <= 0 or facility_count <= 0:
                                                    break
                                                else:
                                                    if reception['setting']:
                                                        if reception['setting'].id == reserve_calendar_update.online.id:
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
                                                                    people_count = reserve_calendar_update.online.people
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
            reserve_calendar_update.delete()
        self.stdout.write(self.style.SUCCESS('reserve calendar create successfully!!'))