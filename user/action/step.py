from django.http import JsonResponse

from linebot import LineBotApi

from flow.models import ShopFlowItem, ShopFlowTemplate, ShopFlowActionMessage, UserFlow, UserFlowSchedule
from reserve.models import ReserveOfflineFacility, ReserveOnlineFacility
from sign.models import AuthLogin, ShopLine, AuthUser
from template.models import ShopTemplateTextItem, ShopTemplateVideo, ShopTemplateCardType
from user.models import LineUser

from common import send_textarea_replace
from flow.action.go import go
from line.action.common import line_info
from line.action.message import push_text_message, push_image_message, push_video_message, push_card_type_message

import re

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
                if request.POST.get('date_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    date = request.POST.get('date_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)).split(' ')
                    if str(user_flow_schedule.date) != date[0].strip().replace('/','-') + ' 00:00:00' or str(user_flow_schedule.time) != date[1].strip() + ':00':
                        change_flg = True
                    user_flow_schedule.date = date[0].strip().replace('/','-')
                    user_flow_schedule.time = date[1].strip()
                join = 0
                if request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    join = int(request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)))
                if request.POST.get('manager_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    user_flow_schedule.manager = AuthUser.objects.filter(display_id=request.POST.get('manager_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number))).first()
                if request.POST.get('facility_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    if user_flow_schedule.offline:
                        user_flow_schedule.offline_facility = ReserveOfflineFacility.objects.filter(display_id=request.POST.get('facility_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number))).first()
                    if user_flow_schedule.online:
                        user_flow_schedule.online_facility = ReserveOnlineFacility.objects.filter(display_id=request.POST.get('facility_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number))).first()
                if user_flow_schedule.join == 0:
                    user_flow_schedule.join = join
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
                elif join == 2:
                    remove = re.compile(r"<[^>]*?>")
                    print(request.POST.get('message_type'))
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

                if change_flg:
                    flow_flg = False
                    for flow_item in ShopFlowItem.objects.filter(flow_tab=user_flow.flow_tab).order_by('y', 'x').all():
                        if flow_flg:
                            if flow_item.type == 6:
                                flow_template = ShopFlowTemplate.objects.filter(flow=flow_item).first()
                                push_card_type_message(user_flow.user, flow_template.template_cardtype, None)
                            if flow_item.type == 51:
                                break
                        if flow_item.type == 54:
                            flow_flg = True
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )