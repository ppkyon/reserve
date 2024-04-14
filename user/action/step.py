from django.http import JsonResponse

from flow.models import ShopFlowItem, UserFlow, UserFlowSchedule
from sign.models import AuthLogin
from user.models import LineUser

from flow.action.go import go

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('user_id')).first()

    for user_flow in UserFlow.objects.filter(user=user).order_by('number').all():
        if not user_flow.end_flg:
            for user_flow_schedule in UserFlowSchedule.objects.filter(flow=user_flow).order_by('number').all():
                join = 0
                if request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)):
                    join = int(request.POST.get('join_'+str(user_flow.display_id)+'_'+str(user_flow_schedule.number)))
                user_flow_schedule.join = join
                user_flow_schedule.save()

                if join == 1:
                    flow_flg = False
                    for flow_item in ShopFlowItem.objects.filter(flow_tab=user_flow.flow_tab).all():
                        if flow_flg:
                            if go(user, user_flow.flow, user_flow.flow_tab, flow_item):
                                user_flow.end_flg = True
                                user_flow.save()
                                break
                        if flow_item.type == 8:
                            flow_flg = True
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )