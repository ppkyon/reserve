from django.http import JsonResponse

from flow.models import HeadFlow

from head.flow.action.list import get_list

from common import create_code
from table.action import action_search

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