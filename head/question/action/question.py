from django.http import JsonResponse
from django.urls import reverse

from question.models import HeadQuestion, HeadQuestionItem, HeadQuestionItemChoice

from head.question.action.list import get_list

from common import create_code
from table.action import action_search

import datetime
import uuid

def save(request):
    if request.POST.get('id') and HeadQuestion.objects.filter(display_id=request.POST.get('id')).exists():
        question = HeadQuestion.objects.filter(display_id=request.POST.get('id')).first()
        question.title = request.POST.get('title')
        question.name = request.POST.get('name')
        question.description = request.POST.get('description')
        question.color = request.POST.get('color')
        question.count = request.POST.get('count')
        question.author = request.user.id
        question.save()
    else:
        question = HeadQuestion.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadQuestion),
            title = request.POST.get('title'),
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            color = request.POST.get('color'),
            count = request.POST.get('count'),
            author = request.user.id,
        )
    
    for question_item in HeadQuestionItem.objects.filter(question=question).all():
        HeadQuestionItemChoice.objects.filter(question_item=question_item).all().delete()
    HeadQuestionItem.objects.filter(question=question).all().delete()

    for i in range(int(request.POST.get('count'))):
        required_flg = False
        if request.POST.get('required_'+str(i+1)) == '1':
            required_flg = True
        
        question_item = HeadQuestionItem.objects.create(
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
            HeadQuestionItemChoice.objects.create(
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
    return JsonResponse( {'copy_url': reverse('head:question:edit') + '?copy=' + request.POST.get('id')}, safe=False )

def delete(request):
    question = HeadQuestion.objects.filter(display_id=request.POST.get('id')).first()
    for question_item in HeadQuestionItem.objects.filter(question=question).all():
        HeadQuestionItemChoice.objects.filter(question_item=question_item).all().delete()
    HeadQuestionItem.objects.filter(question=question).all().delete()
    HeadQuestion.objects.filter(display_id=request.POST.get('id')).all().delete()
    return JsonResponse( {}, safe=False )

def search(request):
    action_search(request, None, None)
    return JsonResponse( list(get_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('page')))), safe=False )