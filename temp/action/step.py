from django.http import JsonResponse

from linebot import LineBotApi

from flow.models import UserFlow, UserFlowSchedule
from sign.models import AuthLogin, ShopLine
from user.models import LineUser

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('user_id')).first()

    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=auth_login.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)

    for user_flow in UserFlow.objects.filter(user=user).order_by('number').all():
        if not user_flow.end_flg:
            for user_flow_schedule in UserFlowSchedule.objects.filter(flow=user_flow).order_by('number').all():
                join = 0
                if request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    join = int(request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)))
                user_flow_schedule.join = join
                user_flow_schedule.save()

                if join == 1:
                    user_flow.end_flg = True
                    user_flow.save()
                    
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )