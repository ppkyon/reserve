from django.db.models import Q
from django.http import JsonResponse

from linebot import LineBotApi

from flow.models import ShopFlowItem, ShopFlowTemplate, ShopFlowActionReminder, ShopFlowActionMessage, UserFlow, UserFlowSchedule, UserFlowActionReminder
from reception.models import ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveOfflineSetting, ReserveOnlineSetting, ReserveOfflineFacility, ReserveOnlineFacility, ReserveOfflineCourse, ReserveOnlineCourse, ReserveUserStartDate,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu
)
from sign.models import AuthLogin, ShopLine, AuthUser, ManagerProfile
from template.models import ShopTemplateTextItem, ShopTemplateVideo, ShopTemplateCardType
from user.models import LineUser, UserAlert, UserProfile

from common import create_code, send_textarea_replace, get_model_field
from flow.action.go import go
from line.action.common import line_info
from line.action.message import push_text_message, push_image_message, push_video_message, push_card_type_message

import datetime
import re
import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('user_id')).first()

    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=auth_login.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)

    remove = re.compile(r"<[^>]*?>")
    for user_flow in UserFlow.objects.filter(user=user).order_by('number').all():
        if not user_flow.end_flg:
            for user_flow_schedule in UserFlowSchedule.objects.filter(flow=user_flow, join=0, temp_flg=False).exclude(number=0).order_by('number').all():
                change_flg = False

                user_flow_schedule_date = None
                user_flow_schedule_time = None
                user_flow_schedule_manager = None
                user_flow_schedule_offline_facility = None
                user_flow_schedule_online_facility = None
                user_flow_schedule_online_join = 0
                if request.POST.get('date_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    date = request.POST.get('date_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)).split(' ')
                    if str(user_flow_schedule.date) != date[0].strip().replace('/','-') + ' 00:00:00' or str(user_flow_schedule.time) != date[1].strip() + ':00':
                        if not check_timeout(user):
                            return JsonResponse( {'temp': True}, safe=False )
                        if not check_reserve(auth_login, user_flow, user_flow_schedule, date):
                            return JsonResponse( {'error': True}, safe=False )
                        change_flg = True
                    user_flow_schedule_date = datetime.datetime.strptime(date[0].strip().replace('/','-') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
                    user_flow_schedule_time = datetime.datetime.strptime(date[1].strip() + ':00', '%H:%M:%S') 
                join = 0
                if request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    join = int(request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)))
                if request.POST.get('manager_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    user_flow_schedule_manager = AuthUser.objects.filter(display_id=request.POST.get('manager_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number))).first()
                if request.POST.get('facility_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    if user_flow_schedule.offline:
                        user_flow_schedule_offline_facility = ReserveOfflineFacility.objects.filter(display_id=request.POST.get('facility_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number))).first()
                    if user_flow_schedule.online:
                        user_flow_schedule_online_facility = ReserveOnlineFacility.objects.filter(display_id=request.POST.get('facility_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number))).first()
                if user_flow_schedule.join == 0:
                    user_flow_schedule_online_join = join

                user_flow.updated_at = datetime.datetime.now()
                user_flow.save()
                if change_flg and user_flow_schedule.date:
                    user_flow_schedule.join = 2
                    user_flow_schedule.save()

                    UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).all().delete()
                    user_flow_schedule = UserFlowSchedule.objects.create(
                        id = str(uuid.uuid4()),
                        display_id = create_code(12, UserFlowSchedule),
                        flow = user_flow,
                        number = UserFlowSchedule.objects.filter(flow=user_flow, temp_flg=False).exclude(number=0).count() + 1,
                        date = user_flow_schedule_date,
                        time = user_flow_schedule_time,
                        join = user_flow_schedule_online_join,
                        offline = user_flow_schedule.offline,
                        online = user_flow_schedule.online,
                        offline_course = user_flow_schedule.offline_course,
                        online_course = user_flow_schedule.online_course,
                        offline_facility = user_flow_schedule_offline_facility,
                        online_facility = user_flow_schedule_online_facility,
                        manager = user_flow_schedule_manager,
                        question = user_flow_schedule.question,
                        check_flg = False,
                        updated_at = datetime.datetime.now(),
                    )
                else:
                    user_flow_schedule.date = user_flow_schedule_date
                    user_flow_schedule.time = user_flow_schedule_time
                    user_flow_schedule.manager = user_flow_schedule_manager
                    user_flow_schedule.offline_facility = user_flow_schedule_offline_facility
                    user_flow_schedule.online_facility = user_flow_schedule_online_facility
                    user_flow_schedule.join = user_flow_schedule_online_join
                    user_flow_schedule.updated_at = datetime.datetime.now()
                    user_flow_schedule.save()

                if user_flow_schedule.offline:
                    for reserve_offline_setting in ReserveOfflineSetting.objects.filter(offline__shop=auth_login.shop).order_by('number').all():
                        if reserve_offline_setting.advance and int(reserve_offline_setting.advance) == user_flow_schedule.offline.display_id:
                            ReserveUserStartDate.objects.filter(user=user, offline=reserve_offline_setting).all().delete()
                            ReserveUserStartDate.objects.create(
                                id = str(uuid.uuid4()),
                                user = user,
                                offline = reserve_offline_setting,
                                date = user_flow_schedule_date,
                            )
                elif user_flow_schedule.online:
                    for reserve_online_setting in ReserveOnlineSetting.objects.filter(online__shop=auth_login.shop).order_by('number').all():
                        if reserve_online_setting.advance and int(reserve_online_setting.advance) == user_flow_schedule.online.display_id:
                            ReserveUserStartDate.objects.filter(user=user, online=reserve_online_setting).all().delete()
                            ReserveUserStartDate.objects.create(
                                id = str(uuid.uuid4()),
                                user = user,
                                online = reserve_online_setting,
                                date = user_flow_schedule_date,
                            )

                if join == 1:
                    flow_flg = False
                    for flow_item in ShopFlowItem.objects.filter(flow_tab=user_flow.flow_tab).all():
                        if flow_flg:
                            if go(user, user_flow.flow, user_flow.flow_tab, flow_item):
                                user_flow.end_flg = True
                                user_flow.save()
                                break
                        if flow_item.type == 8:
                            action_message = ShopFlowActionMessage.objects.filter(flow=flow_item).first()
                            if action_message.type == 0:
                                if action_message.template_text:
                                    for template_text_item in ShopTemplateTextItem.objects.filter(template=action_message.template_text).all():
                                        if template_text_item.message_type == 0 or template_text_item.message_type == 1:
                                            if template_text_item.text:
                                                text = send_textarea_replace(template_text_item.text, line_info(shop_line), user)
                                                if text:
                                                    push_text_message(user, remove.sub( '', text ), None)
                                        elif template_text_item.message_type == 2:
                                            push_image_message(user, template_text_item.image, None)
                                        elif template_text_item.message_type == 3:
                                            push_video_message(user, template_text_item.video, None)
                                elif action_message.template_video:
                                    push_video_message(user, action_message.template_video.video, None)
                                elif action_message.template_richmessage:
                                    print()
                                elif action_message.template_richvideo:
                                    print()
                                elif action_message.template_cardtype:
                                    push_card_type_message(user, action_message.template_cardtype, None)
                            flow_flg = True
                    UserAlert.objects.filter(user=user, number=user_flow.number).all().delete()
                elif join == 2:
                    remove = re.compile(r"<[^>]*?>")
                    if request.POST.get('message_type') == '1':
                        push_text_message(user, remove.sub( '', request.POST.get('message') ), None)
                    elif request.POST.get('message_type') == '2':
                        if request.POST.get('message_template_type') == '0':
                            for template_text_item in ShopTemplateTextItem.objects.filter(template__display_id=request.POST.get('message_template')).all():
                                if template_text_item.message_type == 0 or template_text_item.message_type == 1:
                                    if template_text_item.text:
                                        text = send_textarea_replace(template_text_item.text, line_info(shop_line), user)
                                        if text:
                                            push_text_message(user, remove.sub( '', text ), None)
                                elif template_text_item.message_type == 2:
                                    push_image_message(user, template_text_item.image, None)
                                elif template_text_item.message_type == 3:
                                    push_video_message(user, template_text_item.video, None)
                        elif request.POST.get('message_template_type') == '1':
                            template_video = ShopTemplateVideo.objects.filter(display_id=request.POST.get('message_template')).first()
                            push_video_message(user, template_video.video, None)
                        elif request.POST.get('message_template_type') == '2':
                            print()
                        elif request.POST.get('message_template_type') == '3':
                            print()
                        elif request.POST.get('message_template_type') == '4':
                            template_cardtype = ShopTemplateCardType.objects.filter(display_id=request.POST.get('message_template')).first()
                            push_card_type_message(user, template_cardtype, None)
                    UserAlert.objects.filter(user=user, number=user_flow.number).all().delete()

                if change_flg:
                    target_flow_item = None
                    action_flow_item = None
                    flow_flg = False
                    action_flg = False
                    for flow_item in ShopFlowItem.objects.filter(flow_tab=user_flow.flow_tab).order_by('y', 'x').all():
                        if flow_flg:
                            if action_flg:
                                action_flow_item = flow_item
                                break
                            if flow_item.type == 6:
                                flow_template = ShopFlowTemplate.objects.filter(flow=flow_item).first()
                                push_card_type_message(user_flow.user, flow_template.template_cardtype, None)
                            if flow_item.type == 51:
                                target_flow_item = flow_item
                                action_flg = True
                        if flow_item.type == 54:
                            flow_flg = True
                    
                    user_flow.flow_item = target_flow_item
                    user_flow.save()

                    shop_flow_action_reminder = ShopFlowActionReminder.objects.filter(flow=action_flow_item).first()
                    action_date = datetime.datetime(user_flow_schedule.date.year, user_flow_schedule.date.month, user_flow_schedule.date.day, user_flow_schedule.time.hour, user_flow_schedule.time.minute, 0)
                    action_date = action_date - datetime.timedelta(shop_flow_action_reminder.date)
                    action_date = datetime.datetime(action_date.year, action_date.month, action_date.day, shop_flow_action_reminder.time, 0, 0)
                    if UserFlowActionReminder.objects.filter(user=user, flow=user_flow).exists():
                        user_flow_action_reminder = UserFlowActionReminder.objects.filter(user=user, flow=user_flow).first()
                        user_flow_action_reminder.action_date = action_date
                        user_flow_action_reminder.save()
                    else:
                        UserFlowActionReminder.objects.create(
                            id = str(uuid.uuid4()),
                            user = user,
                            flow = user_flow,
                            template_text = shop_flow_action_reminder.template_text,
                            template_video = shop_flow_action_reminder.template_video,
                            template_richmessage = shop_flow_action_reminder.template_richmessage,
                            template_richvideo = shop_flow_action_reminder.template_richvideo,
                            template_cardtype = shop_flow_action_reminder.template_cardtype,
                            action_date = action_date,
                        )

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )



def get(request):
    user = LineUser.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(LineUser)).first()
    user['profile'] = UserProfile.objects.filter(user__id=user['id']).values(*get_model_field(UserProfile)).first()
    user['flow'] = list(UserFlow.objects.filter(user__id=user['id']).order_by('number').values(*get_model_field(UserFlow)).all())
    for user_flow_index, user_flow_item in enumerate(user['flow']):
        user['flow'][user_flow_index]['schedule'] = list(UserFlowSchedule.objects.filter(flow__id=user_flow_item['id'], temp_flg=False).exclude(number=0).order_by('number').values(*get_model_field(UserFlowSchedule)).all())
        for user_flow_schedule_index, user_flow_schedule_item in enumerate(user['flow'][user_flow_index]['schedule']):
            if user_flow_schedule_item['offline']:
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['offline'] = ReserveOfflineSetting.objects.filter(id=user_flow_schedule_item['offline']).values(*get_model_field(ReserveOfflineSetting)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['offline_course'] = ReserveOfflineCourse.objects.filter(id=user_flow_schedule_item['offline_course']).values(*get_model_field(ReserveOfflineCourse)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['offline_facility'] = ReserveOfflineFacility.objects.filter(id=user_flow_schedule_item['offline_facility']).values(*get_model_field(ReserveOfflineFacility)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager_list'] = list(ReserveOfflineManagerMenu.objects.filter(shop__id=user['shop'], offline__id=user_flow_schedule_item['offline']).values(*get_model_field(ReserveOfflineManagerMenu)).all())
                for manager_index, manager_item in enumerate(user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager_list']):
                    user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager_list'][manager_index] = AuthUser.objects.filter(id=manager_item['id']).values(*get_model_field(AuthUser)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['facility_list'] = list(ReserveOfflineFacilityMenu.objects.filter(shop__id=user['shop'], offline__id=user_flow_schedule_item['offline']).values(*get_model_field(ReserveOfflineFacilityMenu)).all())
                for facility_index, facility_item in enumerate(user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['facility_list']):
                    user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['facility_list'][facility_index] = ReserveOfflineFacility.objects.filter(id=facility_item['id']).values(*get_model_field(ReserveOfflineFacility)).first()
            elif user_flow_schedule_item['online']:
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['online'] = ReserveOnlineSetting.objects.filter(id=user_flow_schedule_item['online']).values(*get_model_field(ReserveOnlineSetting)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['online_course'] = ReserveOnlineCourse.objects.filter(id=user_flow_schedule_item['online_course']).values(*get_model_field(ReserveOnlineCourse)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['offline_facility'] = ReserveOnlineFacility.objects.filter(id=user_flow_schedule_item['online_facility']).values(*get_model_field(ReserveOnlineFacility)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager_list'] = list(ReserveOnlineManagerMenu.objects.filter(shop__id=user['shop'], online__id=user_flow_schedule_item['online']).values(*get_model_field(ReserveOnlineManagerMenu)).all())
                for manager_index, manager_item in enumerate(user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager_list']):
                    user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager_list'][manager_index] = AuthUser.objects.filter(id=manager_item['id']).values(*get_model_field(AuthUser)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['facility_list'] = list(ReserveOnlineFacilityMenu.objects.filter(shop__id=user['shop'], online__id=user_flow_schedule_item['online']).values(*get_model_field(ReserveOnlineFacilityMenu)).all())
                for facility_index, facility_item in enumerate(user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['facility_list']):
                    user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['facility_list'][facility_index] = ReserveOnlineFacility.objects.filter(id=facility_item['id']).values(*get_model_field(ReserveOnlineFacility)).first()            
            if user_flow_schedule_item['date']:
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['date'] = user_flow_schedule_item['date'].strftime('%Y/%m/%d')
            if user_flow_schedule_item['time']:
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['time'] = user_flow_schedule_item['time'].strftime('%H:%M')
            if user_flow_schedule_item['manager']:
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager'] = AuthUser.objects.filter(id=user_flow_schedule_item['manager']).values(*get_model_field(AuthUser)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager']['profile'] = ManagerProfile.objects.filter(manager__id=user_flow_schedule_item['manager']['id']).values(*get_model_field(ManagerProfile)).first()
        user['flow'][user_flow_index]['alert'] = UserAlert.objects.filter(user__id=user['id'], number=user_flow_item['number']).values(*get_model_field(UserAlert)).first()
        if user_flow_item['updated_at']:
            user['flow'][user_flow_index]['updated_at'] = user_flow_item['updated_at'].strftime('%Y年%m月%d日 %H:%M')
        if user_flow_item['created_at']:
            user['flow'][user_flow_index]['created_at'] = user_flow_item['created_at'].strftime('%Y年%m月%d日 %H:%M')
    return JsonResponse( user, safe=False )



def check_reserve(auth_login, user_flow, user_flow_schedule, date):
    if user_flow_schedule.offline and ReserveOfflineSetting.objects.filter(display_id=user_flow_schedule.offline.display_id).exists():
        setting = ReserveOfflineSetting.objects.filter(display_id=user_flow_schedule.offline.display_id).first()
        manager_list = list()
        facility_list = list()
        user_flow_schedule_date = datetime.datetime.strptime(date[0].strip().replace('/','-') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        user_flow_schedule_time = datetime.datetime.strptime(date[1].strip() + ':00', '%H:%M:%S')
        schedule_datetime = datetime.datetime(user_flow_schedule_date.year, user_flow_schedule_date.month, user_flow_schedule_date.day, user_flow_schedule_time.hour, user_flow_schedule_time.minute, 0)
        schedule_add_datetime = schedule_datetime + datetime.timedelta(minutes=setting.time)
        if setting:
            for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=setting).all():
                reception_manager = ReceptionOfflineManager.objects.filter(offline=setting.offline, manager=manager_menu_item.manager, reception_date__year=user_flow_schedule_date.year, reception_date__month=user_flow_schedule_date.month, reception_date__day=user_flow_schedule_date.day, reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).exists():
                            reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).first()
                            if reception_offline_manager_setting.flg:
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)

        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=user_flow_schedule_date.year, date__month=user_flow_schedule_date.month, date__day=user_flow_schedule_date.day).exclude(flow__user=user_flow.user, number=0, temp_flg=True).all():
            if schedule.join != 2:
                schedule_list.append(schedule)

        date = datetime.datetime(user_flow_schedule_date.year, user_flow_schedule_date.month, user_flow_schedule_date.day, user_flow_schedule_time.hour, user_flow_schedule_time.minute, 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        manager_count = len(manager_list)
        facility_count = len(facility_list)
        reception_manager_list = list()
        reception_facility_list = list()
        count_flg = True
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule_item.offline.time)

            people_number = 0
            people_count = setting.people
            same_count = setting.facility
            if add_date > schedule_date and schedule_add_date > date:
                if manager_count <= 0 or facility_count <= 0:
                    break
                else:
                    if schedule_item.offline:
                        if schedule_item.offline == setting:
                            if schedule_date == date:
                                if count_flg:
                                    if schedule_item.offline_facility and schedule_item.offline_facility.count < people_count:
                                        same_count = same_count - 1
                                        if same_count == 0:
                                            if people_count > schedule_item.offline_facility.count:
                                                people_count = schedule_item.offline_facility.count
                                        else:
                                            people_total_count = schedule_item.offline_facility.count
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
                                    if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                        manager_count = manager_count - 1
                                        reception_manager_list.append(schedule_item.manager)
                                    if schedule_item.offline_facility in facility_list and not schedule_item.offline_facility in reception_facility_list:
                                        facility_count = facility_count - 1
                                        reception_facility_list.append(schedule_item.offline_facility)

                                    people_number = people_number + 1
                                    people_count = setting.people
                                    if facility_count > 0 and facility_list[people_number].count < people_count:
                                        people_count = facility_list[people_number].count
                            else:
                                if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                    manager_count = manager_count - 1
                                    reception_manager_list.append(schedule_item.manager)
                                if schedule_item.offline_facility in facility_list and not schedule_item.offline_facility in reception_facility_list:
                                    facility_count = facility_count - 1
                                    reception_facility_list.append(schedule_item.offline_facility)
                        else:
                            if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                manager_count = manager_count - 1
                                reception_manager_list.append(schedule_item.manager)
                            if schedule_item.offline_facility in facility_list and not schedule_item.offline_facility in reception_facility_list:
                                facility_count = facility_count - 1
                                reception_facility_list.append(schedule_item.offline_facility)

    if user_flow_schedule.online and ReserveOnlineSetting.objects.filter(display_id=user_flow_schedule.online.display_id).exists():
        setting = ReserveOnlineSetting.objects.filter(display_id=user_flow_schedule.online.display_id).first()
        manager_list = list()
        facility_list = list()
        user_flow_schedule_date = datetime.datetime.strptime(date[0].strip().replace('/','-') + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        user_flow_schedule_time = datetime.datetime.strptime(date[1].strip() + ':00', '%H:%M:%S')
        schedule_datetime = datetime.datetime(user_flow_schedule_date.year, user_flow_schedule_date.month, user_flow_schedule_date.day, user_flow_schedule_time.hour, user_flow_schedule_time.minute, 0)
        schedule_add_datetime = schedule_datetime + datetime.timedelta(minutes=setting.time)
        if setting:
            for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=setting).all():
                reception_manager = ReceptionOnlineManager.objects.filter(online=setting.online, manager=manager_menu_item.manager, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).exists():
                            reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).first()
                            if reception_online_manager_setting.flg:
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)

        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=auth_login.shop)|Q(temp_manager__shop=auth_login.shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=schedule_datetime.year, date__month=schedule_datetime.month, date__day=schedule_datetime.day).exclude(flow__user=user_flow.user, number=0, temp_flg=True).all():
            if schedule.join != 2:
                schedule_list.append(schedule)

        date = datetime.datetime(schedule_datetime.year, schedule_datetime.month, schedule_datetime.day, user_flow_schedule_time.hour, user_flow_schedule_time.minute, 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        manager_count = len(manager_list)
        facility_count = len(facility_list)
        reception_manager_list = list()
        reception_facility_list = list()
        count_flg = True
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.offline.time)

            people_number = 0
            people_count = setting.people
            same_count = setting.facility
            if add_date > schedule_date and schedule_add_date > date:
                if manager_count <= 0 or facility_count <= 0:
                    break
                else:
                    if schedule_item.online:
                        if schedule_item.online == setting:
                            if schedule_date == date:
                                if count_flg:
                                    if schedule_item.online_facility and schedule_item.online_facility.count < people_count:
                                        same_count = same_count - 1
                                        if same_count == 0:
                                            if people_count > schedule_item.online_facility.count:
                                                people_count = schedule_item.online_facility.count
                                        else:
                                            people_total_count = schedule_item.online_facility.count
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
                                    if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                        manager_count = manager_count - 1
                                        reception_manager_list.append(schedule_item.manager)
                                    if schedule_item.online_facility in facility_list and not schedule_item.online_facility in reception_facility_list:
                                        facility_count = facility_count - 1
                                        reception_facility_list.append(schedule_item.online_facility)

                                    people_number = people_number + 1
                                    people_count = setting.people
                                    if facility_count > 0 and facility_list[people_number].count < people_count:
                                        people_count = facility_list[people_number].count
                            else:
                                if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                    manager_count = manager_count - 1
                                    reception_manager_list.append(schedule_item.manager)
                                if schedule_item.online_facility in facility_list and not schedule_item.online_facility in reception_facility_list:
                                    facility_count = facility_count - 1
                                    reception_facility_list.append(schedule_item.online_facility)
                        else:
                            if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                manager_count = manager_count - 1
                                reception_manager_list.append(schedule_item.manager)
                            if schedule_item.online_facility in facility_list and not schedule_item.online_facility in reception_facility_list:
                                facility_count = facility_count - 1
                                reception_facility_list.append(schedule_item.online_facility)

    if manager_count <= 0 or facility_count <= 0:
        return False
    return True

def check_timeout(user):
    if not UserFlowSchedule.objects.filter(flow__user=user, number=0, temp_flg=True).exists():
        return False
    return True