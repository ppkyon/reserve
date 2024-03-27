from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, VideoSendMessage, FlexSendMessage

from PIL import Image

from sign.models import ShopLine
from talk.models import TalkMessage, TalkMessageCardType, TalkMessageCardTypeAnnounce, TalkMessageCardTypeAnnounceText, TalkMessageCardTypeAnnounceAction, TalkMessageCardTypeMore
from template.models import ShopTemplateCardTypeAnnounce, ShopTemplateCardTypeAnnounceText, ShopTemplateCardTypeAnnounceAction, ShopTemplateCardTypeMore

from common import create_code, send_action_replace

import cv2
import environ
import io
import os
import urllib.request as urllib_request
import uuid

env = environ.Env()
env.read_env('.env')

def push_text_message(user, message, author):
    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=user.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)

    TalkMessage.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(16, TalkMessage),
        user = user,
        line_user_id = user.line_user_id,
        message_type = 0,
        text = message,
        account_type = 1,
        author = author,
        send_date = timezone.datetime.now(),
    )
    line_bot_api.push_message(user.line_user_id, TextSendMessage(text=message))

def push_image_message(user, image, author):
    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=user.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)

    message = TalkMessage.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(16, TalkMessage),
        user = user,
        line_user_id = user.line_user_id,
        message_type = 1,
        image = image,
        account_type = 1,
        author = author,
        send_date = timezone.datetime.now(),
    )

    if env('AWS_FLG') == 'True':
        image_name = './static/' + str(uuid.uuid4()) + '.png'
        urllib_request.urlretrieve(message.image.url, image_name)
        image = cv2.imread(image_name)
    else:
        image = cv2.imread(message.image.url[1:])
    image_height, image_width = image.shape[:2]

    message.image_width = image_width
    message.image_height = image_height
    message.save()
    
    if env('AWS_FLG') == 'True':
        os.remove(image_name)

    if env('NGROK'):
        line_bot_api.push_message(user.line_user_id, ImageSendMessage(original_content_url=env('NGROK_URL') + message.image.url, preview_image_url=env('NGROK_URL') + message.image.url))
    else:
        line_bot_api.push_message(user.line_user_id, ImageSendMessage(original_content_url=env('DOMAIN_URL') + message.image.url, preview_image_url=env('DOMAIN_URL') + message.image.url))

def push_video_message(user, video, author):
    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=user.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)

    message = TalkMessage.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(16, TalkMessage),
        user = user,
        line_user_id = user.line_user_id,
        message_type = 2,
        video = video,
        account_type = 1,
        author = author,
        send_date = timezone.datetime.now(),
    )

    if env('AWS_FLG') == 'True':
        video_name = './static/' + str(uuid.uuid4()).replace('-', '') + '.mp4'
        urllib_request.urlretrieve(message.video.url, video_name)
        cap = cv2.VideoCapture(video_name)
    else:
        cap = cv2.VideoCapture(message.video.url[1:])
    video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    message.video_width = video_width
    message.video_height = video_height
    message.save()
    
    res, thumbnail = cap.read()
    image = Image.fromarray(cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB))
    image_io = io.BytesIO()
    image.save(image_io, format="JPEG")
    image_file = InMemoryUploadedFile(image_io, field_name=None, name=str(uuid.uuid4()).replace('-', '') + '.jpg', content_type="image/jpeg", size=image_io.getbuffer().nbytes, charset=None)
    message.video_thumbnail = image_file
    message.save()

    cap.release()
    if env('AWS_FLG') == 'True':
        os.remove(video_name)

    if env('NGROK'):
        line_bot_api.push_message(user.line_user_id, VideoSendMessage(original_content_url=env('NGROK_URL') + message.video.url, preview_image_url=env('NGROK_URL') + message.video_thumbnail.url))
    else:
        line_bot_api.push_message(user.line_user_id, VideoSendMessage(original_content_url=env('DOMAIN_URL') + message.video.url, preview_image_url=env('DOMAIN_URL') + message.video_thumbnail.url))

def push_card_type_message(user, template, author):
    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=user.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)

    message = TalkMessage.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(16, TalkMessage),
        user = user,
        line_user_id = user.line_user_id,
        message_type = 7,
        template_id = template.id,
        account_type = 1,
        author = author,
        send_date = timezone.datetime.now(),
    )
    message_card_type = TalkMessageCardType.objects.create(
        id = str(uuid.uuid4()),
        message = message,
        type = template.type,
        count = template.count,
    )

    carousel_contents = []
    if template.type == 1:
        for card_type_announce in ShopTemplateCardTypeAnnounce.objects.filter(template=template).order_by('number').all():
            message_card_type_announce = TalkMessageCardTypeAnnounce.objects.create(
                id = str(uuid.uuid4()),
                card_type = message_card_type,
                number = card_type_announce.number,
                title = card_type_announce.title,
                image_count = card_type_announce.image_count,
                image_1 = card_type_announce.image_1,
                image_2 = card_type_announce.image_2,
                image_3 = card_type_announce.image_3,
                image_flg = card_type_announce.image_flg,
                label = card_type_announce.label,
                label_color = card_type_announce.label_color,
                label_flg = card_type_announce.label_flg,
                description = card_type_announce.description,
                description_flg = card_type_announce.description_flg,
            )

            image_contents = []
            if card_type_announce.image_flg:
                image_1 = None
                image_2 = None
                image_3 = None
                if card_type_announce.image_count == '1':
                    if env('NGROK') == 'True':
                        image_1 = env('NGROK_URL') + card_type_announce.image_1.url
                    else:
                        image_1 = card_type_announce.image_1.url
                    image_contents.append(
                        {
                            "type": "image",
                            "url": image_1,
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "300:196",
                            "gravity": "center",
                            "flex": 1
                        }
                    )
                elif card_type_announce.image_count == '2':
                    if env('NGROK') == 'True':
                        image_1 = env('NGROK_URL') + card_type_announce.image_1.url
                        image_2 = env('NGROK_URL') + card_type_announce.image_2.url
                    else:
                        image_1 = card_type_announce.image_1.url
                        image_2 = card_type_announce.image_2.url

                    image_contents.append(
                        {
                            "type": "image",
                            "url": image_1,
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "150:196",
                            "gravity": "center",
                            "flex": 1
                        }
                    )
                    image_contents.append(
                        {
                            "type": "image",
                            "url": image_2,
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "150:196",
                            "gravity": "center",
                            "flex": 1
                        }
                    )
                elif card_type_announce.image_count == '3':
                    if env('NGROK') == 'True':
                        image_1 = env('NGROK_URL') + card_type_announce.image_1.url
                        image_2 = env('NGROK_URL') + card_type_announce.image_2.url
                        image_3 = env('NGROK_URL') + card_type_announce.image_3.url
                    else:
                        image_1 = card_type_announce.image_1.url
                        image_2 = card_type_announce.image_2.url
                        image_3 = card_type_announce.image_3.url

                    image_contents.append(
                        {
                            "type": "image",
                            "url": image_1,
                            "size": "full",
                            "aspectMode": "cover",
                            "aspectRatio": "150:196",
                            "gravity": "center",
                            "flex": 1
                        }
                    )
                    image_contents.append(
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "image",
                                    "url": image_2,
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "150:98",
                                    "gravity": "center"
                                },
                                {
                                    "type": "image",
                                    "url": image_3,
                                    "size": "full",
                                    "aspectMode": "cover",
                                    "aspectRatio": "150:98",
                                    "gravity": "center"
                                }
                            ],
                            "flex": 1
                        }
                    )
            else:
                if card_type_announce.label_flg:
                    image_contents.append(
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "height": "45px"
                        }
                    )
            
            if card_type_announce.label_flg:
                text_color = None
                back_color = None
                if card_type_announce.label_color == '0':
                    text_color = '#FFFFFF'
                    back_color = '#666F86'
                elif card_type_announce.label_color == '1':
                    text_color = '#666F86'
                    back_color = '#FFFFFF'
                elif card_type_announce.label_color == '2':
                    text_color = '#FFFFFF'
                    back_color = '#EB4E3D'
                elif card_type_announce.label_color == '3':
                    text_color = '#FFFFFF'
                    back_color = '#ED8537'
                elif card_type_announce.label_color == '4':
                    text_color = '#FFFFFF'
                    back_color = '#00B900'
                elif card_type_announce.label_color == '5':
                    text_color = '#FFFFFF'
                    back_color = '#5B82DB'
                image_contents.append(
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "text",
                                "text": card_type_announce.label,
                                "size": "xs",
                                "color": text_color,
                                "align": "center",
                                "gravity": "center"
                            }
                        ],
                        "backgroundColor": back_color,
                        "paddingAll": "2px",
                        "paddingStart": "4px",
                        "paddingEnd": "4px",
                        "flex": 0,
                        "position": "absolute",
                        "offsetStart": "18px",
                        "offsetTop": "18px",
                        "cornerRadius": "100px",
                        "width": "96px",
                        "height": "25px"
                    }
                )
            
            body_contents = []
            body_contents.append(
                {
                    "type": "text",
                    "contents": [],
                    "size": "xl",
                    "text": card_type_announce.title,
                    "color": "#000000",
                    "weight": "bold",
                    "wrap": True,
                }
            )
            if card_type_announce.description_flg:
                body_contents.append(
                    {
                        "type": "text",
                        "text": card_type_announce.description,
                        "color": "#000000",
                        "size": "md",
                        "margin": "md",
                        "wrap": True,
                    }
                )
            
            for card_type_announce_text in ShopTemplateCardTypeAnnounceText.objects.filter(card_type=card_type_announce).all():
                TalkMessageCardTypeAnnounceText.objects.create(
                    id = str(uuid.uuid4()),
                    card_type_announce = message_card_type_announce,
                    number = card_type_announce_text.number,
                    title = card_type_announce_text.title,
                    text = card_type_announce_text.text,
                    flg = card_type_announce_text.flg,
                )
                if card_type_announce_text.flg:
                    body_contents.append(
                        {
                            "type": "box",
                            "layout": "vertical",
                            "spacing": "sm",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": card_type_announce_text.title,
                                    "color": "#000000",
                                    "weight": "bold",
                                    "size": "md",
                                    "align": "start"
                                },
                                {
                                    "type": "text",
                                    "text": send_action_replace(card_type_announce_text.text, line_info(shop_line), user),
                                    "color": "#000000",
                                    "size": "md",
                                    "align": "start",
                                    "wrap": True,
                                }
                            ]
                        }
                    )
            
            action_contents = []
            for card_type_announce_action in ShopTemplateCardTypeAnnounceAction.objects.filter(card_type=card_type_announce).all():
                TalkMessageCardTypeAnnounceAction.objects.create(
                    id = str(uuid.uuid4()),
                    card_type_announce = message_card_type_announce,
                    number = card_type_announce_action.number,
                    label = card_type_announce_action.label,
                    type = card_type_announce_action.type,
                    url = card_type_announce_action.url,
                    text = card_type_announce_action.text,
                    button_type = card_type_announce_action.button_type,
                    button_color = card_type_announce_action.button_color,
                    button_background_color = card_type_announce_action.button_background_color,
                    flg = card_type_announce_action.flg,
                )
                if card_type_announce_action.flg:
                    if card_type_announce_action.button_color == 0:
                        color = '#666fb6'
                    elif card_type_announce_action.button_color == 1:
                        color = '#ffffff'
                    elif card_type_announce_action.button_color == 2:
                        color = '#eb4e3d'
                    elif card_type_announce_action.button_color == 3:
                        color = '#ed8537'
                    elif card_type_announce_action.button_color == 4:
                        color = '#00b900'
                    elif card_type_announce_action.button_color == 5:
                        color = '#5b82db'
                    
                    if card_type_announce_action.button_type == 0:
                        if card_type_announce_action.type == 5:
                            action_contents.append(
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "margin": "lg",
                                    "color": color,
                                    "action": {
                                        "type": "message",
                                        "label": card_type_announce_action.label,
                                        "text": card_type_announce_action.text
                                    }
                                }
                            )
                        else:
                            action_contents.append(
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "height": "sm",
                                    "margin": "lg",
                                    "color": color,
                                    "action": {
                                        "type": "uri",
                                        "label": card_type_announce_action.label,
                                        "uri": send_action_replace(card_type_announce_action.url, line_info(shop_line), user)
                                    }
                                }
                            )
                    elif card_type_announce_action.button_type == 1:
                        if card_type_announce_action.type == 5:
                            action_contents.append(
                                {
                                    "type": "button",
                                    "style": "link",
                                    "height": "sm",
                                    "margin": "lg",
                                    "color": color,
                                    "action": {
                                        "type": "message",
                                        "label": card_type_announce_action.label,
                                        "text": card_type_announce_action.text
                                    }
                                }
                            )
                        else:
                            action_contents.append(
                                {
                                    "type": "button",
                                    "style": "link",
                                    "height": "sm",
                                    "margin": "lg",
                                    "color": color,
                                    "action": {
                                        "type": "uri",
                                        "label": card_type_announce_action.label,
                                        "uri": send_action_replace(card_type_announce_action.url, line_info(shop_line), user)
                                    }
                                }
                            )
            
            carousel_contents.append(
                {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": image_contents
                            }
                        ],
                        "paddingAll": "0px"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": body_contents
                                    }
                                ]
                            }
                        ],
                        "backgroundColor": "#FFFFFF"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": action_contents
                    }
                }
            )
    elif template.type == 2:
        print()
    elif template.type == 3:
        print()
    elif template.type == 4:
        print()

    if ShopTemplateCardTypeMore.objects.filter(template=template).exists():
        card_type_more = ShopTemplateCardTypeMore.objects.filter(template=template).first()

        TalkMessageCardTypeMore.objects.create(
            id = str(uuid.uuid4()),
            card_type = message_card_type,
            template = card_type_more.template,
            image = card_type_more.image,
            action_label = card_type_more.action_label,
            action_type = card_type_more.action_type,
            action_url = card_type_more.action_url,
            action_text = card_type_more.action_text,
        )

        action_contents = []
        if card_type_more.template == 1:
            if card_type_more.action_type == 5:
                action_contents.append(
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": card_type_more.action_label,
                            "text": card_type_more.action_text
                        }
                    }
                )
            else:
                action_contents.append(
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": card_type_more.action_label,
                            "uri": card_type_more.action_url
                        }
                    }
                )
            carousel_contents.append(
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": action_contents,
                        "height": "100%",
                        "justifyContent": "center",
                        "alignItems": "center"
                    }
                }
            )
        elif card_type_more.template == 2:
            if card_type_more.action_type == 5:
                action_contents.append(
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": card_type_more.action_label,
                            "text": card_type_more.action_text
                        }
                    }
                )
            else:
                action_contents.append(
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": card_type_more.action_label,
                            "uri": card_type_more.action_url
                        }
                    }
                )
            carousel_contents.append(
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                        "size": "full",
                        "aspectRatio": "154:100",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": action_contents,
                        "justifyContent": "center",
                        "alignItems": "center"
                    }
                }
            )
    contents = {
        "type": "carousel",
        "contents": carousel_contents
    }

    line_bot_api.push_message(
        user.line_user_id,
        FlexSendMessage(
            alt_text=template.title,
            contents=contents,
        )
    )



def line_info(shop):
    global line_bot_api
    line_bot_api = LineBotApi(shop.channel_access_token)
    return line_bot_api.get_bot_info()