from django.http import JsonResponse

from flow.models import ShopFlowItem, ShopFlowTemplate, UserFlow, UserFlowSchedule

from line.action.message import push_card_type_message

import datetime

def send(request):
    user_flow = UserFlow.objects.filter(display_id=request.POST.get('flow_id')).first()
    user_flow_schedule = UserFlowSchedule.objects.filter(display_id=request.POST.get('schedule_id')).first()
    if user_flow_schedule:
        user_flow_schedule.date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day')
        user_flow_schedule.time = request.POST.get('hour') + ':' + request.POST.get('minute')
        user_flow_schedule.updated_at = datetime.datetime.now()
        user_flow_schedule.save()

    flow_flg = False
    for flow_item in ShopFlowItem.objects.filter(flow_tab=user_flow.flow_tab).order_by('y', 'x').all():
        if flow_flg:
            if flow_item.type == 6:
                flow_template = ShopFlowTemplate.objects.filter(flow=flow_item).first()
                push_card_type_message(user_flow.user, flow_template.template_cardtype, None)
            if flow_item.type == 51:
                break
        if flow_item.type == 54:
            flow_flg = True
    return JsonResponse( {}, safe=False )