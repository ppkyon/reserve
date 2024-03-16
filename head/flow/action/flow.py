from django.http import JsonResponse

from flow.models import (
    HeadFlow, HeadFlowTab, HeadFlowItem, HeadFlowTemplate, HeadFlowRichMenu,
    HeadFlowAction, HeadFlowActionReminder, HeadFlowActionMessage, HeadFlowStep, HeadFlowTimer
)
from richmenu.models import HeadRichMenu
from template.models import HeadTemplateText, HeadTemplateVideo, HeadTemplateRichMessage, HeadTemplateRichVideo, HeadTemplateCardType, HeadTemplateGreeting

from head.flow.action.list import get_list

from common import create_code, display_textarea_replace, get_model_field
from table.action import action_search

import re
import uuid

def save(request):
    valid = False
    if request.POST.get('valid') == '1':
        valid = True
    
    if request.POST.get('id') and HeadFlow.objects.filter(display_id=request.POST.get('id')).exists():
        flow = HeadFlow.objects.filter(display_id=request.POST.get('id')).first()
        flow.name = request.POST.get('name')
        flow.valid = valid
        flow.save()
    else:
        HeadFlow.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, HeadFlow),
            name = request.POST.get('name'),
            valid = valid,
            author = request.user.id,
        )

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def search(request):
    action_search(request, None, None)
    return JsonResponse( list(get_list(request, 1)), safe=False )

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('page')))), safe=False )

def valid(request):
    flow = HeadFlow.objects.filter(display_id=request.POST.get('id')).first()
    if flow.valid:
        flow.valid = False
    else:
        flow.valid = True
    flow.save()
    return JsonResponse( {'check': flow.valid}, safe=False )

def get(request):
    remove = re.compile(r"<[^>]*?>")
    flow = HeadFlow.objects.filter(display_id=request.POST.get('id')).values(*get_model_field(HeadFlow)).first()
    flow['tab'] = list(HeadFlowTab.objects.filter(flow__id=flow['id']).values(*get_model_field(HeadFlowTab)).order_by('number').all())
    for tab_index, tab_item in enumerate(flow['tab']):
        flow['tab'][tab_index]['item'] = list(HeadFlowItem.objects.filter(flow_tab__id=tab_item['id']).values(*get_model_field(HeadFlowItem)).order_by('x','y').all())
        for flow_index, flow_item in enumerate(flow['tab'][tab_index]['item']):
            if flow_item['type'] == 1:
                flow['tab'][tab_index]['item'][flow_index]['template'] = HeadTemplateGreeting.objects.filter(number=1).values(*get_model_field(HeadTemplateGreeting)).first()
                if flow['tab'][tab_index]['item'][flow_index]['template']['text']:
                    flow['tab'][tab_index]['item'][flow_index]['template']['text'] = remove.sub('', display_textarea_replace(flow['tab'][tab_index]['item'][flow_index]['template']['text']))
            elif flow_item['type'] == 2:
                print(flow_item)
            elif flow_item['type'] == 3:
                print(flow_item)
            elif flow_item['type'] == 4:
                print(flow_item)
            elif flow_item['type'] == 5:
                print(flow_item)
            elif flow_item['type'] == 6:
                template = HeadFlowTemplate.objects.filter(flow__id=flow_item['id']).values(*get_model_field(HeadFlowTemplate)).first()
                if template['template_cardtype']:
                    flow['tab'][tab_index]['item'][flow_index]['template'] = HeadTemplateCardType.objects.filter(id=template['template_cardtype']).values(*get_model_field(HeadTemplateCardType)).first()
            elif flow_item['type'] == 7:
                rich_menu = HeadFlowRichMenu.objects.filter(flow__id=flow_item['id']).values(*get_model_field(HeadFlowRichMenu)).first()
                if rich_menu['rich_menu']:
                    flow['tab'][tab_index]['item'][flow_index]['rich_menu'] = HeadRichMenu.objects.filter(id=rich_menu['rich_menu']).values(*get_model_field(HeadRichMenu)).first()
            elif flow_item['type'] == 8:
                flow['tab'][tab_index]['item'][flow_index]['action'] = HeadFlowAction.objects.filter(flow__id=flow_item['id']).values(*get_model_field(HeadFlowAction)).first()
                flow['tab'][tab_index]['item'][flow_index]['action']['action'] = HeadFlowTab.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['action']['action']).values(*get_model_field(HeadFlowTab)).first()
                flow['tab'][tab_index]['item'][flow_index]['reminder'] = HeadFlowActionReminder.objects.filter(flow__id=flow_item['id']).values(*get_model_field(HeadFlowActionReminder)).first()
                if flow['tab'][tab_index]['item'][flow_index]['reminder']['template_text']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_text'] = HeadTemplateText.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_text']).values(*get_model_field(HeadTemplateText)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['reminder']['template_video']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_video'] = HeadTemplateVideo.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_video']).values(*get_model_field(HeadTemplateVideo)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richmessage']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richmessage'] = HeadTemplateRichMessage.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richmessage']).values(*get_model_field(HeadTemplateRichMessage)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richvideo']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richvideo'] = HeadTemplateRichVideo.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_richvideo']).values(*get_model_field(HeadTemplateRichVideo)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['reminder']['template_cardtype']:
                    flow['tab'][tab_index]['item'][flow_index]['reminder']['template_cardtype'] = HeadTemplateCardType.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['reminder']['template_cardtype']).values(*get_model_field(HeadTemplateCardType)).first()
                flow['tab'][tab_index]['item'][flow_index]['message'] = HeadFlowActionMessage.objects.filter(flow__id=flow_item['id']).values(*get_model_field(HeadFlowActionMessage)).first()
                if flow['tab'][tab_index]['item'][flow_index]['message']['template_text']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_text'] = HeadTemplateText.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_text']).values(*get_model_field(HeadTemplateText)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['message']['template_video']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_video'] = HeadTemplateVideo.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_video']).values(*get_model_field(HeadTemplateVideo)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['message']['template_richmessage']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_richmessage'] = HeadTemplateRichMessage.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_richmessage']).values(*get_model_field(HeadTemplateRichMessage)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['message']['template_richvideo']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_richvideo'] = HeadTemplateRichVideo.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_richvideo']).values(*get_model_field(HeadTemplateRichVideo)).first()
                elif flow['tab'][tab_index]['item'][flow_index]['message']['template_cardtype']:
                    flow['tab'][tab_index]['item'][flow_index]['message']['template_cardtype'] = HeadTemplateCardType.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['message']['template_cardtype']).values(*get_model_field(HeadTemplateCardType)).first()
            elif flow_item['type'] == 9:
                flow['tab'][tab_index]['item'][flow_index]['step'] = HeadFlowStep.objects.filter(flow__id=flow_item['id']).values(*get_model_field(HeadFlowStep)).first()
                flow['tab'][tab_index]['item'][flow_index]['step']['tab'] = HeadFlowTab.objects.filter(id=flow['tab'][tab_index]['item'][flow_index]['step']['tab']).values(*get_model_field(HeadFlowTab)).first()
            elif flow_item['type'] == 52:
                flow['tab'][tab_index]['item'][flow_index]['timer'] = HeadFlowTimer.objects.filter(flow__id=flow_item['id']).values(*get_model_field(HeadFlowTimer)).first()
    return JsonResponse( flow, safe=False )