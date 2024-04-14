from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from question.models import UserQuestion, UserQuestionItem, UserQuestionItemChoice
from flow.models import (
    ShopFlow, ShopFlowTab, ShopFlowItem,
    UserFlow, UserFlowTimer
)
from richmenu.models import UserRichMenu, UserRichMenuClick
from sign.models import AuthShop, ShopLine
from user.models import LineUser, UserProfile

from common import create_code
from flow.action.go import go
from line.action.message import push_text_message

import datetime
import uuid

@csrf_exempt
def callback(request, login):
    global line_bot_api
    global handler

    body = request.body.decode('utf-8')
    type = None

    if not '"events":[]' in body:
        line_user_id = body[body.find(',"userId":"')+len(',"userId":"'):]
        line_user_id = line_user_id[:line_user_id.find('"},')]

        shop = AuthShop.objects.filter(display_id=login).first()
        shop_line = ShopLine.objects.filter(shop=shop).first()
        if not LineUser.objects.filter(shop=shop, line_user_id=line_user_id).exists():
            LineUser.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, LineUser),
                shop = shop,
                line_user_id = line_user_id,
            )
        
        line_bot_api = LineBotApi(shop_line.channel_access_token)
        handler = WebhookHandler(shop_line.channel_secret)

        type = body[body.find(':[{"type":"')+len(':[{"type":"'):]
        type = type[:type.find('","')]

    try:
        if type:
            if type == 'follow':
                handle_follow(line_user_id, shop)
            elif type == 'unfollow':
                handle_unfollow(line_user_id, shop)
            elif type == 'message':
                handle_message(line_user_id, shop, body)
    except InvalidSignatureError:
        HttpResponseForbidden()
    return HttpResponse('OK', status=200)

def handle_follow(line_user_id, shop):
    user = update_user(line_user_id, shop)
    user.member_flg = False
    user.save()

    UserFlow.objects.filter(user=user).all().delete()
    UserFlowTimer.objects.filter(user=user).all().delete()
    UserRichMenu.objects.filter(user=user).all().delete()
    UserRichMenuClick.objects.filter(user=user).all().delete()
    for user_question in UserQuestion.objects.filter(user=user).all():
        for user_question_item in UserQuestionItem.objects.filter(user=user_question).all():
            UserQuestionItemChoice.objects.filter(user=user_question_item).all().delete()
        UserQuestionItem.objects.filter(user=user_question).all().delete()
    UserQuestion.objects.filter(user=user).all().delete()
        
    flow = None
    if ShopFlow.objects.filter(shop=shop, period_from__lte=datetime.datetime.now(), period_to__isnull=True, delete_flg=False).exists():
        flow = ShopFlow.objects.filter(shop=shop, period_from__lte=datetime.datetime.now(), period_to__isnull=True, delete_flg=False).first()
    elif ShopFlow.objects.filter(shop=shop, period_to__gte=datetime.datetime.now(), period_from__isnull=True, delete_flg=False).exists():
        flow = ShopFlow.objects.filter(shop=shop, period_to__gte=datetime.datetime.now(), period_from__isnull=True, delete_flg=False).first()
    elif ShopFlow.objects.filter(shop=shop, period_from__lte=datetime.datetime.now(), period_to__gte=datetime.datetime.now(), delete_flg=False).exists():
        flow = ShopFlow.objects.filter(shop=shop, period_from__lte=datetime.datetime.now(), period_to__gte=datetime.datetime.now(), delete_flg=False).first()
    
    if flow:
        action_flg = False
        for flow_tab in ShopFlowTab.objects.filter(flow=flow).order_by('number').all():
            if UserFlow.objects.filter(flow_tab=flow_tab, user=user).exists():
                flow_flg = False
                for flow_item in ShopFlowItem.objects.filter(flow_tab=flow_tab).order_by('x','y').all():
                    if flow_item.type and UserFlow.objects.filter(flow_item=flow_item, user=user).exists():
                        flow_flg = True
                    if flow_flg:
                        if go(user, flow, flow_tab, flow_item):
                            action_flg = True
                            break
            else:
                if action_flg:
                    break
                else:
                    for flow_item in ShopFlowItem.objects.filter(flow_tab=flow_tab).order_by('x','y').all():
                        if flow_item.type:
                            if go(user, flow, flow_tab, flow_item):
                                action_flg = True
                                break
    else:
        text = 'ご登録ありがとうございます。\n只今、採用募集期間外となっております。\n採用募集再開の際にこちらへメッセージを送信致しますのでしばらくお待ちください。'
        push_text_message(user, text, None)

def handle_unfollow(line_user_id, shop):
    if LineUser.objects.filter(shop=shop, line_user_id=line_user_id).exists():
        line_user = LineUser.objects.filter(shop=shop, line_user_id=line_user_id).first()
        line_user.status = 2
        line_user.save()
    else:
        line_user = LineUser.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, LineUser),
            shop = shop,
            line_user_id = line_user_id,
            status = 2,
        )

    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)
    line_bot_api.unlink_rich_menu_from_user(line_user_id)

def handle_message(line_user_id, shop, body):
    user = update_user(line_user_id, shop)
    return None



def update_user(line_user_id, shop):
    global line_bot_api

    line_user = LineUser.objects.filter(shop=shop, line_user_id=line_user_id).first()
    shop_line = ShopLine.objects.filter(shop=shop).first()

    line_bot_api = LineBotApi(shop_line.channel_access_token)
    line_profile = line_bot_api.get_profile(line_user_id)

    if LineUser.objects.filter(shop=shop, line_user_id=line_user_id).exists():
        line_user = LineUser.objects.filter(shop=shop, line_user_id=line_user_id).first()
        line_user.display_name = line_profile.display_name
        line_user.display_image = line_profile.picture_url
        line_user.status = 1
        line_user.updated_at = datetime.datetime.now()
        line_user.save()
    else:
        line_user = LineUser.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, LineUser),
            shop = shop,
            line_user_id = line_user_id,
            display_name = line_profile.display_name,
            display_image = line_profile.picture_url,
            status = 1,
            updated_at = datetime.datetime.now(),
        )
    
    if UserProfile.objects.filter(user=line_user).exists():
        user_profile = UserProfile.objects.filter(user=line_user).first()
        if not user_profile.atelle_id:
            user_profile.atelle_id = create_atelle_id(),
            user_profile.save()
    else:
        UserProfile.objects.create(
            id = str(uuid.uuid4()),
            user = line_user,
            atelle_id = create_atelle_id(),
        )

    return line_user

def create_atelle_id():
    code_list = UserProfile.objects.values_list('atelle_id', flat=True)
    number = 1
    while True:
        code = datetime.datetime.now().strftime('%Y%m%d') + str(number).zfill(2)
        if int(code) not in code_list:
            break
        number += 1
    return int(code)