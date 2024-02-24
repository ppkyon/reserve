from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.urls import reverse

from PIL import Image

from template.models import HeadTemplateText, HeadTemplateTextItem

from head.template.action.list import get_text_list

from common import create_code, get_model_field
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
    if request.POST.get('id') and HeadTemplateText.objects.filter(display_id=request.POST.get('id')).exists():
        template = HeadTemplateText.objects.filter(display_id=request.POST.get('id')).first()
        template.name = request.POST.get('name')
        template.author = request.user.id
        template.save()
    else:
        template = HeadTemplateText.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateText),
            name = request.POST.get('name'),
            author = request.user.id,
        )

    HeadTemplateTextItem.objects.filter(template=template).all().delete()
    number = 1
    for i in range(int(request.POST.get('count'))):
        if request.POST.get('message_type_' + str( i + 1 )) == '1':
            if request.POST.get('text_' + str( i + 1 )):
                HeadTemplateTextItem.objects.create(
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
            
            template_item = HeadTemplateTextItem.objects.create(
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
                
            template_item = HeadTemplateTextItem.objects.create(
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
    
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def delete(request):
    template = HeadTemplateText.objects.filter(display_id=request.POST.get('id')).first()
    HeadTemplateTextItem.objects.filter(template=template).all().delete()
    template.delete()
    return JsonResponse( {}, safe=False )

def copy(request):
    return JsonResponse( {'copy_url': reverse('head:template:edit_text') + '?copy=' + request.POST.get('id')}, safe=False )

def search(request):
    action_search(request, None, None)
    return JsonResponse( list(get_text_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_text_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    template = HeadTemplateText.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(HeadTemplateText)).first()
    template['item'] = list(HeadTemplateTextItem.objects.filter(template__id=template['id']).values(*get_model_field(HeadTemplateTextItem)).all())
    return JsonResponse( template, safe=False )