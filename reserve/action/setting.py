from django.http import JsonResponse

from reserve.models import ReserveOfflineSetting, ReserveOnlineSetting, ReserveOnlineMeeting
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthLogin

from common import create_code

import datetime
import uuid

def save(request):
    random_list = list()
    for i in range(int(request.POST.get('count'))):
        random_list.append(request.POST.get('random_'+str( i + 1 )))

    for delete_item in ReserveOnlineSetting.objects.filter(online=ShopOnline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all():
        ReserveOnlineMeeting.objects.filter(online=delete_item).all().delete()
    ReserveOnlineSetting.objects.filter(online=ShopOnline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all().delete()
    ReserveOfflineSetting.objects.filter(offline=ShopOffline.objects.filter(display_id=request.POST.get('id')).first()).exclude(display_id__in=random_list).all().delete()
    
    for i in range(int(request.POST.get('count'))):
        if request.POST.get('course_flg_'+str(i+1)) == '1':
            course_flg = True
        else:
            course_flg = False
        if request.POST.get('display_flg_'+str(i+1)) == '1':
            display_flg = True
        else:
            display_flg = False

        if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('random_'+str(i+1))).exists():
            offline = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('random_'+str(i+1))).first()
            offline.number = ( i + 1 )
            offline.title = request.POST.get('title_'+str( i + 1 ))
            offline.name = request.POST.get('name_'+str( i + 1 ))
            offline.outline = request.POST.get('outline_'+str( i + 1 ))
            offline.note = request.POST.get('note_'+str( i + 1 ))
            offline.time = request.POST.get('time_'+str( i + 1 ))
            offline.people = request.POST.get('people_'+str( i + 1 ))
            offline.facility = request.POST.get('facility_'+str( i + 1 ))
            offline.course_flg = course_flg
            offline.display_flg = display_flg
            offline.save()
        elif ReserveOnlineSetting.objects.filter(display_id=request.POST.get('random_'+str(i+1))).exists():
            online = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('random_'+str(i+1))).first()
            online.number = ( i + 1 )
            online.title = request.POST.get('title_'+str( i + 1 ))
            online.name = request.POST.get('name_'+str( i + 1 ))
            online.outline = request.POST.get('outline_'+str( i + 1 ))
            online.note = request.POST.get('note_'+str( i + 1 ))
            online.time = request.POST.get('time_'+str( i + 1 ))
            online.people = request.POST.get('people_'+str( i + 1 ))
            online.facility = request.POST.get('facility_'+str( i + 1 ))
            offline.course_flg = course_flg
            online.display_flg = display_flg
            online.save()

            ReserveOnlineMeeting.objects.filter(online=online).all().delete()
            for j in range(int(request.POST.get('meeting_count_'+str( i + 1 )))):
                platform_text = None
                if request.POST.get('meeting_platform_text_'+str( i + 1 )+'_'+str( j + 1 )):
                    platform_text = request.POST.get('meeting_platform_text_'+str( i + 1 )+'_'+str( j + 1 ))
                
                start_data = None
                expiration_date = None
                if request.POST.get('meeting_start_'+str( i + 1 )+'_'+str( j + 1 )):
                    start_data = datetime.datetime.strptime(request.POST.get('meeting_start_'+str( i + 1 )+'_'+str( j + 1 )), '%Y/%m/%d')
                    expiration_date = start_data + datetime.timedelta(days=90)
                
                ReserveOnlineMeeting.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOnlineMeeting),
                    online = online,
                    number = ( j + 1 ),
                    name = request.POST.get('meeting_name_'+str( i + 1 )+'_'+str( j + 1 )),
                    url = request.POST.get('meeting_url_'+str( i + 1 )+'_'+str( j + 1 )),
                    platform = request.POST.get('meeting_platform_'+str( i + 1 )+'_'+str( j + 1 )),
                    platform_text = platform_text,
                    start_date = start_data,
                    expiration_date = expiration_date,
                    status = request.POST.get('meeting_status_'+str( i + 1 )+'_'+str( j + 1 )),
                    author = request.user.display_id,
                )
        else:
            if ShopOffline.objects.filter(display_id=request.POST.get('id')).exists():
                ReserveOfflineSetting.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOfflineSetting),
                    offline = ShopOffline.objects.filter(display_id=request.POST.get('id')).first(),
                    number = ( i + 1 ),
                    title = request.POST.get('title_'+str( i + 1 )),
                    name = request.POST.get('name_'+str( i + 1 )),
                    outline = request.POST.get('outline_'+str( i + 1 )),
                    note = request.POST.get('note_'+str( i + 1 )),
                    time = request.POST.get('time_'+str( i + 1 )),
                    people = request.POST.get('people_'+str( i + 1 )),
                    display_flg = display_flg,
                )
            if ShopOnline.objects.filter(display_id=request.POST.get('id')).exists():
                online = ReserveOnlineSetting.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, ReserveOfflineSetting),
                    online = ShopOnline.objects.filter(display_id=request.POST.get('id')).first(),
                    number = ( i + 1 ),
                    title = request.POST.get('title_'+str( i + 1 )),
                    name = request.POST.get('name_'+str( i + 1 )),
                    outline = request.POST.get('outline_'+str( i + 1 )),
                    note = request.POST.get('note_'+str( i + 1 )),
                    time = request.POST.get('time_'+str( i + 1 )),
                    people = request.POST.get('people_'+str( i + 1 )),
                    display_flg = display_flg,
                )
                for j in range(int(request.POST.get('meeting_count_'+str( i + 1 )))):
                    platform_text = None
                    if request.POST.get('meeting_platform_text_'+str( i + 1 )+'_'+str( j + 1 )):
                        platform_text = request.POST.get('meeting_platform_text_'+str( i + 1 )+'_'+str( j + 1 ))
                    
                    start_data = None
                    expiration_date = None
                    if request.POST.get('meeting_start_'+str( i + 1 )+'_'+str( j + 1 )):
                        start_data = datetime.datetime.strptime(request.POST.get('meeting_start_'+str( i + 1 )+'_'+str( j + 1 )), '%Y/%m/%d')
                        expiration_date = start_data + datetime.timedelta(days=90)
                    
                    ReserveOnlineMeeting.objects.create(
                        id = str(uuid.uuid4()),
                        display_id = create_code(12, ReserveOnlineMeeting),
                        online = online,
                        number = ( j + 1 ),
                        name = request.POST.get('meeting_name_'+str( i + 1 )+'_'+str( j + 1 )),
                        url = request.POST.get('meeting_url_'+str( i + 1 )+'_'+str( j + 1 )),
                        platform = request.POST.get('meeting_platform_'+str( i + 1 )+'_'+str( j + 1 )),
                        platform_text = platform_text,
                        start_date = start_data,
                        expiration_date = expiration_date,
                        status = request.POST.get('meeting_status_'+str( i + 1 )+'_'+str( j + 1 )),
                        author = request.user.display_id,
                    )

    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )