from django.http import JsonResponse
from django.urls import reverse

from question.models import ShopQuestion, ShopQuestionItem, ShopQuestionItemChoice
from sign.models import AuthLogin

from question.action.list import get_list

from common import create_code, get_model_field
from table.action import action_search

import datetime
import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    favorite_flg = False
    if request.POST.get('favorite') == '1':
        favorite_flg = True

    if request.POST.get('id') and ShopQuestion.objects.filter(display_id=request.POST.get('id')).exists():
        question = ShopQuestion.objects.filter(display_id=request.POST.get('id')).first()
        question.title = request.POST.get('title')
        question.name = request.POST.get('name')
        question.description = request.POST.get('description')
        question.color = request.POST.get('color')
        question.favorite_flg = favorite_flg
        question.count = request.POST.get('count')
        question.author = request.user.id
        question.save()
    else:
        question = ShopQuestion.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, ShopQuestion),
            shop = auth_login.shop,
            title = request.POST.get('title'),
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            color = request.POST.get('color'),
            favorite_flg = favorite_flg,
            count = request.POST.get('count'),
            author = request.user.id,
        )
    
    for question_item in ShopQuestionItem.objects.filter(question=question).all():
        ShopQuestionItemChoice.objects.filter(question_item=question_item).all().delete()
    ShopQuestionItem.objects.filter(question=question).all().delete()

    for i in range(int(request.POST.get('count'))):
        required_flg = False
        if request.POST.get('required_'+str(i+1)) == '1':
            required_flg = True
        
        question_item = ShopQuestionItem.objects.create(
            id = str(uuid.uuid4()),
            question = question,
            number = (i+1),
            type = request.POST.get('type_'+str(i+1)),
            title = request.POST.get('title_'+str(i+1)),
            description = request.POST.get('description_'+str(i+1)),
            choice_type = request.POST.get('choice_type_'+str(i+1)),
            choice_count = request.POST.get('choice_count_'+str(i+1)),
            required_flg = required_flg,
        )

        for j in range(int(request.POST.get('choice_count_'+str(i+1)))):
            ShopQuestionItemChoice.objects.create(
                id = str(uuid.uuid4()),
                question_item = question_item,
                number = (j+1),
                text = request.POST.get('choice_text_'+str(i+1)+'_'+str(j+1)),
                updated_at = datetime.datetime.now()
            )
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def copy(request):
    return JsonResponse( {'copy_url': reverse('question:edit') + '?copy=' + request.POST.get('id')}, safe=False )

def delete(request):
    question = ShopQuestion.objects.filter(display_id=request.POST.get('id')).first()
    for question_item in ShopQuestionItem.objects.filter(question=question).all():
        ShopQuestionItemChoice.objects.filter(question_item=question_item).all().delete()
    ShopQuestionItem.objects.filter(question=question).all().delete()
    ShopQuestion.objects.filter(display_id=request.POST.get('id')).all().delete()
    return JsonResponse( {}, safe=False )

def favorite(request):
    question = ShopQuestion.objects.filter(display_id=request.POST.get('id')).first()
    if question.favorite_flg:
        question.favorite_flg = False
    else:
        question.favorite_flg = True
    question.save()
    return JsonResponse( {'check': question.favorite_flg}, safe=False )

def search(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    action_search(request, auth_login.shop, auth_login.company)
    return JsonResponse( list(get_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('page')))), safe=False )

def get(request):
    question = ShopQuestion.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(ShopQuestion)).first()
    question['item'] = list(ShopQuestionItem.objects.filter(question__id=question['id']).values(*get_model_field(ShopQuestionItem)).all())
    for question_index, question_item in enumerate(question['item']):
        question['item'][question_index]['choice'] = list(ShopQuestionItemChoice.objects.filter(question_item__id=question_item['id']).values(*get_model_field(ShopQuestionItemChoice)).all())
    return JsonResponse( question, safe=False )

def get_all(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    question_list = list(ShopQuestion.objects.filter(shop=auth_login.shop).values(*get_model_field(ShopQuestion)).all())
    for question_index, question_item in enumerate(question_list):
        question_list[question_index]['item'] = list(ShopQuestionItem.objects.filter(question__id=question_item['id']).values(*get_model_field(ShopQuestionItem)).all())
    return JsonResponse( question_list, safe=False )