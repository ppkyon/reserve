
from linebot import LineBotApi

from flow.models import (
    ShopFlowTab, ShopFlowItem, ShopFlowTemplate, ShopFlowRichMenu, ShopFlowTimer, ShopFlowStep,
    UserFlow, UserFlowTimer, UserFlowHistory
)
from richmenu.models import UserRichMenu
from sign.models import ShopLine
from template.models import ShopTemplateGreeting

from common import create_code, send_textarea_replace
from dateutil.relativedelta import relativedelta
from line.action.message import push_text_message, push_image_message, push_video_message, push_card_type_message
from line.action.richmenu import create_rich_menu, delete_rich_menu

import datetime
import re
import uuid

def go(user, flow, flow_tab, flow_item):
    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=user.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)

    remove = re.compile(r"<[^>]*?>")
    if flow_item.type:
        if flow_item.type == 1:
            template_greeting = ShopTemplateGreeting.objects.filter(shop=user.shop).order_by('number').all()
            for template_greeting_item in template_greeting:
                if template_greeting_item.message_type == 1:
                    text = send_textarea_replace( template_greeting_item.text, line_info(shop_line), user )
                    if text:
                        push_text_message(user, remove.sub( '', text ), None)
                elif template_greeting_item.message_type == 2:
                    push_image_message(user, template_greeting_item.image, None)
                elif template_greeting_item.message_type == 3:
                    push_video_message(user, template_greeting_item.video, None)
        elif flow_item.type == 2:
            print()
        elif flow_item.type == 3:
            print()
        elif flow_item.type == 4:
            print()
        elif flow_item.type == 5:
            print()
        elif flow_item.type == 6:
            flow_template = ShopFlowTemplate.objects.filter(flow=flow_item).first()
            push_card_type_message(user, flow_template.template_cardtype, None)
        elif flow_item.type == 7:
            flow_rich_menu = ShopFlowRichMenu.objects.filter(flow=flow_item).first()
            delete_rich_menu(user)
            if flow_rich_menu.rich_menu:
                UserRichMenu.objects.filter(user=user).all().delete()
                UserRichMenu.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    rich_menu = flow_rich_menu.rich_menu
                )
                create_rich_menu(user)
            
            UserFlowHistory.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlowHistory),
                user = user,
                number = UserFlowHistory.objects.filter(user=user).count() + 1,
                flow = flow_tab,
                name = flow_tab.name,
                richmenu = flow_rich_menu.rich_menu,
                start_flg = True,
                pass_flg = False,
                end_flg = False,
            )
        elif flow_item.type == 8:
            print()
        elif flow_item.type == 9:
            if UserFlow.objects.filter(flow_tab=flow_tab, user=user).exists():
                user_flow = UserFlow.objects.filter(flow_tab=flow_tab, user=user).first()
                user_flow.end_flg = True
                user_flow.save()
            else:
                user_flow = UserFlow.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    flow = flow,
                    flow_tab = flow_tab,
                    flow_item = flow_item,
                    end_flg = True,
                )
            for user_flow_history_index, user_flow_history in enumerate(UserFlowHistory.objects.filter(user=user, flow=flow_tab).all()):
                if (user_flow_history_index+1) == UserFlowHistory.objects.filter(user=user, flow=flow_tab).count():
                    user_flow_history.end_flg = True
                    user_flow_history.save()
                else:
                    user_flow_history.pass_flg = True
                    user_flow_history.save()

            flow_step = ShopFlowStep.objects.filter(flow=flow_item).first()
            flow_tab = ShopFlowTab.objects.filter(flow=user_flow.flow, value=flow_step.tab.value).first()
            UserFlow.objects.create(
                id = str(uuid.uuid4()),
                user = user,
                flow = user_flow.flow,
                flow_tab = flow_tab,
                flow_item = ShopFlowItem.objects.filter(flow_tab=flow_tab, x=1, y=1).first(),
            )

            UserFlowHistory.objects.filter(user=user).first()
            return True
        elif flow_item.type == 10:
            UserFlow.objects.filter(user=user, flow_tab=flow_tab).all().delete()
            UserFlow.objects.create(
                id = str(uuid.uuid4()),
                user = user,
                flow = flow,
                flow_tab = flow_tab,
                flow_item = flow_item,
            )
            return True
        elif flow_item.type == 11:
            print()
        elif flow_item.type == 51:
            UserFlow.objects.filter(user=user, flow_tab=flow_tab).all().delete()
            UserFlow.objects.create(
                id = str(uuid.uuid4()),
                user = user,
                flow = flow,
                flow_tab = flow_tab,
                flow_item = flow_item,
            )
            return True
        elif flow_item.type == 52:
            flow_timer = ShopFlowTimer.objects.filter(flow=flow_item).first()
            if not flow_timer.type == 0:
                UserFlow.objects.filter(user=user, flow_tab=flow_tab).all().delete()
                UserFlow.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    flow = flow,
                    flow_tab = flow_tab,
                    flow_item = flow_item,
                )

                action_date = None
                if flow_timer.type == 1:
                    today = datetime.datetime.now()
                    action_date = today + relativedelta(days=+flow_timer.date)
                    action_date = action_date.replace(hour=flow_timer.time.hour, minute=flow_timer.time.minute, second=0, microsecond=0)
                elif flow_timer.type == 2:
                    today = datetime.datetime.now()
                    action_date = today + relativedelta(days=+flow_timer.date)
                    action_date = action_date + relativedelta(hours=+flow_timer.time.hour)
                    action_date = action_date + relativedelta(minutes=+flow_timer.time.minute)
                    action_date = action_date.replace(second=0, microsecond=0)
                
                UserFlowTimer.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    action_date = action_date,
                )
                return True
        elif flow_item.type == 53:
            print()
        elif flow_item.type == 54:
            print()
        elif flow_item.type == 55:
            print()

    return False

def line_info(shop):
    global line_bot_api
    line_bot_api = LineBotApi(shop.channel_access_token)
    return line_bot_api.get_bot_info()