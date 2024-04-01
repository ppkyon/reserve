from django.http import JsonResponse

from reserve.models import ReserveOfflineFacility, ReserveOnlineFacility
from setting.models import ShopOffline, ShopOnline

from common import create_code

import uuid

def save(request):
    random_list = list()
    for i in range(int(request.POST.get('count'))):
        random_list.append(request.POST.get('random_'+str( i + 1 )))

    ReserveOfflineFacility.objects.filter(offline=ShopOffline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all().delete()
    ReserveOnlineFacility.objects.filter(online=ShopOnline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all().delete()

    for i in range(int(request.POST.get('count'))):
        if ReserveOfflineFacility.objects.filter(display_id=request.POST.get('random_'+str(i+1))).exists():
            offline = ReserveOfflineFacility.objects.filter(display_id=request.POST.get('random_'+str(i+1))).first()
            offline.number = ( i + 1 )
            offline.name = request.POST.get('name_'+str( i + 1 ))
            offline.count = request.POST.get('count_'+str( i + 1 ))
            offline.order = request.POST.get('order_'+str( i + 1 ))
            offline.save()
        elif ReserveOnlineFacility.objects.filter(display_id=request.POST.get('random_'+str(i+1))).exists():
            online = ReserveOnlineFacility.objects.filter(display_id=request.POST.get('random_'+str(i+1))).first()
            online.number = ( i + 1 )
            online.name = request.POST.get('name_'+str( i + 1 ))
            online.count = request.POST.get('count_'+str( i + 1 ))
            online.order = request.POST.get('order_'+str( i + 1 ))
            online.save()
        else:
            if ShopOffline.objects.filter(display_id=request.POST.get('id')).exists():
                ReserveOfflineFacility.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOfflineFacility),
                    offline = ShopOffline.objects.filter(display_id=request.POST.get('id')).first(),
                    number = ( i + 1 ),
                    name = request.POST.get('name_'+str( i + 1 )),
                    count = request.POST.get('count_'+str( i + 1 )),
                    order = request.POST.get('order_'+str( i + 1 )),
                )
            if ShopOnline.objects.filter(display_id=request.POST.get('id')).exists():
                ReserveOnlineFacility.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOnlineFacility),
                    online = ShopOnline.objects.filter(display_id=request.POST.get('id')).first(),
                    number = ( i + 1 ),
                    name = request.POST.get('name_'+str( i + 1 )),
                    count = request.POST.get('count_'+str( i + 1 )),
                    order = request.POST.get('order_'+str( i + 1 )),
                )
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )