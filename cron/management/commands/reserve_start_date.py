from django.core.management.base import BaseCommand

from common import create_code

from flow.models import UserFlowSchedule
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager
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

            unit_time = '60min'
            reserve_basic = ReserveBasic.objects.filter(shop=shop).first()
            if reserve_basic:
                if reserve_basic.unit == 60:
                    unit_time = '60min'
                elif reserve_basic.unit == 30:
                    unit_time = '30min'
                elif reserve_basic.unit == 15:
                    unit_time = '15min'
                
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
                                        for time in pandas.date_range(start=datetime.datetime(target.year, target.month, target.day, reception_place.reception_from.hour, reception_place.reception_from.minute, 0), end=datetime.datetime(target.year, target.month, target.day, reception_place.reception_to.hour, reception_place.reception_to.minute, 0), freq=unit_time):
                                            time_list.append(time)
                                        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=shop, date__year=target.year, date__month=target.month, date__day=target.day, time__gte=datetime.time(reception_place.reception_from.hour, reception_place.reception_from.minute, 0), time__lte=datetime.time(reception_place.reception_to.hour, reception_place.reception_to.minute, 0)).all():
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
                                        for manager in manager_list:
                                            time_from = time
                                            time_to = time + datetime.timedelta(minutes=offline.time)
                                            reception_place = ReceptionOfflinePlace.objects.filter(offline=shop_offline, reception_date__year=time.year, reception_date__month=time.month, reception_date__day=time.day, reception_from__lte=time_from.time(), reception_to__gte=time_to.time(), reception_flg=False).first()
                                            reception_manager = ReceptionOfflineManager.objects.filter(offline=shop_offline, manager=manager, reception_date__year=time.year, reception_date__month=time.month, reception_date__day=time.day, reception_from__lte=time_from.time(), reception_to__gte=time_to.time(), reception_flg=True).first()
                                            if reception_place and reception_manager and reception_flg:
                                                manager_count = len(manager_list)
                                                facility_count = len(facility_list)

                                                if len(reception_list) > 0:
                                                    people_number = 0
                                                    people_count = offline.people
                                                    
                                                    reception_manager_list = list()
                                                    reception_facility_list = list()
                                                    count_flg = True
                                                    for reception in reception_list:
                                                        if time_to > reception['from'] and reception['to'] > time_from:
                                                            if manager_count <= 0 or facility_count <= 0:
                                                                break
                                                            else:
                                                                if reception['setting']:
                                                                    if reception['setting'].id == offline.id:
                                                                        if time_from == reception['from']:
                                                                            if count_flg:
                                                                                if reception['facility'] and reception['facility'].count < people_count:
                                                                                    people_count = reception['facility'].count
                                                                                count_flg = False
                                                                            people_count = people_count - 1
                                                                            if people_count <= 0:
                                                                                manager_count = manager_count - 1
                                                                                facility_count = facility_count - 1

                                                                                people_number = people_number + 1
                                                                                people_count = offline.people
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
                                                    if manager_count > 0 and facility_count > 0:
                                                        reception_flg = False
                                                        break
                                        
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
                                for time in pandas.date_range(start=datetime.datetime(target.year, target.month, target.day, reception_place.reception_from.hour, reception_place.reception_from.minute, 0), end=datetime.datetime(target.year, target.month, target.day, reception_place.reception_to.hour, reception_place.reception_to.minute, 0), freq=unit_time):
                                    time_list.append(time)
                                for schedule in UserFlowSchedule.objects.filter(flow__user__shop=shop, date__year=target.year, date__month=target.month, date__day=target.day, time__gte=datetime.time(reception_place.reception_from.hour, reception_place.reception_from.minute, 0), time__lte=datetime.time(reception_place.reception_to.hour, reception_place.reception_to.minute, 0)).all():
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
                                for manager in manager_list:
                                    time_from = time
                                    time_to = time + datetime.timedelta(minutes=offline.time)
                                    reception_place = ReceptionOfflinePlace.objects.filter(offline=shop_offline, reception_date__year=time.year, reception_date__month=time.month, reception_date__day=time.day, reception_from__lte=time_from.time(), reception_to__gte=time_to.time(), reception_flg=False).first()
                                    reception_manager = ReceptionOfflineManager.objects.filter(offline=shop_offline, manager=manager, reception_date__year=time.year, reception_date__month=time.month, reception_date__day=time.day, reception_from__lte=time_from.time(), reception_to__gte=time_to.time(), reception_flg=True).first()
                                    if reception_place and reception_manager and reception_flg:
                                        manager_count = len(manager_list)
                                        facility_count = len(facility_list)

                                        if len(reception_list) > 0:
                                            people_number = 0
                                            people_count = offline.people
                                            
                                            reception_manager_list = list()
                                            reception_facility_list = list()
                                            count_flg = True
                                            for reception in reception_list:
                                                if time_to > reception['from'] and reception['to'] > time_from:
                                                    if manager_count <= 0 or facility_count <= 0:
                                                        break
                                                    else:
                                                        if reception['setting']:
                                                            if reception['setting'].id == offline.id:
                                                                if time_from == reception['from']:
                                                                    if count_flg:
                                                                        if reception['facility'] and reception['facility'].count < people_count:
                                                                            people_count = reception['facility'].count
                                                                        count_flg = False
                                                                    people_count = people_count - 1
                                                                    if people_count <= 0:
                                                                        manager_count = manager_count - 1
                                                                        facility_count = facility_count - 1

                                                                        people_number = people_number + 1
                                                                        people_count = offline.people
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
                                            if manager_count > 0 and facility_count > 0:
                                                reception_flg = False
                                                break
                                            
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

        self.stdout.write(self.style.SUCCESS('reserve start date successfully!!'))