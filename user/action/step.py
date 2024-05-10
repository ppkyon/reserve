from django.http import JsonResponse

from linebot import LineBotApi

from flow.models import ShopFlowItem, ShopFlowTemplate, ShopFlowActionReminder, ShopFlowActionMessage, UserFlow, UserFlowSchedule, UserFlowActionReminder
from reserve.models import (
    ReserveOfflineSetting, ReserveOnlineSetting, ReserveOfflineFacility, ReserveOnlineFacility, ReserveOfflineCourse, ReserveOnlineCourse,
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
            for user_flow_schedule in UserFlowSchedule.objects.filter(flow=user_flow, join=0).order_by('number').all():
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
                    user_flow_schedule = UserFlowSchedule.objects.create(
                        id = str(uuid.uuid4()),
                        display_id = create_code(12, UserFlowSchedule),
                        flow = user_flow,
                        number = UserFlowSchedule.objects.filter(flow=user_flow).count() + 1,
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
        user['flow'][user_flow_index]['schedule'] = list(UserFlowSchedule.objects.filter(flow__id=user_flow_item['id']).order_by('number').values(*get_model_field(UserFlowSchedule)).all())
        for user_flow_schedule_index, user_flow_schedule_item in enumerate(user['flow'][user_flow_index]['schedule']):
            if user_flow_schedule_item['offline']:
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['offline'] = ReserveOfflineSetting.objects.filter(id=user_flow_schedule_item['offline']).values(*get_model_field(ReserveOfflineSetting)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['offline_course'] = ReserveOfflineCourse.objects.filter(id=user_flow_schedule_item['offline']).values(*get_model_field(ReserveOfflineCourse)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['offline_facility'] = ReserveOfflineFacility.objects.filter(id=user_flow_schedule_item['offline_facility']).values(*get_model_field(ReserveOfflineFacility)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager_list'] = list(ReserveOfflineManagerMenu.objects.filter(shop__id=user['shop'], offline__id=user_flow_schedule_item['offline']).values(*get_model_field(ReserveOfflineManagerMenu)).all())
                for manager_index, manager_item in enumerate(user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager_list']):
                    user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['manager_list'][manager_index] = AuthUser.objects.filter(id=manager_item['id']).values(*get_model_field(AuthUser)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['facility_list'] = list(ReserveOfflineFacilityMenu.objects.filter(shop__id=user['shop'], offline__id=user_flow_schedule_item['offline']).values(*get_model_field(ReserveOfflineFacilityMenu)).all())
                for facility_index, facility_item in enumerate(user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['facility_list']):
                    user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['facility_list'][facility_index] = ReserveOfflineFacility.objects.filter(id=facility_item['id']).values(*get_model_field(ReserveOfflineFacility)).first()
            elif user_flow_schedule_item['online']:
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['online'] = ReserveOnlineSetting.objects.filter(id=user_flow_schedule_item['online']).values(*get_model_field(ReserveOnlineSetting)).first()
                user['flow'][user_flow_index]['schedule'][user_flow_schedule_index]['online_course'] = ReserveOnlineCourse.objects.filter(id=user_flow_schedule_item['online']).values(*get_model_field(ReserveOnlineCourse)).first()
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