from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.urls import reverse

from question.models import HeadQuestion
from template.models import HeadTemplateVideo, HeadTemplateRichMessage, HeadTemplateRichMessageItem

from head.template.action.list import get_richmessage_list

from common import create_code, resize_image, get_model_field
from table.action import action_search

import base64
import cv2
import environ
import os
import urllib.request as urllib_request
import uuid

env = environ.Env()
env.read_env('.env')

def save(request):
    if request.POST.get('id') and HeadTemplateRichMessage.objects.filter(display_id=request.POST.get('id')).exists():
        template = HeadTemplateRichMessage.objects.filter(display_id=request.POST.get('id')).first()
        template.name = request.POST.get('name')
        template.title = request.POST.get('title')
        template.author = request.user.id
        template.save()
    else:
        template = HeadTemplateRichMessage.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateRichMessage),
            name = request.POST.get('name'),
            title = request.POST.get('title'),
            author = request.user.id,
        )
    
    if ';base64,' in request.POST.get('image'):
        format, imgstr = request.POST.get('image').split(';base64,') 
        ext = format.split('/')[-1] 
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    else:
        data = request.POST.get('image')
    template.type = request.POST.get('template')
    template.image = data
    template.save()

    if env('AWS_FLG') == 'True':
        image_name = './static/' + str(uuid.uuid4()) + '.png'
        urllib_request.urlretrieve(template.image.url, image_name)
        image = cv2.imread(image_name)
    else:
        image = cv2.imread(template.image.url[1:])
    
    image_height, image_width = image.shape[:2]
    template.image_width = image_width
    template.image_height = image_height
    template.image240 = resize_image(image, 240, 240, 'png')
    template.image300 = resize_image(image, 300, 300, 'png')
    template.image460 = resize_image(image, 460, 460, 'png')
    template.image700 = resize_image(image, 700, 700, 'png')
    template.image1040 = resize_image(image, 1040, 1040, 'png')
    template.save()
    
    if env('AWS_FLG') == 'True':
        os.remove(image_name)
    
    HeadTemplateRichMessageItem.objects.filter(template=template).all().delete()
    number_list = ['a', 'b', 'c', 'd', 'e', 'f']
    for number_item in number_list:
        if request.POST.get('type_' + number_item):
            video = None
            if request.POST.get('video_' + number_item):
                video = HeadTemplateVideo.objects.filter(display_id=request.POST.get('video_' + number_item)).first()
            question = None
            if request.POST.get('question_' + number_item):
                question = HeadQuestion.objects.filter(display_id=request.POST.get('question_' + number_item)).first()

            HeadTemplateRichMessageItem.objects.create(
                id = str(uuid.uuid4()),
                template = template,
                number = number_item,
                type = request.POST.get('type_' + number_item),
                url = request.POST.get('url_' + number_item),
                video = video,
                question = question,
                label = request.POST.get('label_' + number_item),
            )

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def delete(request):
    template = HeadTemplateRichMessage.objects.filter(display_id=request.POST.get('id')).first()
    HeadTemplateRichMessageItem.objects.filter(template=template).all().delete()
    template.delete()
    return JsonResponse( {}, safe=False )

def copy(request):
    return JsonResponse( {'copy_url': reverse('head:template:edit_richmessage') + '?copy=' + request.POST.get('id')}, safe=False )

def search(request):
    action_search(request, None, None)
    return JsonResponse( list(get_richmessage_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_richmessage_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    template = HeadTemplateRichMessage.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(HeadTemplateRichMessage)).first()
    template['item'] = list(HeadTemplateRichMessageItem.objects.filter(template__id=template['id']).order_by('number').values(*get_model_field(HeadTemplateRichMessageItem)).all())
    return JsonResponse( template, safe=False )

def get_all(request):
    template_list = list(HeadTemplateRichMessage.objects.order_by('-created_at').values(*get_model_field(HeadTemplateRichMessage)).all())
    for template_index, template_item in enumerate(template_list):
        template_list[template_index]['item'] = list(HeadTemplateRichMessageItem.objects.filter(template__id=template_item['id']).order_by('number').values(*get_model_field(HeadTemplateRichMessageItem)).all())
    return JsonResponse( template_list, safe=False )