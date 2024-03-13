from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.urls import reverse

from question.models import CompanyQuestion
from sign.models import AuthLogin
from template.models import (
    CompanyTemplateVideo, CompanyTemplateCardType, CompanyTemplateCardTypeAnnounce, CompanyTemplateCardTypeAnnounceText, CompanyTemplateCardTypeAnnounceAction,
    CompanyTemplateCardTypeLocation, CompanyTemplateCardTypePerson, CompanyTemplateCardTypeImage, CompanyTemplateCardTypeMore
)

from company.template.action.list import get_cardtype_list

from common import create_code, get_model_field
from table.action import action_search

import base64
import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    if request.POST.get('id') and CompanyTemplateCardType.objects.filter(display_id=request.POST.get('id')).exists():
        template = CompanyTemplateCardType.objects.filter(display_id=request.POST.get('id')).first()
        template.name = request.POST.get('name')
        template.title = request.POST.get('title')
        template.author = request.user.id
        template.save()
    else:
        template = CompanyTemplateCardType.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, CompanyTemplateCardType),
            company = auth_login.company,
            name = request.POST.get('name'),
            title = request.POST.get('title'),
            author = request.user.id,
        )
    
    CompanyTemplateCardTypeLocation.objects.filter(template=template).all().delete()
    CompanyTemplateCardTypePerson.objects.filter(template=template).all().delete()
    CompanyTemplateCardTypeImage.objects.filter(template=template).all().delete()
    for card_type in CompanyTemplateCardTypeAnnounce.objects.filter(template=template).all():
        CompanyTemplateCardTypeAnnounceText.objects.filter(card_type=card_type).all().delete()
        CompanyTemplateCardTypeAnnounceAction.objects.filter(card_type=card_type).all().delete()
    CompanyTemplateCardTypeAnnounce.objects.filter(template=template).all().delete()
    CompanyTemplateCardTypeMore.objects.filter(template=template).all().delete()

    if request.POST.get('type'):
        type = int(request.POST.get('type'))
        template.type = type
        template.count = int(request.POST.get('count'))
        template.save()
        if request.POST.get('template_10'):
            template.count = template.count + 1
            template.save()
        
        for i in range(int(request.POST.get('count'))):
            data = None
            data1 = None
            data2 = None
            data3 = None
            if type == 1 or type == 2:
                if request.POST.get('image_1_'+str(i+1)):
                    if ';base64,' in request.POST.get('image_1_'+str(i+1)):
                        format, imgstr = request.POST.get('image_1_'+str(i+1)).split(';base64,') 
                        ext = format.split('/')[-1] 
                        data1 = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                    else:
                        data1 = request.POST.get('image_1_'+str(i+1))
                if request.POST.get('image_2_'+str(i+1)):
                    if ';base64,' in request.POST.get('image_2_'+str(i+1)):
                        format, imgstr = request.POST.get('image_2_'+str(i+1)).split(';base64,') 
                        ext = format.split('/')[-1] 
                        data2 = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                    else:
                        data2 = request.POST.get('image_2_'+str(i+1))
                if request.POST.get('image_3_'+str(i+1)):
                    if ';base64,' in request.POST.get('image_3_'+str(i+1)):
                        format, imgstr = request.POST.get('image_3_'+str(i+1)).split(';base64,') 
                        ext = format.split('/')[-1] 
                        data3 = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                    else:
                        data3 = request.POST.get('image_3_'+str(i+1))
            elif type == 3 or type == 4:
                if request.POST.get('image_'+str(i+1)):
                    if ';base64,' in request.POST.get('image_'+str(i+1)):
                        format, imgstr = request.POST.get('image_'+str(i+1)).split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                    else:
                        data = request.POST.get('image_'+str(i+1))
            
            if type == 1:
                card_type = CompanyTemplateCardTypeAnnounce.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = (i+1),
                    title = request.POST.get('title_'+str(i+1)),
                    image_count = request.POST.get('image_count_'+str(i+1)),
                    image_1 = data1,
                    image_2 = data2,
                    image_3 = data3,
                    image_flg = request.POST.get('image_flg_'+str(i+1)),
                    label = request.POST.get('label_'+str(i+1)),
                    label_color = request.POST.get('label_color_'+str(i+1)),
                    label_flg = request.POST.get('label_flg_'+str(i+1)),
                    description = request.POST.get('description_'+str(i+1)),
                    description_flg = request.POST.get('description_flg_'+str(i+1)),
                )
                for j in range(int(request.POST.get('text_count_'+str(i+1)))):
                    text = request.POST.get('text_text_'+str(j+1)+'_'+str(i+1))
                    if request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'name':
                        text = '【応募者名】'
                    elif request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'line':
                        text = '【公式LINE名】'
                    elif request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'company':
                        text = '【企業名】'
                    elif request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'manager_name':
                        text = '【担当者名】'
                    elif request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'phone':
                        text = '【担当者電話番号】'
                    elif request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'date':
                        text = '【予約日時】'
                    elif request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'address':
                        text = '【会場住所】'
                    elif request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'url':
                        text = '【オンラインURL】'
                    CompanyTemplateCardTypeAnnounceText.objects.create(
                        id = str(uuid.uuid4()),
                        card_type = card_type,
                        number = (j+1),
                        title = request.POST.get('text_title_'+str(j+1)+'_'+str(i+1)),
                        text = text,
                        flg = request.POST.get('text_flg_'+str(j+1)+'_'+str(i+1)),
                    )
                for j in range(int(request.POST.get('action_count_'+str(i+1)))):
                    video = None
                    question = None
                    if request.POST.get('action_url_value_'+str(j+1)+'_'+str(i+1)):
                        video = CompanyTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_'+str(j+1)+'_'+str(i+1))).first()
                        question = CompanyQuestion.objects.filter(display_id=request.POST.get('action_url_value_'+str(j+1)+'_'+str(i+1))).first()
                    button_type = 0
                    if request.POST.get('action_button_type_'+str(j+1)+'_'+str(i+1)) == 'action':
                        button_type = 0
                    elif request.POST.get('action_button_type_'+str(j+1)+'_'+str(i+1)) == 'text':
                        button_type = 1
                    CompanyTemplateCardTypeAnnounceAction.objects.create(
                        id = str(uuid.uuid4()),
                        card_type = card_type,
                        number = (j+1),
                        label = request.POST.get('action_label_'+str(j+1)+'_'+str(i+1)),
                        type = request.POST.get('action_type_'+str(j+1)+'_'+str(i+1)),
                        url = request.POST.get('action_url_'+str(j+1)+'_'+str(i+1)),
                        text = request.POST.get('action_text_'+str(j+1)+'_'+str(i+1)),
                        video = video,
                        question = question,
                        button_type = button_type,
                        button_color = request.POST.get('action_text_color_'+str(j+1)+'_'+str(i+1)),
                        button_background_color = request.POST.get('action_background_color_'+str(j+1)+'_'+str(i+1)),
                        flg = request.POST.get('action_flg_'+str(j+1)+'_'+str(i+1)),
                    )
            elif type == 2:
                video_1 = None
                question_1 = None
                if request.POST.get('action_url_value_1_'+str(i+1)):
                    video_1 = CompanyTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_1_'+str(i+1))).first()
                    question_1 = CompanyQuestion.objects.filter(display_id=request.POST.get('action_url_value_1_'+str(i+1))).first()
                video_2 = None
                question_2 = None
                if request.POST.get('action_url_value_2_'+str(i+1)):
                    video_2 = CompanyTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_2_'+str(i+1))).first()
                    question_2 = CompanyQuestion.objects.filter(display_id=request.POST.get('action_url_value_2_'+str(i+1))).first()

                CompanyTemplateCardTypeLocation.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = (i+1),
                    title = request.POST.get('title_'+str(i+1)),
                    image_count = request.POST.get('image_count_'+str(i+1)),
                    image_1 = data1,
                    image_2 = data2,
                    image_3 = data3,
                    label = request.POST.get('label_'+str(i+1)),
                    label_color = request.POST.get('label_color_'+str(i+1)),
                    label_flg = request.POST.get('label_flg_'+str(i+1)),
                    place = request.POST.get('place_'+str(i+1)),
                    place_flg = request.POST.get('place_flg_'+str(i+1)),
                    plus = request.POST.get('plus_'+str(i+1)),
                    plus_type = request.POST.get('plus_type_'+str(i+1)),
                    plus_flg = request.POST.get('plus_flg_'+str(i+1)),
                    action_label_1 = request.POST.get('action_label_1_'+str(i+1)),
                    action_type_1 = request.POST.get('action_type_1_'+str(i+1)),
                    action_url_1 = request.POST.get('action_url_1_'+str(i+1)),
                    action_video_1 = video_1,
                    action_question_1 = question_1,
                    action_text_1 = request.POST.get('action_text_1_'+str(i+1)),
                    action_flg_1 = request.POST.get('action_label_flg_1_'+str(i+1)),
                    action_label_2 = request.POST.get('action_label_2_'+str(i+1)),
                    action_type_2 = request.POST.get('action_type_2_'+str(i+1)),
                    action_url_2 = request.POST.get('action_url_2_'+str(i+1)),
                    action_video_2 = video_2,
                    action_question_2 = question_2,
                    action_text_2 = request.POST.get('action_text_2_'+str(i+1)),
                    action_flg_2 = request.POST.get('action_label_flg_2_'+str(i+1)),
                )
            elif type == 3:
                video_1 = None
                question_1 = None
                if request.POST.get('action_url_value_1_'+str(i+1)):
                    video_1 = CompanyTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_1_'+str(i+1))).first()
                    question_1 = CompanyQuestion.objects.filter(display_id=request.POST.get('action_url_value_1_'+str(i+1))).first()
                video_2 = None
                question_2 = None
                if request.POST.get('action_url_value_2_'+str(i+1)):
                    video_2 = CompanyTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_2_'+str(i+1))).first()
                    question_2 = CompanyQuestion.objects.filter(display_id=request.POST.get('action_url_value_2_'+str(i+1))).first()

                CompanyTemplateCardTypePerson.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = (i+1),
                    image = data,
                    name = request.POST.get('name_'+str(i+1)),
                    tag_1 = request.POST.get('tag_1_'+str(i+1)),
                    tag_color_1 = request.POST.get('tag_color_1_'+str(i+1)),
                    tag_flg_1 = request.POST.get('tag_flg_1_'+str(i+1)),
                    tag_2 = request.POST.get('tag_2_'+str(i+1)),
                    tag_color_2 = request.POST.get('tag_color_2_'+str(i+1)),
                    tag_flg_2 = request.POST.get('tag_flg_2_'+str(i+1)),
                    tag_3 = request.POST.get('tag_3_'+str(i+1)),
                    tag_color_3 = request.POST.get('tag_color_3_'+str(i+1)),
                    tag_flg_3 = request.POST.get('tag_flg_3_'+str(i+1)),
                    description = request.POST.get('description_'+str(i+1)),
                    description_flg = request.POST.get('description_flg_'+str(i+1)),
                    action_label_1 = request.POST.get('action_label_1_'+str(i+1)),
                    action_type_1 = request.POST.get('action_type_1_'+str(i+1)),
                    action_url_1 = request.POST.get('action_url_1_'+str(i+1)),
                    action_video_1 = video_1,
                    action_question_1 = question_1,
                    action_text_1 = request.POST.get('action_text_1_'+str(i+1)),
                    action_flg_1 = request.POST.get('action_label_flg_1_'+str(i+1)),
                    action_label_2 = request.POST.get('action_label_2_'+str(i+1)),
                    action_type_2 = request.POST.get('action_type_2_'+str(i+1)),
                    action_url_2 = request.POST.get('action_url_2_'+str(i+1)),
                    action_video_2 = video_2,
                    action_question_2 = question_2,
                    action_text_2 = request.POST.get('action_text_2_'+str(i+1)),
                    action_flg_2 = request.POST.get('action_label_flg_2_'+str(i+1)),
                )
            elif type == 4:
                video = None
                question = None
                if request.POST.get('action_url_value_'+str(i+1)):
                    video = CompanyTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_'+str(i+1))).first()
                    question = CompanyQuestion.objects.filter(display_id=request.POST.get('action_url_value_'+str(i+1))).first()

                CompanyTemplateCardTypeImage.objects.create(
                    id = str(uuid.uuid4()),
                    template = template,
                    number = (i+1),
                    image = data,
                    label = request.POST.get('label_'+str(i+1)),
                    label_color = request.POST.get('label_color_'+str(i+1)),
                    label_flg = request.POST.get('label_flg_'+str(i+1)),
                    action_label = request.POST.get('action_label_'+str(i+1)),
                    action_type = request.POST.get('action_type_'+str(i+1)),
                    action_url = request.POST.get('action_url_'+str(i+1)),
                    action_video = video,
                    action_question = question,
                    action_text = request.POST.get('action_text_'+str(i+1)),
                    action_flg = request.POST.get('action_label_flg_'+str(i+1)),
                )
        
        if request.POST.get('template_10'):
            data = None
            if request.POST.get('image_10'):
                if ';base64,' in request.POST.get('image_10'):
                    format, imgstr = request.POST.get('image_10').split(';base64,') 
                    ext = format.split('/')[-1] 
                    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                else:
                    data = request.POST.get('image_10')
                    
            video = None
            question = None
            if request.POST.get('action_question_10'):
                video = CompanyTemplateVideo.objects.filter(display_id=request.POST.get('action_question_10')).first()
                question = CompanyQuestion.objects.filter(display_id=request.POST.get('action_question_10')).first()

            CompanyTemplateCardTypeMore.objects.create(
                id = str(uuid.uuid4()),
                template = template,
                type = request.POST.get('template_10'),
                image = data,
                action_label = request.POST.get('action_label_10'),
                action_type = request.POST.get('action_type_10'),
                action_url = request.POST.get('action_url_10'),
                action_video = video,
                action_question = question,
                action_text = request.POST.get('action_text_10'),
            )

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def delete(request):
    template = CompanyTemplateCardType.objects.filter(display_id=request.POST.get('id')).first()
    CompanyTemplateCardTypeLocation.objects.filter(template=template).all().delete()
    CompanyTemplateCardTypePerson.objects.filter(template=template).all().delete()
    CompanyTemplateCardTypeImage.objects.filter(template=template).all().delete()
    for card_type in CompanyTemplateCardTypeAnnounce.objects.filter(template=template).all():
        CompanyTemplateCardTypeAnnounceText.objects.filter(card_type=card_type).all().delete()
        CompanyTemplateCardTypeAnnounceAction.objects.filter(card_type=card_type).all().delete()
    CompanyTemplateCardTypeAnnounce.objects.filter(template=template).all().delete()
    CompanyTemplateCardTypeMore.objects.filter(template=template).all().delete()
    template.delete()
    return JsonResponse( {}, safe=False )

def copy(request):
    return JsonResponse( {'copy_url': reverse('company:template:edit_cardtype') + '?copy=' + request.POST.get('id')}, safe=False )

def search(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    action_search(request, None, auth_login.company)
    return JsonResponse( list(get_cardtype_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_cardtype_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    template = CompanyTemplateCardType.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(CompanyTemplateCardType)).first()
    if template['type'] == 1:
        template['item'] = list(CompanyTemplateCardTypeAnnounce.objects.filter(template_id=template['id']).values(*get_model_field(CompanyTemplateCardTypeAnnounce)).all())
        for template_index, template_item in enumerate(template['item']):
            template['item'][template_index]['text'] = list(CompanyTemplateCardTypeAnnounceText.objects.filter(card_type_id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypeAnnounceText)).all())
            template['item'][template_index]['action'] = list(CompanyTemplateCardTypeAnnounceAction.objects.filter(card_type_id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypeAnnounceAction)).all())
    elif template['type'] == 2:
        template['item'] = list(CompanyTemplateCardTypeLocation.objects.filter(template_id=template['id']).values(*get_model_field(CompanyTemplateCardTypeLocation)).all())
    elif template['type'] == 3:
        template['item'] = list(CompanyTemplateCardTypePerson.objects.filter(template_id=template['id']).values(*get_model_field(CompanyTemplateCardTypePerson)).all())
    elif template['type'] == 4:
        template['item'] = list(CompanyTemplateCardTypeImage.objects.filter(template_id=template['id']).values(*get_model_field(CompanyTemplateCardTypeImage)).all())
    template['more'] = CompanyTemplateCardTypeMore.objects.filter(template_id=template['id']).values(*get_model_field(CompanyTemplateCardTypeMore)).first()
    return JsonResponse( template, safe=False )

def get_all(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    template_list = list(CompanyTemplateCardType.objects.filter(company=auth_login.company).order_by('-created_at').values(*get_model_field(CompanyTemplateCardType)).all())
    for template_index, template_item in enumerate(template_list):
        if template_item['type'] == 1:
            template_list[template_index]['item'] = list(CompanyTemplateCardTypeAnnounce.objects.filter(template_id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypeAnnounce)).all())
            for card_type_index, card_type_item in enumerate(template_list[template_index]['item']):
                template_list[template_index]['item'][card_type_index]['text'] = list(CompanyTemplateCardTypeAnnounceText.objects.filter(card_type_id=card_type_item['id']).values(*get_model_field(CompanyTemplateCardTypeAnnounceText)).all())
                template_list[template_index]['item'][card_type_index]['action'] = list(CompanyTemplateCardTypeAnnounceAction.objects.filter(card_type_id=card_type_item['id']).values(*get_model_field(CompanyTemplateCardTypeAnnounceAction)).all())
        elif template_item['type'] == 2:
            template_list[template_index]['item'] = list(CompanyTemplateCardTypeLocation.objects.filter(template_id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypeLocation)).all())
        elif template_item['type'] == 3:
            template_list[template_index]['item'] = list(CompanyTemplateCardTypePerson.objects.filter(template_id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypePerson)).all())
        elif template_item['type'] == 4:
            template_list[template_index]['item'] = list(CompanyTemplateCardTypeImage.objects.filter(template_id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypeImage)).all())
        template_list[template_index]['more'] = CompanyTemplateCardTypeMore.objects.filter(template_id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypeMore)).first()
    return JsonResponse( template_list, safe=False )