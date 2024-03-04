from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.urls import reverse

from question.models import HeadQuestion
from template.models import (
    HeadTemplateVideo, HeadTemplateCardType, HeadTemplateCardTypeAnnounce, HeadTemplateCardTypeAnnounceText, HeadTemplateCardTypeAnnounceAction,
    HeadTemplateCardTypeLocation, HeadTemplateCardTypePerson, HeadTemplateCardTypeImage, HeadTemplateCardTypeMore
)

from head.template.action.list import get_cardtype_list

from common import create_code, get_model_field
from table.action import action_search

import base64
import uuid

def save(request):
    if request.POST.get('id') and HeadTemplateCardType.objects.filter(display_id=request.POST.get('id')).exists():
        template = HeadTemplateCardType.objects.filter(display_id=request.POST.get('id')).first()
        template.name = request.POST.get('name')
        template.title = request.POST.get('title')
        template.author = request.user.id
        template.save()
    else:
        template = HeadTemplateCardType.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadTemplateCardType),
            name = request.POST.get('name'),
            title = request.POST.get('title'),
            author = request.user.id,
        )
    
    HeadTemplateCardTypeLocation.objects.filter(template=template).all().delete()
    HeadTemplateCardTypePerson.objects.filter(template=template).all().delete()
    HeadTemplateCardTypeImage.objects.filter(template=template).all().delete()
    for card_type in HeadTemplateCardTypeAnnounce.objects.filter(template=template).all():
        HeadTemplateCardTypeAnnounceText.objects.filter(card_type=card_type).all().delete()
        HeadTemplateCardTypeAnnounceAction.objects.filter(card_type=card_type).all().delete()
    HeadTemplateCardTypeAnnounce.objects.filter(template=template).all().delete()
    HeadTemplateCardTypeMore.objects.filter(template=template).all().delete()

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
                card_type = HeadTemplateCardTypeAnnounce.objects.create(
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
                        text = '【面接日時】'
                    elif request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'address':
                        text = '【会場住所】'
                    elif request.POST.get('text_value_'+str(j+1)+'_'+str(i+1)) == 'url':
                        text = '【オンラインURL】'
                    HeadTemplateCardTypeAnnounceText.objects.create(
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
                        video = HeadTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_'+str(j+1)+'_'+str(i+1))).first()
                        question = HeadQuestion.objects.filter(display_id=request.POST.get('action_url_value_'+str(j+1)+'_'+str(i+1))).first()
                    button_type = 0
                    if request.POST.get('action_button_type_'+str(j+1)+'_'+str(i+1)) == 'action':
                        button_type = 0
                    elif request.POST.get('action_button_type_'+str(j+1)+'_'+str(i+1)) == 'text':
                        button_type = 1
                    HeadTemplateCardTypeAnnounceAction.objects.create(
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
                    video_1 = HeadTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_1_'+str(i+1))).first()
                    question_1 = HeadQuestion.objects.filter(display_id=request.POST.get('action_url_value_1_'+str(i+1))).first()
                video_2 = None
                question_2 = None
                if request.POST.get('action_url_value_2_'+str(i+1)):
                    video_2 = HeadTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_2_'+str(i+1))).first()
                    question_2 = HeadQuestion.objects.filter(display_id=request.POST.get('action_url_value_2_'+str(i+1))).first()

                HeadTemplateCardTypeLocation.objects.create(
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
                    video_1 = HeadTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_1_'+str(i+1))).first()
                    question_1 = HeadQuestion.objects.filter(display_id=request.POST.get('action_url_value_1_'+str(i+1))).first()
                video_2 = None
                question_2 = None
                if request.POST.get('action_url_value_2_'+str(i+1)):
                    video_2 = HeadTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_2_'+str(i+1))).first()
                    question_2 = HeadQuestion.objects.filter(display_id=request.POST.get('action_url_value_2_'+str(i+1))).first()

                HeadTemplateCardTypePerson.objects.create(
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
                    video = HeadTemplateVideo.objects.filter(display_id=request.POST.get('action_url_value_'+str(i+1))).first()
                    question = HeadQuestion.objects.filter(display_id=request.POST.get('action_url_value_'+str(i+1))).first()

                HeadTemplateCardTypeImage.objects.create(
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
                video = HeadTemplateVideo.objects.filter(display_id=request.POST.get('action_question_10')).first()
                question = HeadQuestion.objects.filter(display_id=request.POST.get('action_question_10')).first()

            HeadTemplateCardTypeMore.objects.create(
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
    template = HeadTemplateCardType.objects.filter(display_id=request.POST.get('id')).first()
    HeadTemplateCardTypeLocation.objects.filter(template=template).all().delete()
    HeadTemplateCardTypePerson.objects.filter(template=template).all().delete()
    HeadTemplateCardTypeImage.objects.filter(template=template).all().delete()
    for card_type in HeadTemplateCardTypeAnnounce.objects.filter(template=template).all():
        HeadTemplateCardTypeAnnounceText.objects.filter(card_type=card_type).all().delete()
        HeadTemplateCardTypeAnnounceAction.objects.filter(card_type=card_type).all().delete()
    HeadTemplateCardTypeAnnounce.objects.filter(template=template).all().delete()
    HeadTemplateCardTypeMore.objects.filter(template=template).all().delete()
    template.delete()
    return JsonResponse( {}, safe=False )

def copy(request):
    return JsonResponse( {'copy_url': reverse('head:template:edit_cardtype') + '?copy=' + request.POST.get('id')}, safe=False )

def search(request):
    action_search(request, None, None)
    return JsonResponse( list(get_cardtype_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_cardtype_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    template = HeadTemplateCardType.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(HeadTemplateCardType)).first()
    if template['type'] == 1:
        template['item'] = list(HeadTemplateCardTypeAnnounce.objects.filter(template_id=template['id']).values(*get_model_field(HeadTemplateCardTypeAnnounce)).all())
        for template_index, template_item in enumerate(template['item']):
            template['item'][template_index]['text'] = list(HeadTemplateCardTypeAnnounceText.objects.filter(card_type_id=template_item['id']).values(*get_model_field(HeadTemplateCardTypeAnnounceText)).all())
            template['item'][template_index]['action'] = list(HeadTemplateCardTypeAnnounceAction.objects.filter(card_type_id=template_item['id']).values(*get_model_field(HeadTemplateCardTypeAnnounceAction)).all())
    elif template['type'] == 2:
        template['item'] = list(HeadTemplateCardTypeLocation.objects.filter(template_id=template['id']).values(*get_model_field(HeadTemplateCardTypeLocation)).all())
    elif template['type'] == 3:
        template['item'] = list(HeadTemplateCardTypePerson.objects.filter(template_id=template['id']).values(*get_model_field(HeadTemplateCardTypePerson)).all())
    elif template['type'] == 4:
        template['item'] = list(HeadTemplateCardTypeImage.objects.filter(template_id=template['id']).values(*get_model_field(HeadTemplateCardTypeImage)).all())
    template['more'] = HeadTemplateCardTypeMore.objects.filter(template_id=template['id']).values(*get_model_field(HeadTemplateCardTypeMore)).first()
    return JsonResponse( template, safe=False )