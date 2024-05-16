from django.db.models import Q
from django.http import JsonResponse

from linebot import LineBotApi

from flow.models import ShopFlowTab, ShopFlowItem, ShopFlowRichMenu, UserFlow, UserFlowSchedule
from reserve.models import ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
from richmenu.models import UserRichMenu
from sign.models import AuthLogin, ShopLine
from tag.models import ShopTag, UserHashTag
from template.models import ShopTemplateTextItem, ShopTemplateVideo, ShopTemplateCardType
from user.models import LineUser, UserProfile

from common import create_code, send_textarea_replace, get_model_field
from line.action.common import line_info
from line.action.message import push_text_message, push_image_message, push_video_message, push_card_type_message
from line.action.richmenu import create_rich_menu, delete_rich_menu
from user.action.list import get_list

import phonenumbers
import re
import uuid

def save(request):
    birth = None
    if request.POST.get('birth'):
        birth = request.POST.get('birth')
    age = 0
    if request.POST.get('age'):
        age = request.POST.get('age')
    sex = 0
    if request.POST.get('sex'):
        sex = request.POST.get('sex')

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).first()
    if UserProfile.objects.filter(user=user).exists():
        user_profile = UserProfile.objects.filter(user=user).first()
        user_profile.email = request.POST.get('email')
        user_profile.name = request.POST.get('name')
        user_profile.name_kana = request.POST.get('name_kana')
        user_profile.birth = birth
        user_profile.age = age
        user_profile.sex = sex
        user_profile.phone_number = request.POST.get('phone_number').replace('-', '')
        user_profile.memo = request.POST.get('memo')
        user_profile.save()
    else:
        UserProfile.objects.create(
            id = str(uuid.uuid4()),
            user = user,
            email = request.POST.get('email'),
            name = request.POST.get('name'),
            name_kana = request.POST.get('name_kana'),
            birth = birth,
            age = age,
            sex = sex,
            phone_number = request.POST.get('phone_number').replace('-', ''),
            memo = request.POST.get('memo'),
        )
    
    UserHashTag.objects.filter(user=user).all().delete()
    if request.POST.get('tag[]'):
        for tag_index, tag_item in enumerate( request.POST.get('tag[]').split(',') ):
            if not UserHashTag.objects.filter(tag=ShopTag.objects.filter(display_id=tag_item).first()).exists():
                UserHashTag.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    number = (tag_index+1),
                    tag = ShopTag.objects.filter(display_id=tag_item).first()
                )
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).values(*get_model_field(LineUser)).first()

    user['profile'] = UserProfile.objects.filter(user__id=user['id']).values(*get_model_field(UserProfile)).first()
    if user['profile'] and user['profile']['birth']:
        user['profile']['display_birth'] = user['profile']['birth'].strftime('%Y年%m月%d日')
    if user['profile'] and user['profile']['phone_number']:
        user['profile']['phone_number'] = phonenumbers.format_number(phonenumbers.parse(user['profile']['phone_number'], 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
    user['display_date'] = user['created_at'].strftime('%Y年%m月%d日 %H:%M')
    if user['profile']['updated_at']:
        user['profile']['updated_at'] = user['profile']['updated_at'].strftime('%Y/%m/%d')

    user['active_flow'] = UserFlow.objects.filter(user__id=user['id'], end_flg=False).order_by('flow_tab__number').values(*get_model_field(UserFlow)).first()
    if user['active_flow']:
        user['active_flow']['tab'] = ShopFlowTab.objects.filter(id=user['active_flow']['flow_tab']).values(*get_model_field(ShopFlowTab)).first()
    
    user['tag'] = list(UserHashTag.objects.filter(user__id=user['id']).values(*get_model_field(UserHashTag)).all())
    for user_tag_index, user_tag_item in enumerate(user['tag']):
        user['tag'][user_tag_index]['tag'] = ShopTag.objects.filter(id=user_tag_item['tag']).values(*get_model_field(ShopTag)).first()

    return JsonResponse( user, safe=False )



def member(request):
    birth = None
    if request.POST.get('birth'):
        birth = request.POST.get('birth')
    age = 0
    if request.POST.get('age'):
        age = request.POST.get('age')
    sex = 0
    if request.POST.get('sex'):
        sex = request.POST.get('sex')

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).first()
    user.member_flg = True
    user.save()

    if UserProfile.objects.filter(user=user).exists():
        user_profile = UserProfile.objects.filter(user=user).first()
        user_profile.email = request.POST.get('email')
        user_profile.name = request.POST.get('name')
        user_profile.name_kana = request.POST.get('name_kana')
        user_profile.birth = birth
        user_profile.age = age
        user_profile.sex = sex
        user_profile.phone_number = request.POST.get('phone_number').replace('-', '')
        user_profile.save()
    else:
        UserProfile.objects.create(
            id = str(uuid.uuid4()),
            user = user,
            email = request.POST.get('email'),
            name = request.POST.get('name'),
            name_kana = request.POST.get('name_kana'),
            birth = birth,
            age = age,
            sex = sex,
            phone_number = request.POST.get('phone_number').replace('-', ''),
        )

    for user_flow in UserFlow.objects.filter(user=user, flow_tab__member=0).order_by('number').all():
        user_flow.end_flg = True
        user_flow.save()

    if not UserFlow.objects.filter(Q(user=user), Q(Q(flow_tab__member=1)|Q(flow_tab__member=2))).order_by('number').exists():
        user_flow = UserFlow.objects.filter(user=user).order_by('number').first()
        for flow_tab in ShopFlowTab.objects.filter(Q(flow=user_flow.flow), Q(Q(member=1)|Q(member=2))).order_by('number').all():
            target_flow_item = None
            target_rich_menu = None
            for flow_item in ShopFlowItem.objects.filter(flow_tab=flow_tab).all():
                if flow_item.type == 7:
                    target_rich_menu = ShopFlowRichMenu.objects.filter(flow=flow_item).first()
                    target_rich_menu = target_rich_menu.rich_menu
                if flow_item.type == 10:
                    target_flow_item = flow_item
                    break
            
            delete_rich_menu(user)
            if target_rich_menu:
                UserRichMenu.objects.filter(user=user).all().delete()
                UserRichMenu.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    rich_menu = target_rich_menu
                )
                create_rich_menu(user)

            user_flow = UserFlow.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                user = user,
                number = UserFlow.objects.filter(user=user).count() + 1,
                flow = flow_tab.flow,
                flow_tab = flow_tab,
                flow_item = target_flow_item,
                name = flow_tab.name,
                richmenu = target_rich_menu,
                end_flg = False,
            )
            if not UserFlowSchedule.objects.filter(flow=user_flow, join=0, temp_flg=False).exclude(number=0).exists():
                reserve_offline_flow = ReserveOfflineFlowMenu.objects.filter(shop=user.shop, flow=flow_tab.name).order_by('offline__number').first()
                reserve_online_flow = ReserveOnlineFlowMenu.objects.filter(shop=user.shop, flow=flow_tab.name).order_by('online__number').first()
                if reserve_offline_flow:
                    if reserve_offline_flow.offline:
                        UserFlowSchedule.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, UserFlow),
                            flow = user_flow,
                            number = UserFlowSchedule.objects.filter(flow=user_flow, temp_flg=False).exclude(number=0).count() + 1,
                            date = None,
                            time = None,
                            join = 0,
                            offline = reserve_offline_flow.offline,
                            offline_course = None,
                            offline_facility = None,
                            manager = None,
                            question = None,
                        )
                elif reserve_online_flow:
                    if reserve_online_flow.online:
                        UserFlowSchedule.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, UserFlow),
                            flow = user_flow,
                            number = UserFlowSchedule.objects.filter(flow=user_flow, temp_flg=False).exclude(number=0).count() + 1,
                            date = None,
                            time = None,
                            join = 0,
                            online = reserve_online_flow.online,
                            online_course = None,
                            online_facility = None,
                            manager = None,
                            question = None,
                        )
            break
    
    remove = re.compile(r"<[^>]*?>")
    if request.POST.get('message_type') == '1':
        push_text_message(user, remove.sub( '', request.POST.get('message') ), None)
    elif request.POST.get('message_type') == '2':
        if request.POST.get('message_template_type') == '0':
            global line_bot_api
            shop_line = ShopLine.objects.filter(shop=auth_login.shop).first()
            line_bot_api = LineBotApi(shop_line.channel_access_token)

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

    return JsonResponse( {}, safe=False )