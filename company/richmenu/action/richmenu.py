from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.urls import reverse

from question.models import CompanyQuestion
from richmenu.models import CompanyRichMenu, CompanyRichMenuItem
from sign.models import AuthLogin
from template.models import CompanyTemplateVideo

from company.richmenu.action.list import get_list

from common import create_code, get_model_field
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
    menu_flg = False
    if request.POST.get('menu_flg') == '1':
        menu_flg = True
    
    if ';base64,' in request.POST.get('image'):
        format, imgstr = request.POST.get('image').split(';base64,') 
        ext = format.split('/')[-1] 
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    else:
        data = request.POST.get('image')
    
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    if request.POST.get('id') and CompanyRichMenu.objects.filter(display_id=request.POST.get('id')).exists():
        rich_menu = CompanyRichMenu.objects.filter(display_id=request.POST.get('id')).first()
        rich_menu.name = request.POST.get('name')
        rich_menu.menu_type = request.POST.get('menu_type')
        rich_menu.menu_flg = menu_flg
        rich_menu.menu_text = request.POST.get('menu_text')
        rich_menu.type = request.POST.get('template')
        rich_menu.image = data
        rich_menu.author = request.user.id
        rich_menu.save()
    else:
        rich_menu = CompanyRichMenu.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, CompanyRichMenu),
            company = auth_login.company,
            name = request.POST.get('name'),
            menu_type = request.POST.get('menu_type'),
            menu_flg = menu_flg,
            menu_text = request.POST.get('menu_text'),
            type = request.POST.get('template'),
            image = data,
            author = request.user.id,
        )
    
    if env('AWS_FLG') == 'True':
        image_name = './static/' + str(uuid.uuid4()) + '.png'
        urllib_request.urlretrieve(rich_menu.image.url, image_name)
        image = cv2.imread(image_name)
    else:
        image = cv2.imread(rich_menu.image.url[1:])
    image_height, image_width = image.shape[:2]

    rich_menu.image_width = image_width
    rich_menu.image_height = image_height
    rich_menu.save()

    if env('AWS_FLG') == 'True':
        os.remove(image_name)
    
    CompanyRichMenuItem.objects.filter(rich_menu=rich_menu).all().delete()
    number_list = ['a', 'b', 'c', 'd', 'e', 'f']
    for number_item in number_list:
        video = None
        if request.POST.get('video_' + number_item):
            video = CompanyTemplateVideo.objects.filter(display_id=request.POST.get('video_' + number_item)).first()
        question = None
        if request.POST.get('question_' + number_item):
            question = CompanyQuestion.objects.filter(display_id=request.POST.get('question_' + number_item)).first()

        if request.POST.get('type_' + number_item):
            CompanyRichMenuItem.objects.create(
                id = str(uuid.uuid4()),
                rich_menu = rich_menu,
                number = number_item,
                type = request.POST.get('type_' + number_item),
                url = request.POST.get('url_' + number_item),
                video = video,
                question = question,
                label = request.POST.get('label_' + number_item),
                text = request.POST.get('text_' + number_item),
            )

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def copy(request):
    return JsonResponse( {'copy_url': reverse('company:richmenu:edit') + '?copy=' + request.POST.get('id')}, safe=False )

def delete(request):
    rich_menu = CompanyRichMenu.objects.filter(display_id=request.POST.get('id')).first()
    CompanyRichMenuItem.objects.filter(rich_menu=rich_menu).all().delete()
    rich_menu.delete()
    return JsonResponse( {}, safe=False )

def search(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    action_search(request, None, auth_login.company)
    return JsonResponse( list(get_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    rich_menu = CompanyRichMenu.objects.filter(display_id=request.POST.get("id")).values(*get_model_field(CompanyRichMenu)).first()
    return JsonResponse( rich_menu, safe=False )

def get_all(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    rich_menu_list = list(CompanyRichMenu.objects.filter(company=auth_login.company).order_by('-created_at').values(*get_model_field(CompanyRichMenu)).all())
    for rich_menu_index, rich_menu_item in enumerate(rich_menu_list):
        rich_menu_list[rich_menu_index]['item'] = list(CompanyRichMenuItem.objects.filter(rich_menu__id=rich_menu_item['id']).order_by('number').values(*get_model_field(CompanyRichMenuItem)).all())
    return JsonResponse( rich_menu_list, safe=False )