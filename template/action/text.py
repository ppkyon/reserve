from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.urls import reverse

from PIL import Image

from sign.models import AuthLogin
from template.models import ShopTemplateText, ShopTemplateTextItem, ShopTemplateVideo, ShopTemplateRichMessage, ShopTemplateRichVideo, ShopTemplateCardType

from template.action.list import get_text_list

from common import create_code, display_textarea_replace, get_model_field
from table.action import action_search

import base64
import cv2
import environ
import io
import os
import urllib.request as urllib_request
import uuid

env = environ.Env()
env.read_env('.env')

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    favorite_flg = False
    if request.POST.get('favorite') == '1':
        favorite_flg = True

    if request.POST.get('id') and ShopTemplateText.objects.filter(display_id=request.POST.get('id')).exists():
        template = ShopTemplateText.objects.filter(display_id=request.POST.get('id')).first()
        template.name = request.POST.get('name')
        template.favorite_flg = favorite_flg
        template.author = request.user.id
        template.save()
    else:
        template = ShopTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, ShopTemplateText),
            company = auth_login.shop.company,
            shop = auth_login.shop,
            name = request.POST.get('name'),
            favorite_flg = favorite_flg,
            author = request.user.id,
        )

    ShopTemplateTextItem.objects.filter(template=template).all().delete()
    number = 1
    for i in range(int(request.POST.get('count'))):
        if request.POST.get('message_type_' + str( i + 1 )) == '1':
            if request.POST.get('text_' + str( i + 1 )):
                ShopTemplateTextItem.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = number,
                    message_type = request.POST.get('message_type_' + str( i + 1 )),
                    text = request.POST.get('text_' + str( i + 1 )),
                )
                number += 1
        elif request.POST.get('message_type_' + str( i + 1 )) == '2':
            if ';base64,' in request.POST.get('image_' + str( i + 1 )):
                format, imgstr = request.POST.get('image_' + str( i + 1 )).split(';base64,') 
                ext = format.split('/')[-1] 
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                data = request.POST.get('image_' + str( i + 1 ))
            
            template_item = ShopTemplateTextItem.objects.create(
                id = str(uuid.uuid4()),
                template = template,
                number = number,
                message_type = request.POST.get('message_type_' + str( i + 1 )),
                image = data,
            )

            if env('AWS_FLG') == 'True':
                image = cv2.imread(template_item.image)
            else:
                image = cv2.imread(template_item.image.url[1:])
            image_height, image_width = image.shape[:2]

            template_item.image_width = image_width
            template_item.image_height = image_height
            template_item.save()
            
            number += 1
        elif request.POST.get('message_type_' + str( i + 1 )) == '3':
            if ';base64,' in request.POST.get('video_' + str( i + 1 )):
                format, imgstr = request.POST.get('video_' + str( i + 1 )).split(';base64,') 
                ext = format.split('/')[-1] 
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                data = request.POST.get('video_' + str( i + 1 ))
                
            template_item = ShopTemplateTextItem.objects.create(
                id = str(uuid.uuid4()),
                template = template,
                number = number,
                message_type = request.POST.get('message_type_' + str( i + 1 )),
                video = data,
            )

            if env('AWS_FLG') == 'True':
                video_name = './static/' + str(uuid.uuid4()).replace('-', '') + '.mp4'
                urllib_request.urlretrieve(template_item.video.url, video_name)
                cap = cv2.VideoCapture(video_name)
            else:
                cap = cv2.VideoCapture(template_item.video.url[1:])
            video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            template_item.video_width = video_width
            template_item.video_height = video_height
            template_item.save()
            
            res, thumbnail = cap.read()
            image = Image.fromarray(cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB))
            image_io = io.BytesIO()
            image.save(image_io, format="JPEG")
            image_file = InMemoryUploadedFile(image_io, field_name=None, name=str(uuid.uuid4()).replace('-', '') + '.jpg', content_type="image/jpeg", size=image_io.getbuffer().nbytes, charset=None)
            template_item.video_thumbnail = image_file
            template_item.save()

            cap.release()
            if env('AWS_FLG') == 'True':
                os.remove(video_name)

            number += 1
        elif request.POST.get('message_type_' + str( i + 1 )) == '4':
            if request.POST.get('template_type_' + str( i + 1 )) == '0':
                ShopTemplateTextItem.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = number,
                    message_type = request.POST.get('message_type_' + str( i + 1 )),
                    template_text = ShopTemplateText.objects.filter(display_id=request.POST.get('template_' + str( i + 1 ))).first(),
                )
            elif request.POST.get('template_type_' + str( i + 1 )) == '1':
                ShopTemplateTextItem.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = number,
                    message_type = request.POST.get('message_type_' + str( i + 1 )),
                    template_video = ShopTemplateVideo.objects.filter(display_id=request.POST.get('template_' + str( i + 1 ))).first(),
                )
            elif request.POST.get('template_type_' + str( i + 1 )) == '2':
                ShopTemplateTextItem.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = number,
                    message_type = request.POST.get('message_type_' + str( i + 1 )),
                    template_richmessage = ShopTemplateRichMessage.objects.filter(display_id=request.POST.get('template_' + str( i + 1 ))).first(),
                )
            elif request.POST.get('template_type_' + str( i + 1 )) == '3':
                ShopTemplateTextItem.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = number,
                    message_type = request.POST.get('message_type_' + str( i + 1 )),
                    template_richvideo = ShopTemplateRichVideo.objects.filter(display_id=request.POST.get('template_' + str( i + 1 ))).first(),
                )
            elif request.POST.get('template_type_' + str( i + 1 )) == '4':
                ShopTemplateTextItem.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = number,
                    message_type = request.POST.get('message_type_' + str( i + 1 )),
                    template_cardtype = ShopTemplateCardType.objects.filter(display_id=request.POST.get('template_' + str( i + 1 ))).first(),
                )
            number += 1
    
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def delete(request):
    template = ShopTemplateText.objects.filter(display_id=request.POST.get('id')).first()
    ShopTemplateTextItem.objects.filter(template=template).all().delete()
    template.delete()
    return JsonResponse( {}, safe=False )

def favorite(request):
    template = ShopTemplateText.objects.filter(display_id=request.POST.get('id')).first()
    if template.favorite_flg:
        template.favorite_flg = False
    else:
        template.favorite_flg = True
    template.save()
    return JsonResponse( {'check': template.favorite_flg}, safe=False )

def copy(request):
    return JsonResponse( {'copy_url': reverse('template:edit_text') + '?copy=' + request.POST.get('id')}, safe=False )

def search(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    action_search(request, auth_login.shop, auth_login.shop.company)
    return JsonResponse( list(get_text_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_text_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    template = ShopTemplateText.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(ShopTemplateText)).first()
    template['item'] = list(ShopTemplateTextItem.objects.filter(template__id=template['id']).values(*get_model_field(ShopTemplateTextItem)).all())
    return JsonResponse( template, safe=False )

def get_all(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    template_list = list(ShopTemplateText.objects.filter(company=auth_login.shop.company, shop=auth_login.shop).order_by('-created_at').values(*get_model_field(ShopTemplateText)).all())
    for template_index, template_item in enumerate(template_list):
        template_list[template_index]['item'] = ShopTemplateTextItem.objects.filter(template__id=template_item['id']).order_by('number').values(*get_model_field(ShopTemplateTextItem)).first()
    return JsonResponse( template_list, safe=False )

def preview(request):
    template = ShopTemplateText.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(ShopTemplateText)).first()
    template['item'] = list(ShopTemplateTextItem.objects.filter(template__id=template['id']).values(*get_model_field(ShopTemplateTextItem)).all())
    for template_index, template_item in enumerate(template['item']):
        if template_item['text']:
            template['item'][template_index]['text'] = display_textarea_replace(template_item['text'])
    return JsonResponse( template, safe=False )