from django.core.management.base import BaseCommand

from linebot import LineBotApi

from flow.models import UserFlowActionReminder
from sign.models import ShopLine
from template.models import ShopTemplateTextItem

from common import send_textarea_replace
from line.action.message import push_text_message, push_image_message, push_video_message, push_card_type_message, push_button_message

import datetime
import re

class Command(BaseCommand):
    def handle(self, *args, **options):
        remove = re.compile(r"<[^>]*?>")
        send_flg = True
        for reminder_item in UserFlowActionReminder.objects.filter(action_date__lte=datetime.datetime.now()).order_by('flow__number').all():
            global line_bot_api
            shop_line = ShopLine.objects.filter(shop=reminder_item.user.shop).first()
            line_bot_api = LineBotApi(shop_line.channel_access_token)

            if reminder_item.template_text:
                for template_text_item in ShopTemplateTextItem.objects.filter(template=reminder_item.template_text).all():
                    if template_text_item.message_type == 0 or template_text_item.message_type == 1:
                        if template_text_item.text:
                            text = send_textarea_replace(template_text_item.text, line_info(shop_line), reminder_item.user)
                            if text:
                                push_text_message(reminder_item.user, remove.sub( '', text ), None)
                        else:
                            send_flg = False
                    elif template_text_item.message_type == 2:
                        push_image_message(reminder_item.user, template_text_item.image, None)
                    elif template_text_item.message_type == 3:
                        push_video_message(reminder_item.user, template_text_item.video, None)
            elif reminder_item.template_video:
                push_video_message(reminder_item.user, reminder_item.template_video.video, None)
            elif reminder_item.template_richmessage:
                print()
            elif reminder_item.template_richvideo:
                print()
            elif reminder_item.template_cardtype:
                push_card_type_message(reminder_item.user, reminder_item.template_cardtype, None)
            
            if send_flg:
                push_button_message(reminder_item.user)
                UserFlowActionReminder.objects.filter(id=reminder_item.id).all().delete()
        self.stdout.write(self.style.SUCCESS('send_action_reminder successfully!!'))

def line_info(shop):
    global line_bot_api
    line_bot_api = LineBotApi(shop.channel_access_token)
    return line_bot_api.get_bot_info()