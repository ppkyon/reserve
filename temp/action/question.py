from django.http import JsonResponse

from question.models import ShopQuestionItem, ShopQuestionItemChoice, UserQuestion, UserQuestionItem, UserQuestionItemChoice

from common import get_model_field

def save(request):
    question = UserQuestion.objects.filter(display_id=request.POST.get('id')).first()
    question.memo = request.POST.get('memo')
    question.save()
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def get(request):
    question = UserQuestion.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(UserQuestion)).first()
    question['item'] = list(UserQuestionItem.objects.filter(user__id=question['id']).values(*get_model_field(UserQuestionItem)).all())
    for question_index, question_item in enumerate(question['item']):
        question['item'][question_index]['choice'] = list(UserQuestionItemChoice.objects.filter(user__id=question_item['id']).values(*get_model_field(UserQuestionItemChoice)).all())
        question['item'][question_index]['data'] = ShopQuestionItem.objects.filter(id=question_item['question']).values(*get_model_field(ShopQuestionItem)).first()
        for question_choice_index, question_choice_item in enumerate(question['item'][question_index]['choice']):
            question['item'][question_index]['choice'][question_choice_index]['data'] = ShopQuestionItemChoice.objects.filter(id=question_choice_item['question']).values(*get_model_field(ShopQuestionItemChoice)).first()
    return JsonResponse( question, safe=False )