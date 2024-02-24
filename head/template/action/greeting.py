from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from PIL import Image

from template.models import HeadTemplateGreeting

from common import create_code

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
    HeadTemplateGreeting.objects.all().delete()

    number = 1
    for i in range(int(request.POST.get('count'))):
        if request.POST.get('message_type_' + str( i + 1 )) == '1':
            if request.POST.get('text_' + str( i + 1 )):
                HeadTemplateGreeting.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, HeadTemplateGreeting),
                    number = number,
                    message_type = request.POST.get('message_type_' + str( i + 1 )),
                    text = request.POST.get('text_' + str( i + 1 )),
                    author = request.user.id,
                )
                number += 1
        elif request.POST.get('message_type_' + str( i + 1 )) == '2':
            if ';base64,' in request.POST.get('image_' + str( i + 1 )):
                format, imgstr = request.POST.get('image_' + str( i + 1 )).split(';base64,') 
                ext = format.split('/')[-1] 
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                data = request.POST.get('image_' + str( i + 1 ))
            
            template = HeadTemplateGreeting.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, HeadTemplateGreeting),
                number = number,
                message_type = request.POST.get('message_type_' + str( i + 1 )),
                image = data,
                author = request.user.id,
            )

            if env('AWS_FLG') == 'True':
                image = cv2.imread(template.image)
            else:
                image = cv2.imread(template.image.url[1:])
            image_height, image_width = image.shape[:2]

            template.image_width = image_width
            template.image_height = image_height
            template.save()
            
            number += 1
        elif request.POST.get('message_type_' + str( i + 1 )) == '3':
            if ';base64,' in request.POST.get('video_' + str( i + 1 )):
                format, imgstr = request.POST.get('video_' + str( i + 1 )).split(';base64,') 
                ext = format.split('/')[-1] 
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            else:
                data = request.POST.get('video_' + str( i + 1 ))
                
            template_greeting = HeadTemplateGreeting.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, HeadTemplateGreeting),
                number = number,
                message_type = request.POST.get('message_type_' + str( i + 1 )),
                video = data,
                author = request.user.id,
            )

            if env('AWS_FLG') == 'True':
                video_name = './static/' + str(uuid.uuid4()).replace('-', '') + '.mp4'
                urllib_request.urlretrieve(template_greeting.video.url, video_name)
                cap = cv2.VideoCapture(video_name)
            else:
                cap = cv2.VideoCapture(template_greeting.video.url[1:])
            video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            template_greeting.video_width = video_width
            template_greeting.video_height = video_height
            template_greeting.save()
            
            res, thumbnail = cap.read()
            image = Image.fromarray(cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB))
            image_io = io.BytesIO()
            image.save(image_io, format="JPEG")
            image_file = InMemoryUploadedFile(image_io, field_name=None, name=str(uuid.uuid4()).replace('-', '') + '.jpg', content_type="image/jpeg", size=image_io.getbuffer().nbytes, charset=None)
            template_greeting.video_thumbnail = image_file
            template_greeting.save()

            cap.release()
            if env('AWS_FLG') == 'True':
                os.remove(video_name)

            number += 1

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )