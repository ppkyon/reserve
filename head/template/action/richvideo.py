from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.urls import reverse

from PIL import Image

from template.models import HeadTemplateRichVideo

from head.template.action.list import get_richvideo_list

from common import create_code, resize_image, get_model_field
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
    if request.POST.get('id') and HeadTemplateRichVideo.objects.filter(display_id=request.POST.get('id')).exists():
        template = HeadTemplateRichVideo.objects.filter(display_id=request.POST.get('id')).first()
        template.name = request.POST.get('name')
        template.title = request.POST.get('title')
        template.author = request.user.id
        template.save()
    else:
        template = HeadTemplateRichVideo.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateRichVideo),
            name = request.POST.get('name'),
            title = request.POST.get('title'),
            author = request.user.id,
        )

    if request.POST.get('video'):
        if ';base64,' in request.POST.get('video'):
            format, imgstr = request.POST.get('video').split(';base64,') 
            ext = format.split('/')[-1] 
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        else:
            data = request.POST.get('video')

        display_flg = False
        if request.POST.get('display') == '1':
            display_flg = True
        
        template.video = data
        template.display_flg = display_flg
        template.url = request.POST.get('url')
        template.text = request.POST.get('text')
        template.custom = request.POST.get('custom')
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
        template.video_thumbnail240 = resize_image(thumbnail, 240, 240, 'jpg')
        template.video_thumbnail300 = resize_image(thumbnail, 300, 300, 'jpg')
        template.video_thumbnail460 = resize_image(thumbnail, 460, 460, 'jpg')
        template.video_thumbnail700 = resize_image(thumbnail, 700, 700, 'jpg')
        template.video_thumbnail1040 = resize_image(thumbnail, 1040, 1040, 'jpg')
        template.save()
        cap.release()

        if env('AWS_FLG') == 'True':
            os.remove(video_name)

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def delete(request):
    HeadTemplateRichVideo.objects.filter(display_id=request.POST.get('id')).all().delete()
    return JsonResponse( {}, safe=False )

def copy(request):
    return JsonResponse( {'copy_url': reverse('head:template:edit_richvideo') + '?copy=' + request.POST.get('id')}, safe=False )

def search(request):
    action_search(request, None, None)
    return JsonResponse( list(get_richvideo_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_richvideo_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    template = HeadTemplateRichVideo.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(HeadTemplateRichVideo)).first()
    template['video_display_time'] = time.strftime('%M:%S', time.gmtime(template['video_time']))
    return JsonResponse( template, safe=False )

def get_all(request):
    template_list = list(HeadTemplateRichVideo.objects.order_by('-created_at').values(*get_model_field(HeadTemplateRichVideo)).all())
    for template_index, template_item in enumerate(template_list):
        template_list[template_index]['video_display_time'] = time.strftime('%M:%S', time.gmtime(template_item['video_time']))
    return JsonResponse( template_list, safe=False )