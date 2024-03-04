from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.urls import reverse

from PIL import Image

from template.models import HeadTemplateVideo

from head.template.action.list import get_video_list

from common import create_code, get_model_field
from table.action import action_search

import base64
import cv2
import environ
import io
import os
import time
import urllib.request as urllib_request
import uuid

env = environ.Env()
env.read_env('.env')

def save(request):
    if request.POST.get('id') and HeadTemplateVideo.objects.filter(display_id=request.POST.get('id')).exists():
        template = HeadTemplateVideo.objects.filter(display_id=request.POST.get('id')).first()
        template.name = request.POST.get('name')
        template.author = request.user.id
        template.save()
    else:
        template = HeadTemplateVideo.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateVideo),
            name = request.POST.get('name'),
            author = request.user.id,
        )
    
    if request.POST.get('video'):
        if ';base64,' in request.POST.get('video'):
            format, imgstr = request.POST.get('video').split(';base64,') 
            ext = format.split('/')[-1] 
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        else:
            data = request.POST.get('video')
        template.video = data
        template.save()

        if env('AWS_FLG') == 'True':
            video_name = './static/' + str(uuid.uuid4()).replace('-', '') + '.mp4'
            urllib_request.urlretrieve(template.video.url, video_name)
            cap = cv2.VideoCapture(video_name)
        else:
            cap = cv2.VideoCapture(template.video.url[1:])
        video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        video_time = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        video_size = request.POST.get('size')

        template.video_width = video_width
        template.video_height = video_height
        template.video_time = round(video_time)
        template.video_size = video_size
        template.save()
        
        res, thumbnail = cap.read()
        image = Image.fromarray(cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB))
        image_io = io.BytesIO()
        image.save(image_io, format="JPEG")
        image_file = InMemoryUploadedFile(image_io, field_name=None, name=str(uuid.uuid4()).replace('-', '') + '.jpg', content_type="image/jpeg", size=image_io.getbuffer().nbytes, charset=None)
        
        template.video_thumbnail = image_file
        template.save()

        cap.release()
        if env('AWS_FLG') == 'True':
            os.remove(video_name)
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def delete(request):
    HeadTemplateVideo.objects.filter(display_id=request.POST.get('id')).all().delete()
    return JsonResponse( {}, safe=False )

def copy(request):
    return JsonResponse( {'copy_url': reverse('head:template:edit_video') + '?copy=' + request.POST.get('id')}, safe=False )

def search(request):
    action_search(request, None, None)
    return JsonResponse( list(get_video_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_video_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    template = HeadTemplateVideo.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(HeadTemplateVideo)).first()
    template['video_display_time'] = time.strftime('%M:%S', time.gmtime(template['video_time']))
    return JsonResponse( template, safe=False )

def get_all(request):
    template_list = list(HeadTemplateVideo.objects.order_by('-created_at').values(*get_model_field(HeadTemplateVideo)).all())
    for template_index, template_item in enumerate(template_list):
        template_list[template_index]['video_display_time'] = time.strftime('%M:%S', time.gmtime(template_item['video_time']))
    return JsonResponse( template_list, safe=False )