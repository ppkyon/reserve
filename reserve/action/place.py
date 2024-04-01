from django.http import JsonResponse

from reserve.models import ReserveOfflinePlace, ReserveOnlinePlace, ReserveOfflineCourse, ReserveOnlineCourse
from sign.models import AuthLogin

from common import create_code

import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    ReserveOfflinePlace.objects.filter(shop=auth_login.shop).all().delete()
    ReserveOfflinePlace.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(12, ReserveOfflinePlace),
        shop = auth_login.shop,
        name = request.POST.get('offline_name'),
        outline = request.POST.get('offline_outline'),
    )
    ReserveOfflineCourse.objects.filter(shop=auth_login.shop).all().delete()
    for i in range(int(request.POST.get('offline_course_count'))):
        start = 0
        if request.POST.get('offline_course_start_'+str(i+1)):
            start = int(request.POST.get('offline_course_start_'+str(i+1)))
        deadline = 0
        if request.POST.get('offline_course_deadline_'+str(i+1)):
            deadline = int(request.POST.get('offline_course_deadline_'+str(i+1)))
        on_time = 0
        if request.POST.get('offline_course_on_time_'+str(i+1)):
            on_time = int(request.POST.get('offline_course_on_time_'+str(i+1)))
        any_day = 0
        if request.POST.get('offline_course_any_day_'+str(i+1)):
            any_day = int(request.POST.get('offline_course_any_day_'+str(i+1)))
        any_time = 0
        if request.POST.get('offline_course_any_time_'+str(i+1)):
            any_time = int(request.POST.get('offline_course_any_time_'+str(i+1)))
        method = 0
        if request.POST.get('offline_course_method_'+str(i+1)):
            method = int(request.POST.get('offline_course_method_'+str(i+1)))
        if request.POST.get('offline_course_business_check_1_'+str(i+1)) == '1':
            business_check_1 = True
        business_check_2 = False
        if request.POST.get('offline_course_business_check_2_'+str(i+1)) == '1':
            business_check_2 = True
        business_check_3 = False
        if request.POST.get('offline_course_business_check_3_'+str(i+1)) == '1':
            business_check_3 = True
        business_check_4 = False
        if request.POST.get('offline_course_business_check_4_'+str(i+1)) == '1':
            business_check_4 = True
        business_check_5 = False
        if request.POST.get('offline_course_business_check_5_'+str(i+1)) == '1':
            business_check_5 = True
        business_check_6 = False
        if request.POST.get('offline_course_business_check_6_'+str(i+1)) == '1':
            business_check_6 = True
        business_check_7 = False
        if request.POST.get('offline_course_business_check_7_'+str(i+1)) == '1':
            business_check_7 = True

        ReserveOfflineCourse.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, ReserveOfflineCourse),
            shop = auth_login.shop,
            number = (i+1),
            title = request.POST.get('offline_course_title_'+str(i+1)),
            outline = request.POST.get('offline_course_outline_'+str(i+1)),
            start = start,
            deadline = deadline,
            on_time = on_time,
            any_day = any_day,
            any_time = any_time,
            method = method,
            business_mon_day = business_check_1,
            business_tue_day = business_check_2,
            business_wed_day = business_check_3,
            business_thu_day = business_check_4,
            business_fri_day = business_check_5,
            business_sat_day = business_check_6,
            business_sun_day = business_check_7,
        )
    
    ReserveOnlinePlace.objects.filter(shop=auth_login.shop).all().delete()
    ReserveOnlinePlace.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(12, ReserveOnlinePlace),
        shop = auth_login.shop,
        name = request.POST.get('online_name'),
        outline = request.POST.get('online_outline'),
    )
    ReserveOnlineCourse.objects.filter(shop=auth_login.shop).all().delete()
    for i in range(int(request.POST.get('online_course_count'))):
        start = 0
        if request.POST.get('online_course_start_'+str(i+1)):
            start = int(request.POST.get('online_course_start_'+str(i+1)))
        deadline = 0
        if request.POST.get('online_course_deadline_'+str(i+1)):
            deadline = int(request.POST.get('online_course_deadline_'+str(i+1)))
        on_time = 0
        if request.POST.get('online_course_on_time_'+str(i+1)):
            on_time = int(request.POST.get('online_course_on_time_'+str(i+1)))
        any_day = 0
        if request.POST.get('online_course_any_day_'+str(i+1)):
            any_day = int(request.POST.get('online_course_any_day_'+str(i+1)))
        any_time = 0
        if request.POST.get('online_course_any_time_'+str(i+1)):
            any_time = int(request.POST.get('online_course_any_time_'+str(i+1)))
        method = 0
        if request.POST.get('online_course_method_'+str(i+1)):
            method = int(request.POST.get('online_course_method_'+str(i+1)))
        business_check_1 = False
        if request.POST.get('online_course_business_check_1_'+str(i+1)) == '1':
            business_check_1 = True
        business_check_2 = False
        if request.POST.get('online_course_business_check_2_'+str(i+1)) == '1':
            business_check_2 = True
        business_check_3 = False
        if request.POST.get('online_course_business_check_3_'+str(i+1)) == '1':
            business_check_3 = True
        business_check_4 = False
        if request.POST.get('online_course_business_check_4_'+str(i+1)) == '1':
            business_check_4 = True
        business_check_5 = False
        if request.POST.get('online_course_business_check_5_'+str(i+1)) == '1':
            business_check_5 = True
        business_check_6 = False
        if request.POST.get('online_course_business_check_6_'+str(i+1)) == '1':
            business_check_6 = True
        business_check_7 = False
        if request.POST.get('online_course_business_check_7_'+str(i+1)) == '1':
            business_check_7 = True

        ReserveOnlineCourse.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, ReserveOnlineCourse),
            shop = auth_login.shop,
            number = (i+1),
            title = request.POST.get('online_course_title_'+str(i+1)),
            outline = request.POST.get('online_course_outline_'+str(i+1)),
            start = start,
            deadline = deadline,
            on_time = on_time,
            any_day = any_day,
            any_time = any_time,
            method = method,
            business_mon_day = business_check_1,
            business_tue_day = business_check_2,
            business_wed_day = business_check_3,
            business_thu_day = business_check_4,
            business_fri_day = business_check_5,
            business_sat_day = business_check_6,
            business_sun_day = business_check_7,
        )
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )