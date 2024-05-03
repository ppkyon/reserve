from django.http import JsonResponse

from linebot import LineBotApi

from flow.models import UserFlow, UserFlowSchedule
from reserve.models import ReserveOfflineFacility, ReserveOnlineFacility
from sign.models import AuthLogin, ShopLine, AuthUser
from user.models import LineUser, UserAlert

from common import create_code

import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('user_id')).first()

    global line_bot_api
    shop_line = ShopLine.objects.filter(shop=auth_login.shop).first()
    line_bot_api = LineBotApi(shop_line.channel_access_token)

    for user_flow in UserFlow.objects.filter(user=user).order_by('number').all():
        if not user_flow.end_flg:
            for user_flow_schedule in UserFlowSchedule.objects.filter(flow=user_flow, join=0).order_by('number').all():
                if request.POST.get('date_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    date = request.POST.get('date_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)).split(' ')
                    user_flow_schedule.date = date[0].strip().replace('/','-')
                    user_flow_schedule.time = date[1].strip()
                join = 0
                if request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    join = int(request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)))
                if request.POST.get('manager_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    user_flow_schedule.manager = AuthUser.objects.filter(display_id=request.POST.get('manager_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number))).first()
                if request.POST.get('facility_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    if user_flow_schedule.offline:
                        user_flow_schedule.offline_facility = ReserveOfflineFacility.objects.filter(display_id=request.POST.get('facility_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number))).first()
                    elif user_flow_schedule.online:
                        user_flow_schedule.online_facility = ReserveOnlineFacility.objects.filter(display_id=request.POST.get('facility_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number))).first()
                if user_flow_schedule.join == 0:
                    user_flow_schedule.join = join
                user_flow_schedule.save()

                if join == 1:
                    user_flow.end_flg = True
                    user_flow.save()
                    UserAlert.objects.filter(user=user, number=user_flow.number).all().delete()
                elif join == 2:
                    if user_flow_schedule.offline:
                        UserFlowSchedule.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, UserFlow),
                            flow = user_flow,
                            number = UserFlowSchedule.objects.filter(flow=user_flow).count() + 1,
                            date = None,
                            time = None,
                            join = 0,
                            offline =user_flow_schedule.offline,
                            offline_course = None,
                            offline_facility = None,
                            manager = None,
                            question = None,
                        )
                    elif user_flow_schedule.online:
                        UserFlowSchedule.objects.create(
                            id = str(uuid.uuid4()),
                            display_id = create_code(12, UserFlow),
                            flow = user_flow,
                            number = UserFlowSchedule.objects.filter(flow=user_flow).count() + 1,
                            date = None,
                            time = None,
                            join = 0,
                            online = user_flow_schedule.online,
                            online_course = None,
                            online_facility = None,
                            manager = None,
                            question = None,
                        )
                    UserAlert.objects.filter(user=user, number=user_flow.number).all().delete()
                    
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )