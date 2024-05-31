from django.db.models import Q
from django.http import JsonResponse

from flow.models import UserFlow, UserFlowSchedule
from reception.models import ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflineSetting, ReserveOnlineSetting,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu
)
from sign.models import AuthLogin

from common import create_code

import datetime
import uuid

def temp(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
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
            for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(temp_manager=auth_login.user, number=0, temp_flg=True).all():
                if schedule.join != 2:
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
                                    if manager_item.count <= 0:
                                        reception_manager_list.append(schedule_item.manager.id)
                            for facility_item in facility_list:
                                if facility_item == schedule_item.offline_facility:
                                    facility_item.count = facility_item.count - 1
                                    if facility_item.count <= 0:
                                        reception_facility_list.append(facility_item.id)
                        else:
                            reception_manager_list.append(schedule_item.manager.id)
                            reception_facility_list.append(schedule_item.offline_facility.id)
                    else:
                        reception_manager_list.append(schedule_item.manager.id)
                        reception_facility_list.append(schedule_item.offline_facility.id)
            
            manager = None
            for manager_item in ReserveOfflineManagerMenu.objects.filter(shop=auth_login.shop, offline=setting).order_by('manager__created_at').all():
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
            for facility_item in ReserveOfflineFacilityMenu.objects.filter(shop=auth_login.shop, offline=setting).order_by('facility__order').all():
                if not facility_item.facility.id in reception_facility_list:
                    facility = facility_item.facility
                    break
                
            course = None
            if request.POST.get('course_id'):
                course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()

            UserFlowSchedule.objects.filter(temp_manager=auth_login.user, number=0, temp_flg=True).all().delete()
            UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                flow = None,
                number = 0,
                date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
                time = request.POST.get('hour') + ':' + request.POST.get('minute'),
                join = 0,
                offline = setting,
                offline_course = course,
                offline_facility = facility,
                manager = manager,
                temp_manager = auth_login.user,
                temp_flg = True,
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
            for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(temp_manager=auth_login.user, number=0, temp_flg=True).all():
                if schedule.join != 2:
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
                                    if manager_item.count <= 0:
                                        reception_manager_list.append(schedule_item.manager.id)
                            for facility_item in facility_list:
                                if facility_item == schedule_item.online_facility:
                                    facility_item.count = facility_item.count - 1
                                    if facility_item.count <= 0:
                                        reception_facility_list.append(facility_item.id)
                        else:
                            reception_manager_list.append(schedule_item.manager.id)
                            reception_facility_list.append(schedule_item.online_facility.id)
                    else:
                        reception_manager_list.append(schedule_item.manager.id)
                        reception_facility_list.append(schedule_item.online_facility.id)

            manager = None
            for manager_item in ReserveOnlineManagerMenu.objects.filter(shop=auth_login.shop, online=setting).order_by('manager__created_at').all():
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
            for facility_item in ReserveOnlineFacilityMenu.objects.filter(shop=auth_login.shop, online=setting).all():
                if not facility_item.facility in reception_facility_list:
                    facility = facility_item.facility
                    break
            
            course = None
            if request.POST.get('course_id'):
                course = ReserveOnlineCourse.objects.filter(display_id=request.POST.get('course_id')).first()
            
            UserFlowSchedule.objects.filter(temp_manager=auth_login.user, number=0, temp_flg=True).all().delete()
            UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                flow = None,
                number = 0,
                date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
                time = request.POST.get('hour') + ':' + request.POST.get('minute'),
                join = 0,
                online = setting,
                online_course = course,
                online_facility = facility,
                manager = manager,
                temp_manager = auth_login.user,
                temp_flg = True,
            )
    return JsonResponse( {}, safe=False )