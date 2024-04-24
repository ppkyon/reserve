from django.http import JsonResponse

from flow.models import UserFlow, UserFlowSchedule
from question.models import UserQuestion, UserQuestionItem, UserQuestionItemChoice
from reserve.models import ReserveOnlineSetting, ReserveOfflineSetting, ReserveOnlineCourse, ReserveOfflineCourse, ReserveOnlineFacility, ReserveOfflineFacility
from setting.models import ShopOnline, ShopOffline
from sign.models import AuthShop
from user.models import LineUser, UserProfile

from common import get_model_field

import datetime

def check(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).values(*get_model_field(LineUser)).first()
    user['profile'] = UserProfile.objects.filter(user__id=user['id']).values(*get_model_field(UserProfile)).first()

    user_flow = list(UserFlow.objects.filter(user__id=user['id']).order_by('-number').values(*get_model_field(UserFlow)).all())
    for user_flow_index, user_flow_item in enumerate(user_flow):
        user_flow[user_flow_index]['schedule'] = UserFlowSchedule.objects.filter(flow__id=user_flow_item['id'], cancel_flg=False).order_by('-number').values(*get_model_field(UserFlowSchedule)).first()
        if user_flow[user_flow_index]['schedule']:
            date = datetime.datetime(user_flow[user_flow_index]['schedule']['date'].year, user_flow[user_flow_index]['schedule']['date'].month, user_flow[user_flow_index]['schedule']['date'].day, user_flow[user_flow_index]['schedule']['time'].hour, user_flow[user_flow_index]['schedule']['time'].minute, 0)
            if user_flow[user_flow_index]['schedule']['online']:
                user_flow[user_flow_index]['setting'] = ReserveOnlineSetting.objects.filter(id=user_flow[user_flow_index]['schedule']['online']).values(*get_model_field(ReserveOnlineSetting)).first()
                add_date = date + datetime.timedelta(minutes=user_flow[user_flow_index]['setting']['time'])
                user_flow[user_flow_index]['place'] = ShopOnline.objects.filter(id=user_flow[user_flow_index]['setting']['online']).values(*get_model_field(ShopOnline)).first()
                if user_flow[user_flow_index]['schedule']['online_course']:
                    user_flow[user_flow_index]['course'] = ReserveOnlineCourse.objects.filter(id=user_flow[user_flow_index]['schedule']['online_course']).values(*get_model_field(ReserveOnlineCourse)).first()
            elif user_flow[user_flow_index]['schedule']['offline']:
                user_flow[user_flow_index]['setting'] = ReserveOfflineSetting.objects.filter(id=user_flow[user_flow_index]['schedule']['offline']).values(*get_model_field(ReserveOfflineSetting)).first()
                add_date = date + datetime.timedelta(minutes=user_flow[user_flow_index]['setting']['time'])
                user_flow[user_flow_index]['place'] = ShopOffline.objects.filter(id=user_flow[user_flow_index]['setting']['offline']).values(*get_model_field(ShopOffline)).first()
                if user_flow[user_flow_index]['schedule']['offline_course']:
                    user_flow[user_flow_index]['course'] = ReserveOfflineCourse.objects.filter(id=user_flow[user_flow_index]['schedule']['offline_course']).values(*get_model_field(ReserveOfflineCourse)).first()
            user_flow[user_flow_index]['reserve'] = str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日 ' + str(date.hour) + '時' + str(date.minute).zfill(2) + '分 ～ ' + str(add_date.hour) + '時' + str(add_date.minute).zfill(2) + '分'

    user_question = list(UserQuestion.objects.filter(user__id=user['id']).order_by('created_at').values(*get_model_field(UserQuestion)).all())
    for user_question_index, user_question_item in enumerate(user_question):
        user_question[user_question_index]['item'] = list(UserQuestionItem.objects.filter(question__id=user_question_item['id']).order_by('created_at').values(*get_model_field(UserQuestionItem)).all())
        for user_question_item_index, user_question_item_item in enumerate(user_question[user_question_index]['item']):
            user_question[user_question_index]['item'][user_question_item_index]['choice'] = list(UserQuestionItemChoice.objects.filter(question__id=user_question_item_item['id']).values(*get_model_field(UserQuestionItemChoice)).all())

    data = {
        'user': user,
        'history': user_flow,
        'question': user_question,
    }
    return JsonResponse( data, safe=False )