from django.core.files.base import ContentFile
from django.http import JsonResponse

from linebot import LineBotApi

from sign.models import AuthLogin, ShopLine
from template.models import ShopTemplateText, ShopTemplateTextItem, ShopTemplateVideo, ShopTemplateRichMessage, ShopTemplateRichVideo, ShopTemplateCardType
from user.models import LineUser

from common import send_textarea_replace
from line.action.message import push_text_message, push_image_message, push_video_message, push_card_type_message

import base64
import re

def text(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).first()
    push_text_message(user, request.POST.get('message'), request.user.id)
    return JsonResponse( {}, safe=False )

def image(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).first()

    format, imgstr = request.POST.get('image').split(';base64,') 
    ext = format.split('/')[-1] 
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

    push_image_message(user, data, request.user.id)
    return JsonResponse( {}, safe=False )

def video(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).first()

    format, imgstr = request.POST.get('video').split(';base64,') 
    ext = format.split('/')[-1] 
    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

    push_video_message(user, data, request.user.id)
    return JsonResponse( {}, safe=False )

def template(request):
    remove = re.compile(r"<[^>]*?>")
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    shop_line = ShopLine.objects.filter(shop=auth_login.shop).first()

    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('user_id')).first()
    if request.POST.get('type') == 'text':
        template = ShopTemplateText.objects.filter(display_id=request.POST.get('id')).first()
        for template_text_item in ShopTemplateTextItem.objects.filter(template=template).all():
            if template_text_item.message_type == 0 or template_text_item.message_type == 1:
                if template_text_item.text:
                    text = send_textarea_replace(template_text_item.text, line_info(shop_line), user)
                    if text:
                        push_text_message(user, remove.sub( '', text ), request.user.id)
            elif template_text_item.message_type == 2:
                push_image_message(user, template_text_item.image, request.user.id)
            elif template_text_item.message_type == 3:
                push_video_message(user, template_text_item.video, request.user.id)
    elif request.POST.get('type') == 'video':
        template_video = ShopTemplateVideo.objects.filter(display_id=request.POST.get('id')).first()
        push_video_message(user, template_video.video, request.user.id)
    elif request.POST.get('type') == 'richmessage':
        template_richmessage = ShopTemplateRichMessage.objects.filter(display_id=request.POST.get('id')).first()
        print()
    elif request.POST.get('type') == 'richvideo':
        template_richvideo = ShopTemplateRichVideo.objects.filter(display_id=request.POST.get('id')).first()
        print()
    elif request.POST.get('type') == 'cardtype':
        template_cardtype = ShopTemplateCardType.objects.filter(display_id=request.POST.get('id')).first()
        push_card_type_message(user, template_cardtype, request.user.id)
    return JsonResponse( {}, safe=False )

def line_info(shop):
    global line_bot_api
    line_bot_api = LineBotApi(shop.channel_access_token)
    return line_bot_api.get_bot_info()