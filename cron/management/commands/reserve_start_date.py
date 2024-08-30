from django.core.management.base import BaseCommand

from flow.models import UserFlowSchedule
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveBasic, ReserveOfflineSetting, ReserveOnlineSetting, ReserveOfflineCourse, ReserveOnlineCourse, ReserveStartDate,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu
)
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthShop

import datetime
import environ
import pandas
import uuid

env = environ.Env()
env.read_env('.env')

class Command(BaseCommand):
    def handle(self, *args, **options):
        for shop in AuthShop.objects.filter(status__gte=2, delete_flg=False).all():
            current_date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            reserve_basic = ReserveBasic.objects.filter(shop=shop).first()
                
            for shop_offline in ShopOffline.objects.filter(shop=shop).order_by('created_at').all():
                for offline in ReserveOfflineSetting.objects.filter(offline=shop_offline).order_by('number').all():
                    manager_list = list()
                    for reserve_manager in ReserveOfflineManagerMenu.objects.filter(offline=offline).all():
                        manager_list.append(reserve_manager.manager)
                    facility_list = list()
                    for reserve_facility in ReserveOfflineFacilityMenu.objects.filter(offline=offline).order_by('facility__order').all():
                        facility_list.append(reserve_facility.facility)

                    start_date = current_date
                    if offline.course_flg:
                        for course in ReserveOfflineCourse.objects.filter(shop=shop).all():
                            if course.deadline == 2 and course.any_day and course.any_day != 0 and course.any_time and course.any_time != 0:
                                if course.method == 0 or course.method == 1:
                                    start_date = start_date + datetime.timedelta(days=course.any_day)
                                elif course.method == 2:
                                    if course.business_mon_day or course.business_tue_day or course.business_wed_day or course.business_thu_day or course.business_fri_day or course.business_sat_day or course.business_sun_day:
                                        count_date = start_date
                                        count = course.any_day
                                        while count > 0:
                                            count_date = count_date + datetime.timedelta(days=1)
                                            if count_date.weekday() == 0:
                                                if course.business_mon_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 1:
                                                if course.business_tue_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 2:
                                                if course.business_wed_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 3:
                                                if course.business_thu_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 4:
                                                if course.business_fri_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 5:
                                                if course.business_sat_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 6:
                                                if course.business_sun_day:
                                                    count = count - 1
                                        start_date = datetime.datetime(count_date.year, count_date.month, count_date.day, 0, 0, 0)
                                    else:
                                        start_date = start_date + datetime.timedelta(days=course.any_day)
                            end_date = None
                            if course and course.start != 0:
                                end_date = current_date +  datetime.timedelta(days=(course.start*7)+1)

                            first_date = None
                            second_date = None
                            for i in range((end_date - start_date).days + 1):
                                target = start_date + datetime.timedelta(i)

                                time_list = list()
                                reception_list = list()
                                for reception_place in ReceptionOfflinePlace.objects.filter(offline=shop_offline, reception_date__year=target.year, reception_date__month=target.month, reception_date__day=target.day).all():
                                    if not reception_place.reception_flg:
                                        for time in pandas.date_range(start=datetime.datetime(target.year, target.month, target.day, reception_place.reception_from.hour, reception_place.reception_from.minute, 0), end=datetime.datetime(target.year, target.month, target.day, reception_place.reception_to.hour, reception_place.reception_to.minute, 0), freq=str(offline.unit)+'min'):
                                            time_list.append(time)
                                        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=shop, date__year=target.year, date__month=target.month, date__day=target.day, time__gte=datetime.time(reception_place.reception_from.hour, reception_place.reception_from.minute, 0), time__lte=datetime.time(reception_place.reception_to.hour, reception_place.reception_to.minute, 0), temp_flg=False).exclude(number=0).all():
                                            if schedule.join == 0 or schedule.join == 1:
                                                schedule_date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                                                reception_list.append({
                                                    'from': schedule_date,
                                                    'to': schedule_date + datetime.timedelta(minutes=offline.time),
                                                    'setting': schedule.offline,
                                                    'manager': schedule.manager,
                                                    'facility': schedule.offline_facility,
                                                    'meeting': schedule.meeting,
                                                    'end_flg': schedule.flow.end_flg,
                                                })
                                                
                                    for time in time_list:
                                        reception_flg = True
                                        time_from = time
                                        time_to = time + datetime.timedelta(minutes=offline.time)
                                        manager_count = len(manager_list)
                                        facility_count = len(facility_list)
                                        for manager in manager_list:
                                            if reception_flg:
                                                reception_manager = ReceptionOfflineManager.objects.filter(offline=shop_offline, manager=manager, reception_date__year=target.year, reception_date__month=target.month, reception_date__day=target.day, reception_from__lte=time_from, reception_to__gte=time_to.time(), reception_flg=True).first()
                                                if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                                                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=offline).exists():
                                                        reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=offline).first()
                                                        if not reception_offline_manager_setting.flg:
                                                            reception_manager = None
                                                if reception_manager:
                                                    if len(reception_list) > 0:
                                                        people_count = offline.people
                                                        same_count = offline.facility
                                                        
                                                        reception_manager_list = list()
                                                        reception_facility_list = list()
                                                        for reception in reception_list:
                                                            if time_to > reception['from'] and reception['to'] > time_from and reception['manager'] == manager:
                                                                if manager_count <= 0 or facility_count <= 0:
                                                                    break
                                                                else:
                                                                    if reception['setting']:
                                                                        if reception['setting'].id == offline.id:
                                                                            if time_from == reception['from']:
                                                                                if reception['facility'] and reception['facility'].count <= people_count:
                                                                                    same_count = same_count - 1
                                                                                    if same_count == 0:
                                                                                        if people_count > reception['facility'].count:
                                                                                            people_count = reception['facility'].count
                                                                                people_count = people_count - 1
                                                                                if people_count <= 0:
                                                                                    if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                                        manager_count = manager_count - 1
                                                                                        reception_manager_list.append(reception['manager'])
                                                                                if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                                    facility_count = facility_count - 1
                                                                                    reception_facility_list.append(reception['facility'])
                                                                            else:
                                                                                if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                                    manager_count = manager_count - 1
                                                                                    reception_manager_list.append(reception['manager'])
                                                                                if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                                    facility_count = facility_count - 1
                                                                                    reception_facility_list.append(reception['facility'])
                                                                        else:
                                                                            if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                                manager_count = manager_count - 1
                                                                                reception_manager_list.append(reception['manager'])
                                                                            if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
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
                                                            break
                                                    else:
                                                        if manager_count > 0 and facility_count > 0:
                                                            reception_flg = False
                                                            break
                                                else:
                                                    if manager in manager_list and not manager in reception_manager_list:
                                                        manager_count = manager_count - 1
                                                        reception_manager_list.append(manager)

                                        if not reception_flg:
                                            if not first_date or time.date() == first_date.date():
                                                first_date = time
                                            elif first_date and not second_date:
                                                second_date = time
                                                break
                            
                            ReserveStartDate.objects.filter(shop=shop, offline=offline, offline_course=course).all().delete()
                            ReserveStartDate.objects.create(
                                id = str(uuid.uuid4()),
                                shop = shop,
                                offline = offline,
                                offline_course = course,
                                first_date = first_date,
                                second_date = second_date,
                            )
                    
                    start_date = current_date
                    if reserve_basic:
                        if reserve_basic.deadline == 2 and reserve_basic.any_day and reserve_basic.any_day != 0 and reserve_basic.any_time and reserve_basic.any_time != 0:
                            if reserve_basic.method == 0 or reserve_basic.method == 1:
                                start_date = start_date + datetime.timedelta(days=reserve_basic.any_day)
                            elif reserve_basic.method == 2:
                                if reserve_basic.business_mon_day or reserve_basic.business_tue_day or reserve_basic.business_wed_day or reserve_basic.business_thu_day or reserve_basic.business_fri_day or reserve_basic.business_sat_day or reserve_basic.business_sun_day:
                                    count_date = start_date
                                    count = reserve_basic.any_day
                                    while count > 0:
                                        count_date = count_date + datetime.timedelta(days=1)
                                        if count_date.weekday() == 0:
                                            if reserve_basic.business_mon_day:
                                                count = count - 1
                                        elif count_date.weekday() == 1:
                                            if reserve_basic.business_tue_day:
                                                count = count - 1
                                        elif count_date.weekday() == 2:
                                            if reserve_basic.business_wed_day:
                                                count = count - 1
                                        elif count_date.weekday() == 3:
                                            if reserve_basic.business_thu_day:
                                                count = count - 1
                                        elif count_date.weekday() == 4:
                                            if reserve_basic.business_fri_day:
                                                count = count - 1
                                        elif count_date.weekday() == 5:
                                            if reserve_basic.business_sat_day:
                                                count = count - 1
                                        elif count_date.weekday() == 6:
                                            if reserve_basic.business_sun_day:
                                                count = count - 1
                                    start_date = datetime.datetime(count_date.year, count_date.month, count_date.day, 0, 0, 0)
                                else:
                                    start_date = start_date + datetime.timedelta(days=reserve_basic.any_day)
                    end_date = None
                    if reserve_basic and reserve_basic.start != 0:
                        end_date = current_date +  datetime.timedelta(days=(reserve_basic.start*7)+1)

                    first_date = None
                    second_date = None
                    for i in range((end_date - start_date).days + 1):
                        target = start_date + datetime.timedelta(i)

                        time_list = list()
                        reception_list = list()
                        for reception_place in ReceptionOfflinePlace.objects.filter(offline=shop_offline, reception_date__year=target.year, reception_date__month=target.month, reception_date__day=target.day).all():
                            if not reception_place.reception_flg:
                                for time in pandas.date_range(start=datetime.datetime(target.year, target.month, target.day, reception_place.reception_from.hour, reception_place.reception_from.minute, 0), end=datetime.datetime(target.year, target.month, target.day, reception_place.reception_to.hour, reception_place.reception_to.minute, 0), freq=str(offline.unit)+'min'):
                                    time_list.append(time)
                                for schedule in UserFlowSchedule.objects.filter(flow__user__shop=shop, date__year=target.year, date__month=target.month, date__day=target.day, time__gte=datetime.time(reception_place.reception_from.hour, reception_place.reception_from.minute, 0), time__lte=datetime.time(reception_place.reception_to.hour, reception_place.reception_to.minute, 0), temp_flg=False).exclude(number=0).all():
                                    if schedule.join == 0 or schedule.join == 1:
                                        schedule_date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                                        reception_list.append({
                                            'from': schedule_date,
                                            'to': schedule_date + datetime.timedelta(minutes=offline.time),
                                            'setting': schedule.offline,
                                            'manager': schedule.manager,
                                            'facility': schedule.offline_facility,
                                            'meeting': schedule.meeting,
                                            'end_flg': schedule.flow.end_flg,
                                        })
                            
                            for time in time_list:
                                reception_flg = True
                                time_from = time
                                time_to = time + datetime.timedelta(minutes=offline.time)
                                manager_count = len(manager_list)
                                facility_count = len(facility_list)
                                for manager in manager_list:
                                    if reception_flg:
                                        reception_manager = ReceptionOfflineManager.objects.filter(offline=shop_offline, manager=manager, reception_date__year=target.year, reception_date__month=target.month, reception_date__day=target.day, reception_from__lte=time_from, reception_to__gte=time_to.time(), reception_flg=True).first()
                                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                                            if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=offline).exists():
                                                reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=offline).first()
                                                if not reception_offline_manager_setting.flg:
                                                    reception_manager = None
                                        if reception_manager:
                                            if len(reception_list) > 0:
                                                people_count = offline.people
                                                same_count = offline.facility
                                                
                                                reception_manager_list = list()
                                                reception_facility_list = list()
                                                for reception in reception_list:
                                                    if time_to > reception['from'] and reception['to'] > time_from and reception['manager'] == manager:
                                                        if manager_count <= 0 or facility_count <= 0:
                                                            break
                                                        else:
                                                            if reception['setting']:
                                                                if reception['setting'].id == offline.id:
                                                                    if time_from == reception['from']:
                                                                        if reception['facility'] and reception['facility'].count <= people_count:
                                                                            same_count = same_count - 1
                                                                            if same_count == 0:
                                                                                if people_count > reception['facility'].count:
                                                                                    people_count = reception['facility'].count
                                                                        people_count = people_count - 1
                                                                        if people_count <= 0:
                                                                            if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                                manager_count = manager_count - 1
                                                                                reception_manager_list.append(reception['manager'])
                                                                        if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                            facility_count = facility_count - 1
                                                                            reception_facility_list.append(reception['facility'])
                                                                    else:
                                                                        if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                            manager_count = manager_count - 1
                                                                            reception_manager_list.append(reception['manager'])
                                                                        if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                            facility_count = facility_count - 1
                                                                            reception_facility_list.append(reception['facility'])
                                                                else:
                                                                    if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                        manager_count = manager_count - 1
                                                                        reception_manager_list.append(reception['manager'])
                                                                    if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                        facility_count = facility_count - 1
                                                                        reception_facility_list.append(reception['facility'])
                                                    if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                        manager_count = manager_count - 1
                                                        reception_manager_list.append(reception['manager'])
                                                    if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                        facility_count = facility_count - 1
                                                        reception_facility_list.append(reception['facility'])

                                                if manager_count > 0 and facility_count > 0:
                                                    reception_flg = False
                                                    break
                                            else:
                                                if manager_count > 0 and facility_count > 0:
                                                    reception_flg = False
                                                    break
                                        else:
                                            if manager in manager_list and not manager in reception_manager_list:
                                                manager_count = manager_count - 1
                                                reception_manager_list.append(manager)
                                            
                                if not reception_flg:
                                    if not first_date or time.date() == first_date.date():
                                        first_date = time
                                    elif first_date and not second_date:
                                        second_date = time
                    
                    ReserveStartDate.objects.filter(shop=shop, offline=offline, offline_course=None).all().delete()
                    ReserveStartDate.objects.create(
                        id = str(uuid.uuid4()),
                        shop = shop,
                        offline = offline,
                        offline_course = None,
                        first_date = first_date,
                        second_date = second_date,
                    )

            for shop_online in ShopOnline.objects.filter(shop=shop).order_by('created_at').all():
                for online in ReserveOnlineSetting.objects.filter(online=shop_online).order_by('number').all():
                    manager_list = list()
                    for reserve_manager in ReserveOnlineManagerMenu.objects.filter(online=online).all():
                        manager_list.append(reserve_manager.manager)
                    facility_list = list()
                    for reserve_facility in ReserveOnlineFacilityMenu.objects.filter(online=online).order_by('facility__order').all():
                        facility_list.append(reserve_facility.facility)

                    start_date = current_date
                    if online.course_flg:
                        for course in ReserveOnlineCourse.objects.filter(shop=shop).all():
                            if course.deadline == 2 and course.any_day and course.any_day != 0 and course.any_time and course.any_time != 0:
                                if course.method == 0 or course.method == 1:
                                    start_date = start_date + datetime.timedelta(days=course.any_day)
                                elif course.method == 2:
                                    if course.business_mon_day or course.business_tue_day or course.business_wed_day or course.business_thu_day or course.business_fri_day or course.business_sat_day or course.business_sun_day:
                                        count_date = start_date
                                        count = course.any_day
                                        while count > 0:
                                            count_date = count_date + datetime.timedelta(days=1)
                                            if count_date.weekday() == 0:
                                                if course.business_mon_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 1:
                                                if course.business_tue_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 2:
                                                if course.business_wed_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 3:
                                                if course.business_thu_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 4:
                                                if course.business_fri_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 5:
                                                if course.business_sat_day:
                                                    count = count - 1
                                            elif count_date.weekday() == 6:
                                                if course.business_sun_day:
                                                    count = count - 1
                                        start_date = datetime.datetime(count_date.year, count_date.month, count_date.day, 0, 0, 0)
                                    else:
                                        start_date = start_date + datetime.timedelta(days=course.any_day)
                            end_date = None
                            if course and course.start != 0:
                                end_date = current_date +  datetime.timedelta(days=(course.start*7)+1)

                            first_date = None
                            second_date = None
                            for i in range((end_date - start_date).days + 1):
                                target = start_date + datetime.timedelta(i)

                                time_list = list()
                                reception_list = list()
                                for reception_place in ReceptionOnlinePlace.objects.filter(online=shop_online, reception_date__year=target.year, reception_date__month=target.month, reception_date__day=target.day).all():
                                    if not reception_place.reception_flg:
                                        for time in pandas.date_range(start=datetime.datetime(target.year, target.month, target.day, reception_place.reception_from.hour, reception_place.reception_from.minute, 0), end=datetime.datetime(target.year, target.month, target.day, reception_place.reception_to.hour, reception_place.reception_to.minute, 0), freq=str(online.unit)+'min'):
                                            time_list.append(time)
                                        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=shop, date__year=target.year, date__month=target.month, date__day=target.day, time__gte=datetime.time(reception_place.reception_from.hour, reception_place.reception_from.minute, 0), time__lte=datetime.time(reception_place.reception_to.hour, reception_place.reception_to.minute, 0), temp_flg=False).exclude(number=0).all():
                                            if schedule.join == 0 or schedule.join == 1:
                                                schedule_date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                                                reception_list.append({
                                                    'from': schedule_date,
                                                    'to': schedule_date + datetime.timedelta(minutes=online.time),
                                                    'setting': schedule.online,
                                                    'manager': schedule.manager,
                                                    'facility': schedule.online_facility,
                                                    'meeting': schedule.meeting,
                                                    'end_flg': schedule.flow.end_flg,
                                                })
                                                
                                    for time in time_list:
                                        reception_flg = True
                                        time_from = time
                                        time_to = time + datetime.timedelta(minutes=online.time)
                                        manager_count = len(manager_list)
                                        facility_count = len(facility_list)
                                        for manager in manager_list:
                                            if reception_flg:
                                                reception_manager = ReceptionOnlineManager.objects.filter(online=shop_online, manager=manager, reception_date__year=target.year, reception_date__month=target.month, reception_date__day=target.day, reception_from__lte=time_from, reception_to__gte=time_to.time(), reception_flg=True).first()
                                                if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                                                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=online).exists():
                                                        reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=online).first()
                                                        if not reception_online_manager_setting.flg:
                                                            reception_manager = None
                                                if reception_manager:
                                                    if len(reception_list) > 0:
                                                        people_count = online.people
                                                        same_count = online.facility
                                                        
                                                        reception_manager_list = list()
                                                        reception_facility_list = list()
                                                        for reception in reception_list:
                                                            if time_to > reception['from'] and reception['to'] > time_from and reception['manager'] == manager:
                                                                if manager_count <= 0 or facility_count <= 0:
                                                                    break
                                                                else:
                                                                    if reception['setting']:
                                                                        if reception['setting'].id == online.id:
                                                                            if time_from == reception['from']:
                                                                                if reception['facility'] and reception['facility'].count <= people_count:
                                                                                    same_count = same_count - 1
                                                                                    if same_count == 0:
                                                                                        if people_count > reception['facility'].count:
                                                                                            people_count = reception['facility'].count
                                                                                people_count = people_count - 1
                                                                                if people_count <= 0:
                                                                                    if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                                        manager_count = manager_count - 1
                                                                                        reception_manager_list.append(reception['manager'])
                                                                                if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                                    facility_count = facility_count - 1
                                                                                    reception_facility_list.append(reception['facility'])
                                                                            else:
                                                                                if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                                    manager_count = manager_count - 1
                                                                                    reception_manager_list.append(reception['manager'])
                                                                                if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                                    facility_count = facility_count - 1
                                                                                    reception_facility_list.append(reception['facility'])
                                                                        else:
                                                                            if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                                manager_count = manager_count - 1
                                                                                reception_manager_list.append(reception['manager'])
                                                                            if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                                facility_count = facility_count - 1
                                                                                reception_facility_list.append(reception['facility'])
                                                            if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                manager_count = manager_count - 1
                                                                reception_manager_list.append(reception['manager'])
                                                            if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                facility_count = facility_count - 1
                                                                reception_facility_list.append(reception['facility'])

                                                        if manager_count > 0 and facility_count > 0:
                                                            reception_flg = False
                                                            break
                                                    else:
                                                        if manager_count > 0 and facility_count > 0:
                                                            reception_flg = False
                                                            break
                                                else:
                                                    if manager in manager_list and not manager in reception_manager_list:
                                                        manager_count = manager_count - 1
                                                        reception_manager_list.append(manager)
                                        
                                        if not reception_flg:
                                            if not first_date or time.date() == first_date.date():
                                                first_date = time
                                            elif first_date and not second_date:
                                                second_date = time
                                                break
                            
                            ReserveStartDate.objects.filter(shop=shop, online=online, online_course=course).all().delete()
                            ReserveStartDate.objects.create(
                                id = str(uuid.uuid4()),
                                shop = shop,
                                online = online,
                                online_course = course,
                                first_date = first_date,
                                second_date = second_date,
                            )
                    
                    start_date = current_date
                    if reserve_basic:
                        if reserve_basic.deadline == 2 and reserve_basic.any_day and reserve_basic.any_day != 0 and reserve_basic.any_time and reserve_basic.any_time != 0:
                            if reserve_basic.method == 0 or reserve_basic.method == 1:
                                start_date = start_date + datetime.timedelta(days=reserve_basic.any_day)
                            elif reserve_basic.method == 2:
                                if reserve_basic.business_mon_day or reserve_basic.business_tue_day or reserve_basic.business_wed_day or reserve_basic.business_thu_day or reserve_basic.business_fri_day or reserve_basic.business_sat_day or reserve_basic.business_sun_day:
                                    count_date = start_date
                                    count = reserve_basic.any_day
                                    while count > 0:
                                        count_date = count_date + datetime.timedelta(days=1)
                                        if count_date.weekday() == 0:
                                            if reserve_basic.business_mon_day:
                                                count = count - 1
                                        elif count_date.weekday() == 1:
                                            if reserve_basic.business_tue_day:
                                                count = count - 1
                                        elif count_date.weekday() == 2:
                                            if reserve_basic.business_wed_day:
                                                count = count - 1
                                        elif count_date.weekday() == 3:
                                            if reserve_basic.business_thu_day:
                                                count = count - 1
                                        elif count_date.weekday() == 4:
                                            if reserve_basic.business_fri_day:
                                                count = count - 1
                                        elif count_date.weekday() == 5:
                                            if reserve_basic.business_sat_day:
                                                count = count - 1
                                        elif count_date.weekday() == 6:
                                            if reserve_basic.business_sun_day:
                                                count = count - 1
                                    start_date = datetime.datetime(count_date.year, count_date.month, count_date.day, 0, 0, 0)
                                else:
                                    start_date = start_date + datetime.timedelta(days=reserve_basic.any_day)
                    end_date = None
                    if reserve_basic and reserve_basic.start != 0:
                        end_date = current_date +  datetime.timedelta(days=(reserve_basic.start*7)+1)

                    first_date = None
                    second_date = None
                    for i in range((end_date - start_date).days + 1):
                        target = start_date + datetime.timedelta(i)

                        time_list = list()
                        reception_list = list()
                        for reception_place in ReceptionOnlinePlace.objects.filter(online=shop_online, reception_date__year=target.year, reception_date__month=target.month, reception_date__day=target.day).all():
                            if not reception_place.reception_flg:
                                for time in pandas.date_range(start=datetime.datetime(target.year, target.month, target.day, reception_place.reception_from.hour, reception_place.reception_from.minute, 0), end=datetime.datetime(target.year, target.month, target.day, reception_place.reception_to.hour, reception_place.reception_to.minute, 0), freq=str(online.unit)+'min'):
                                    time_list.append(time)
                                for schedule in UserFlowSchedule.objects.filter(flow__user__shop=shop, date__year=target.year, date__month=target.month, date__day=target.day, time__gte=datetime.time(reception_place.reception_from.hour, reception_place.reception_from.minute, 0), time__lte=datetime.time(reception_place.reception_to.hour, reception_place.reception_to.minute, 0), temp_flg=False).exclude(number=0).all():
                                    if schedule.join == 0 or schedule.join == 1:
                                        schedule_date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                                        reception_list.append({
                                            'from': schedule_date,
                                            'to': schedule_date + datetime.timedelta(minutes=online.time),
                                            'setting': schedule.online,
                                            'manager': schedule.manager,
                                            'facility': schedule.online_facility,
                                            'meeting': schedule.meeting,
                                            'end_flg': schedule.flow.end_flg,
                                        })
                            
                            for time in time_list:
                                reception_flg = True
                                time_from = time
                                time_to = time + datetime.timedelta(minutes=online.time)
                                manager_count = len(manager_list)
                                facility_count = len(facility_list)
                                for manager in manager_list:
                                    if reception_flg:
                                        reception_manager = ReceptionOnlineManager.objects.filter(online=shop_online, manager=manager, reception_date__year=target.year, reception_date__month=target.month, reception_date__day=target.day, reception_from__lte=time_from, reception_to__gte=time_to.time(), reception_flg=True).first()
                                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                                            if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=online).exists():
                                                reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=online).first()
                                                if not reception_online_manager_setting.flg:
                                                    reception_manager = None
                                        if reception_manager:
                                            manager_count = len(manager_list)
                                            facility_count = len(facility_list)

                                            if len(reception_list) > 0:
                                                people_count = online.people
                                                same_count = online.facility
                                                
                                                reception_manager_list = list()
                                                reception_facility_list = list()
                                                for reception in reception_list:
                                                    if time_to > reception['from'] and reception['to'] > time_from and reception['manager'] == manager:
                                                        if manager_count <= 0 or facility_count <= 0:
                                                            break
                                                        else:
                                                            if reception['setting']:
                                                                if reception['setting'].id == online.id:
                                                                    if time_from == reception['from']:
                                                                        if reception['facility'] and reception['facility'].count <= people_count:
                                                                            same_count = same_count - 1
                                                                            if same_count == 0:
                                                                                if people_count > reception['facility'].count:
                                                                                    people_count = reception['facility'].count
                                                                        people_count = people_count - 1
                                                                        if people_count <= 0:
                                                                            if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                                manager_count = manager_count - 1
                                                                                reception_manager_list.append(reception['manager'])
                                                                        if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                            facility_count = facility_count - 1
                                                                            reception_facility_list.append(reception['facility'])
                                                                    else:
                                                                        if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                            manager_count = manager_count - 1
                                                                            reception_manager_list.append(reception['manager'])
                                                                        if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                            facility_count = facility_count - 1
                                                                            reception_facility_list.append(reception['facility'])
                                                                else:
                                                                    if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                                        manager_count = manager_count - 1
                                                                        reception_manager_list.append(reception['manager'])
                                                                    if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                                        facility_count = facility_count - 1
                                                                        reception_facility_list.append(reception['facility'])
                                                    if reception['manager'] in manager_list and not reception['manager'] in reception_manager_list:
                                                        manager_count = manager_count - 1
                                                        reception_manager_list.append(reception['manager'])
                                                    if reception['facility'] in facility_list and not reception['facility'] in reception_facility_list:
                                                        facility_count = facility_count - 1
                                                        reception_facility_list.append(reception['facility'])

                                                if manager_count > 0 and facility_count > 0:
                                                    reception_flg = False
                                                    break
                                            else:
                                                if manager_count > 0 and facility_count > 0:
                                                    reception_flg = False
                                                    break
                                        else:
                                            if manager in manager_list and not manager in reception_manager_list:
                                                manager_count = manager_count - 1
                                                reception_manager_list.append(manager)
                                            
                                if not reception_flg:
                                    if not first_date or time.date() == first_date.date():
                                        first_date = time
                                    elif first_date and not second_date:
                                        second_date = time
                    
                    ReserveStartDate.objects.filter(shop=shop, online=online, online_course=None).all().delete()
                    ReserveStartDate.objects.create(
                        id = str(uuid.uuid4()),
                        shop = shop,
                        online = online,
                        online_course = None,
                        first_date = first_date,
                        second_date = second_date,
                    )

        self.stdout.write(self.style.SUCCESS('reserve start date successfully!!'))