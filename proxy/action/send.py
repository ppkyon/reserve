from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import JsonResponse

from PIL import Image

from flow.models import ShopFlowTab, UserFlow, UserFlowSchedule
from question.models import ShopQuestion, ShopQuestionItem, ShopQuestionItemChoice, UserQuestion, UserQuestionItem, UserQuestionItemChoice
from reception.models import ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflineSetting, ReserveOnlineSetting,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu, ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
)
from sign.models import AuthLogin
from user.models import LineUser, UserProfile

from common import create_code

import base64
import cv2
import datetime
import environ
import io
import os
import urllib.parse
import uuid

env = environ.Env()
env.read_env('.env')

def send(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        manager_list = list()
        facility_list = list()
        schedule_datetime = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        schedule_add_datetime = schedule_datetime + datetime.timedelta(minutes=setting.time)
        if setting:
            for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=setting).all():
                reception_manager = ReceptionOfflineManager.objects.filter(offline=setting.offline, manager=manager_menu_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).exists():
                            reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).first()
                            if reception_offline_manager_setting.flg:
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)
                
        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(join=2).all():
            schedule_list.append(schedule)

        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        manager_count = len(manager_list)
        facility_count = len(facility_list)
        reception_manager_list = list()
        reception_facility_list = list()
        count_flg = True
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.offline.time)

            people_number = 0
            people_count = setting.people
            same_count = setting.facility
            if add_date > schedule_date and schedule_add_date > date:
                if manager_count <= 0 or facility_count <= 0:
                    break
                else:
                    if schedule_item.offline:
                        if schedule_item.offline == setting:
                            if schedule_date == date:
                                if count_flg:
                                    if schedule_item.offline_facility and schedule_item.offline_facility.count < people_count:
                                        same_count = same_count - 1
                                        if same_count == 0:
                                            people_count = schedule_item.offline_facility.count
                                        while same_count > 0:
                                            people_number = people_number + 1
                                            facility_count = facility_count - 1
                                            if facility_list[people_number] and schedule_item.offline_facility.count + facility_list[people_number].count <= people_count:
                                                people_count = schedule_item.offline_facility.count + facility_list[people_number].count
                                            else:
                                                people_number = people_number - 1
                                                facility_count = facility_count + 1
                                            same_count = same_count - 1
                                    count_flg = False
                                people_count = people_count - 1
                                if people_count <= 0:
                                    if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                        manager_count = manager_count - 1
                                        reception_manager_list.append(schedule_item.manager)
                                    if schedule_item.offline_facility in facility_list and not schedule_item.offline_facility in reception_facility_list:
                                        facility_count = facility_count - 1
                                        reception_facility_list.append(schedule_item.offline_facility)

                                    people_number = people_number + 1
                                    people_count = setting.people
                                    if facility_count > 0 and facility_list[people_number].count < people_count:
                                        people_count = facility_list[people_number].count
                            else:
                                if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                    manager_count = manager_count - 1
                                    reception_manager_list.append(schedule_item.manager)
                                if schedule_item.offline_facility in facility_list and not schedule_item.offline_facility in reception_facility_list:
                                    facility_count = facility_count - 1
                                    reception_facility_list.append(schedule_item.offline_facility)
                        else:
                            if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                manager_count = manager_count - 1
                                reception_manager_list.append(schedule_item.manager)
                            if schedule_item.offline_facility in facility_list and not schedule_item.offline_facility in reception_facility_list:
                                facility_count = facility_count - 1
                                reception_facility_list.append(schedule_item.offline_facility)

    if ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        manager_list = list()
        facility_list = list()
        schedule_datetime = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        schedule_add_datetime = schedule_datetime + datetime.timedelta(minutes=setting.time)
        if setting:
            for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=setting).all():
                reception_manager = ReceptionOnlineManager.objects.filter(online=setting.online, manager=manager_menu_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).exists():
                            reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).first()
                            if reception_online_manager_setting.flg:
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)

        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(join=2).all():
            schedule_list.append(schedule)

        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        manager_count = len(manager_list)
        facility_count = len(facility_list)
        reception_manager_list = list()
        reception_facility_list = list()
        count_flg = True
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.offline.time)

            people_number = 0
            people_count = setting.people
            same_count = setting.facility
            if add_date > schedule_date and schedule_add_date > date:
                if manager_count <= 0 or facility_count <= 0:
                    break
                else:
                    if schedule_item.online:
                        if schedule_item.online == setting:
                            if schedule_date == date:
                                if count_flg:
                                    if schedule_item.online_facility and schedule_item.online_facility.count < people_count:
                                        same_count = same_count - 1
                                        if same_count == 0:
                                            people_count = schedule_item.online_facility.count
                                        while same_count > 0:
                                            people_number = people_number + 1
                                            facility_count = facility_count - 1
                                            if facility_list[people_number] and schedule_item.online_facility.count + facility_list[people_number].count <= people_count:
                                                people_count = schedule_item.online_facility.count + facility_list[people_number].count
                                            else:
                                                people_number = people_number - 1
                                                facility_count = facility_count + 1
                                            same_count = same_count - 1
                                    count_flg = False
                                people_count = people_count - 1
                                if people_count <= 0:
                                    if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                        manager_count = manager_count - 1
                                        reception_manager_list.append(schedule_item.manager)
                                    if schedule_item.online_facility in facility_list and not schedule_item.online_facility in reception_facility_list:
                                        facility_count = facility_count - 1
                                        reception_facility_list.append(schedule_item.online_facility)

                                    people_number = people_number + 1
                                    people_count = setting.people
                                    if facility_count > 0 and facility_list[people_number].count < people_count:
                                        people_count = facility_list[people_number].count
                            else:
                                if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                    manager_count = manager_count - 1
                                    reception_manager_list.append(schedule_item.manager)
                                if schedule_item.online_facility in facility_list and not schedule_item.online_facility in reception_facility_list:
                                    facility_count = facility_count - 1
                                    reception_facility_list.append(schedule_item.online_facility)
                        else:
                            if schedule_item.manager in manager_list and not schedule_item.manager in reception_manager_list:
                                manager_count = manager_count - 1
                                reception_manager_list.append(schedule_item.manager)
                            if schedule_item.online_facility in facility_list and not schedule_item.online_facility in reception_facility_list:
                                facility_count = facility_count - 1
                                reception_facility_list.append(schedule_item.online_facility)

    if manager_count <= 0 or facility_count <= 0:
        return JsonResponse( {'error': True}, safe=False )

    user = LineUser.objects.create(
        id = str(uuid.uuid4()),
        display_id = create_code(12, LineUser),
        shop = auth_login.shop,
        line_user_id = None,
        display_name = None,
        display_image = None,
        status = 1,
        proxy_flg = True,
        updated_at = datetime.datetime.now(),
    )

    if UserProfile.objects.filter(user=user).exists():
        user_profile = UserProfile.objects.filter(user=user).first()
        user_profile.atelle_id = create_atelle_id(),
        user_profile.save()
    else:
        user_profile = UserProfile.objects.create(
            id = str(uuid.uuid4()),
            user = user,
            atelle_id = create_atelle_id(),
        )

    user.updated_at = datetime.datetime.now()
    user.save()

    question = None
    if request.POST.get('question_id'):
        question = ShopQuestion.objects.filter(display_id=request.POST.get('question_id')).first()
        user_question = UserQuestion.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, UserQuestion),
            user = user,
            question = question,
            title = question.title,
            name = question.name,
            description =  question.description,
            color = question.color,
            count = question.count,
        )
        
        UserQuestionItem.objects.filter(question=user_question).all().delete()
        for shop_question_index, shop_question_item in enumerate(ShopQuestionItem.objects.filter(question=question).order_by('number').all()):
            if request.POST.get('type_'+str(shop_question_index+1)) == '1':
                if request.POST.get('text_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))),
                    )
                    user_profile.name = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1)))
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        text = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '2':
                if request.POST.get('text_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))),
                    )
                    user_profile.name_kana = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1)))
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        text = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '3':
                if request.POST.get('value_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        value = urllib.parse.unquote(request.POST.get('value_'+str(shop_question_index+1))).replace('歳', ''),
                    )
                    user_profile.age = urllib.parse.unquote(request.POST.get('value_'+str(shop_question_index+1))).replace('歳', '')
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        value = 0,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '4':
                if request.POST.get('value_'+str(shop_question_index+1)):
                    if request.POST.get('value_'+str(shop_question_index+1)):
                        UserQuestionItem.objects.create(
                            id = str(uuid.uuid4()),
                            question = user_question,
                            number = shop_question_item.number,
                            type = shop_question_item.type,
                            title = shop_question_item.title,
                            description = shop_question_item.description,
                            choice_type = shop_question_item.choice_type,
                            choice_count = shop_question_item.choice_count,
                            required_flg = shop_question_item.required_flg,
                            value = 0,
                        )
                    elif urllib.parse.unquote(request.POST.get('value_'+str(shop_question_index+1))) == '男性':
                        UserQuestionItem.objects.create(
                            id = str(uuid.uuid4()),
                            question = user_question,
                            number = shop_question_item.number,
                            type = shop_question_item.type,
                            title = shop_question_item.title,
                            description = shop_question_item.description,
                            choice_type = shop_question_item.choice_type,
                            choice_count = shop_question_item.choice_count,
                            required_flg = shop_question_item.required_flg,
                            value = 1,
                        )
                        user_profile.sex = 1
                    elif urllib.parse.unquote(request.POST.get('value_'+str(shop_question_index+1))) == '女性':
                        UserQuestionItem.objects.create(
                            id = str(uuid.uuid4()),
                            question = user_question,
                            number = shop_question_item.number,
                            type = shop_question_item.type,
                            title = shop_question_item.title,
                            description = shop_question_item.description,
                            choice_type = shop_question_item.choice_type,
                            choice_count = shop_question_item.choice_count,
                            required_flg = shop_question_item.required_flg,
                            value = 2,
                        )
                        user_profile.sex = 2
                    user_profile.save()
            elif request.POST.get('type_'+str(shop_question_index+1)) == '5':
                if request.POST.get('text_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))).replace( '-', ''),
                    )
                    user_profile.phone_number = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))).replace( '-', '')
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        text = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '6':
                if request.POST.get('email_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        email = urllib.parse.unquote(request.POST.get('email_'+str(shop_question_index+1))),
                    )
                    user_profile.email = urllib.parse.unquote(request.POST.get('email_'+str(shop_question_index+1)))
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        email = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '7':
                if request.POST.get('date_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        date = urllib.parse.unquote(request.POST.get('date_'+str(shop_question_index+1))).replace( '/', '-'),
                    )
                    today = datetime.date.today()
                    birthday = datetime.datetime.strptime(urllib.parse.unquote(request.POST.get('date_'+str(shop_question_index+1))).replace( '/', '-'), '%Y-%m-%d')
                    user_profile.age = (int(today.strftime("%Y%m%d")) - int(birthday.strftime("%Y%m%d"))) // 10000
                    user_profile.birth = urllib.parse.unquote(request.POST.get('date_'+str(shop_question_index+1))).replace( '/', '-')
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        date = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '8':
                if request.POST.get('text_'+str(shop_question_index+1)):
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1))),
                    )
                    user_profile.address = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1)))
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        text = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '9':
                if request.POST.get('image_'+str(shop_question_index+1)):
                    if ';base64,' in request.POST.get('image_'+str(shop_question_index+1)):
                        format, imgstr = request.POST.get('image_'+str(shop_question_index+1)).split(';base64,') 
                        ext = format.split('/')[-1]
                        data = ContentFile(base64.b64decode(request.POST.get('image_url_'+str(shop_question_index+1)).replace( ' ', '+' )), name='temp.' + ext)
                    else:
                        data = request.POST.get('image_url_'+str(shop_question_index+1))
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        image = data,
                    )
                    user_profile.image = data
                    user_profile.save()
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        image = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '10':
                if request.POST.get('image_'+str(shop_question_index+1)):
                    if ';base64,' in request.POST.get('image_'+str(shop_question_index+1)):
                        format, imgstr = request.POST.get('image_'+str(shop_question_index+1)).split(';base64,') 
                        ext = format.split('/')[-1]
                        data = ContentFile(base64.b64decode(request.POST.get('image_url_'+str(shop_question_index+1)).replace( ' ', '+' )), name='temp.' + ext)
                    else:
                        data = request.POST.get('image_url_'+str(shop_question_index+1))
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        image = data,
                    )
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        image = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '11':
                if request.POST.get('video_'+str(shop_question_index+1)):
                    if ';base64,' in request.POST.get('video_'+str(shop_question_index+1)):
                        format, imgstr = request.POST.get('video_'+str(shop_question_index+1)).split(';base64,') 
                        ext = format.split('/')[-1] 
                        data = ContentFile(base64.b64decode(request.POST.get('video_'+str(shop_question_index+1)).replace( ' ', '+' )), name='temp.' + ext)
                    else:
                        data = request.POST.get('video_url_'+str(shop_question_index+1))
                    user_question_item = UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        video = data,
                        video_thumbnail = None,
                    )

                    if env('AWS_FLG') == 'True':
                        video_name = './static/' + str(uuid.uuid4()).replace('-', '') + '.mp4'
                        urllib.request.urlretrieve(user_question_item.video.url, video_name)
                        cap = cv2.VideoCapture(video_name)
                    else:
                        cap = cv2.VideoCapture(user_question_item.video.url[1:])
                    res, thumbnail = cap.read()
                    image = Image.fromarray(cv2.cvtColor(thumbnail, cv2.COLOR_BGR2RGB))
                    image_io = io.BytesIO()
                    image.save(image_io, format="JPEG")
                    image_file = InMemoryUploadedFile(image_io, field_name=None, name=str(uuid.uuid4()).replace('-', '') + '.jpg', content_type="image/jpeg", size=image_io.getbuffer().nbytes, charset=None)
                    
                    user_question_item.video_thumbnail = image_file
                    user_question_item.save()

                    cap.release()
                    if env('AWS_FLG') == 'True':
                        os.remove(video_name)
                else:
                    UserQuestionItem.objects.create(
                        id = str(uuid.uuid4()),
                        question = user_question,
                        number = shop_question_item.number,
                        type = shop_question_item.type,
                        title = shop_question_item.title,
                        description = shop_question_item.description,
                        choice_type = shop_question_item.choice_type,
                        choice_count = shop_question_item.choice_count,
                        required_flg = shop_question_item.required_flg,
                        video = None,
                        video_thumbnail = None,
                    )
            elif request.POST.get('type_'+str(shop_question_index+1)) == '99':
                user_question_item = UserQuestionItem.objects.create(
                    id = str(uuid.uuid4()),
                    question = user_question,
                    number = shop_question_item.number,
                    type = shop_question_item.type,
                    title = shop_question_item.title,
                    description = shop_question_item.description,
                    choice_type = shop_question_item.choice_type,
                    choice_count = shop_question_item.choice_count,
                    required_flg = shop_question_item.required_flg,
                )
                UserQuestionItemChoice.objects.filter(question=user_question_item).all().delete()
                if request.POST.get('choice_type_'+str(shop_question_index+1)) == '1':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('text_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1)):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                text = urllib.parse.unquote(request.POST.get('text_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1))),
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                text = None,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '2':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('choice_value_'+str(shop_question_index+1)) == str(shop_question_choice_item.number):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                text = 1,
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                text = 0,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '3':
                    choice_value = request.POST.getlist('choice_value_'+str(shop_question_index+1)+'%5B%5D')
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if str(shop_question_choice_item.number) in choice_value:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                text = 1,
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                text = 0,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '4':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('choice_text_'+str(shop_question_index+1)) == shop_question_choice_item.text:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                text = 1,
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                text = 0,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '5':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('date_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1)):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                date = urllib.parse.unquote(request.POST.get('date_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1))).replace( '/', '-'),
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                date = None,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '6':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('time_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1)):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                time = urllib.parse.unquote(request.POST.get('time_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1))),
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                time = None,
                            )
                elif request.POST.get('choice_type_'+str(shop_question_index+1)) == '7':
                    for shop_question_choice_index, shop_question_choice_item in enumerate(ShopQuestionItemChoice.objects.filter(question_item=shop_question_item).order_by('number').all()):
                        if request.POST.get('date_time_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1)):
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                date = urllib.parse.unquote(request.POST.get('date_time_'+str(shop_question_index+1)+'_'+str(shop_question_choice_index+1))).replace( '/', '-'),
                            )
                        else:
                            UserQuestionItemChoice.objects.create(
                                id = str(uuid.uuid4()),
                                question = user_question_item,
                                number = shop_question_choice_item.number,
                                title = shop_question_choice_item.text,
                                date = None,
                            )
    
    target_flow_tab = None
    if ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        for menu in ReserveOfflineFlowMenu.objects.filter(shop=auth_login.shop, offline=setting).all():
            flow_tab = ShopFlowTab.objects.filter(name=menu.flow).first()
            if not target_flow_tab or target_flow_tab.number > flow_tab.number:
                target_flow_tab = flow_tab
        
        people_count = setting.people
        manager_list = list()
        facility_list = list()
        schedule_datetime = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        schedule_add_datetime = schedule_datetime + datetime.timedelta(minutes=setting.time)
        if setting:
            for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=setting).all():
                reception_manager = ReceptionOfflineManager.objects.filter(offline=setting.offline, manager=manager_menu_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).exists():
                            reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).first()
                            if reception_offline_manager_setting.flg:
                                manager_menu_item.manager.count = people_count
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_menu_item.manager.count = people_count
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_menu_item.manager.count = people_count
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)
        
        user_flow = UserFlow.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, UserFlow),
            user = user,
            number = UserFlow.objects.filter(user=user).count() + 1,
            flow = target_flow_tab.flow,
            flow_tab = target_flow_tab,
            flow_item = None,
            name = target_flow_tab.name,
            richmenu = None,
            end_flg = False,
            updated_at = datetime.datetime.now(),
        )

        for flow_tab in ShopFlowTab.objects.filter(Q(flow=target_flow_tab.flow), Q(Q(member=0)|Q(member=2))).all():
            if flow_tab.number > user_flow.flow_tab.number:
                UserFlow.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, UserFlow),
                    user = user,
                    number = UserFlow.objects.filter(user=user).count() + 1,
                    flow = flow_tab.flow,
                    flow_tab = flow_tab,
                    flow_item = None,
                    name = flow_tab.name,
                    richmenu = None,
                    end_flg = False,
                )
        
        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(join=2).all():
            schedule_list.append(schedule)

        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        reception_manager_list = list()
        reception_facility_list = list()
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.offline.time)

            if add_date > schedule_date and schedule_add_date > date:
                if schedule_item.offline == setting:
                    if schedule_date == date:
                        for manager_item in manager_list:
                            if manager_item == schedule_item.manager:
                                manager_item.count = manager_item.count - 1
                                if manager_item.count <= 0:
                                    reception_manager_list.append(schedule_item.manager.id)
                        for facility_item in facility_list:
                            if facility_item == schedule_item.offline_facility:
                                facility_item.count = facility_item.count - 1
                                if facility_item.count <= 0:
                                    reception_facility_list.append(facility_item.id)
                    else:
                        reception_manager_list.append(schedule_item.manager.id)
                        reception_facility_list.append(schedule_item.offline_facility.id)
                else:
                    reception_manager_list.append(schedule_item.manager.id)
                    reception_facility_list.append(schedule_item.offline_facility.id)
        
        manager = None
        for manager_item in ReserveOfflineManagerMenu.objects.filter(shop=auth_login.shop, offline=setting).order_by('manager__created_at').all():
            reception_manager = ReceptionOfflineManager.objects.filter(offline=setting.offline, manager=manager_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
            if reception_manager:
                if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).exists():
                        reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=setting).first()
                        if reception_offline_manager_setting.flg:
                            if not manager_item.manager.id in reception_manager_list:
                                manager = manager_item.manager
                                break
                    else:
                        if not manager_item.manager.id in reception_manager_list:
                            manager = manager_item.manager
                            break
                else:
                    if not manager_item.manager.id in reception_manager_list:
                        manager = manager_item.manager
                        break

        facility = None
        for facility_item in ReserveOfflineFacilityMenu.objects.filter(shop=auth_login.shop, offline=setting).all():
            if not facility_item.facility.id in reception_facility_list:
                facility = facility_item.facility
                break
        
        course = None
        if request.POST.get('course_id'):
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()

        if UserFlowSchedule.objects.filter(flow=user_flow, join=0).exists():
            user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow, join=0).order_by('-number').first()
            user_flow_schedule.number = 1
            user_flow_schedule.date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day')
            user_flow_schedule.time = request.POST.get('hour') + ':' + request.POST.get('minute')
            user_flow_schedule.join = 0
            user_flow_schedule.offline = setting
            user_flow_schedule.offline_course = course
            user_flow_schedule.offline_facility = facility
            user_flow_schedule.manager = manager
            user_flow_schedule.question = question
            user_flow_schedule.updated_at = datetime.datetime.now()
            user_flow_schedule.save()
        else:
            UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                flow = user_flow,
                number = 1,
                date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
                time = request.POST.get('hour') + ':' + request.POST.get('minute'),
                join = 0,
                offline = setting,
                offline_course = course,
                offline_facility = facility,
                manager = manager,
                question = question,
                updated_at = datetime.datetime.now()
            )
    
    if ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        for menu in ReserveOnlineFlowMenu.objects.filter(shop=auth_login.shop, online=setting).all():
            flow_tab = ShopFlowTab.objects.filter(name=menu.flow).first()
            if not target_flow_tab or target_flow_tab.number > flow_tab.number:
                target_flow_tab = flow_tab
        
        people_count = setting.people
        manager_list = list()
        facility_list = list()
        schedule_datetime = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        schedule_add_datetime = schedule_datetime + datetime.timedelta(minutes=setting.time)
        if setting:
            for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=setting).all():
                reception_manager = ReceptionOnlineManager.objects.filter(online=setting.online, manager=manager_menu_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
                if reception_manager:
                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).exists():
                            reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).first()
                            if reception_online_manager_setting.flg:
                                manager_menu_item.manager.count = people_count
                                manager_list.append(manager_menu_item.manager)
                        else:
                            manager_menu_item.manager.count = people_count
                            manager_list.append(manager_menu_item.manager)
                    else:
                        manager_menu_item.manager.count = people_count
                        manager_list.append(manager_menu_item.manager)
            for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=setting).order_by('facility__order').all():
                facility_list.append(facility_menu_item.facility)
        
        user_flow = UserFlow.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, UserFlow),
            user = user,
            number = UserFlow.objects.filter(user=user).count() + 1,
            flow = target_flow_tab.flow,
            flow_tab = target_flow_tab,
            flow_item = None,
            name = target_flow_tab.name,
            richmenu = None,
            end_flg = False,
            updated_at = datetime.datetime.now(),
        )

        for flow_tab in ShopFlowTab.objects.filter(Q(flow=target_flow_tab.flow), Q(Q(member=0)|Q(member=2))).all():
            if flow_tab.number > user_flow.flow_tab.number:
                UserFlow.objects.create(
                    id = str(uuid.uuid4()),
                    display_id = create_code(12, UserFlow),
                    user = user,
                    number = UserFlow.objects.filter(user=user).count() + 1,
                    flow = flow_tab.flow,
                    flow_tab = flow_tab,
                    flow_item = None,
                    name = flow_tab.name,
                    richmenu = None,
                    end_flg = False,
                )

        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(flow__user__shop=auth_login.shop, date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(join=2).all():
            schedule_list.append(schedule)

        date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
        add_date = date + datetime.timedelta(minutes=setting.time)

        reception_manager_list = list()
        reception_facility_list = list()
        for schedule_item in schedule_list:
            schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.online.time)

            if add_date > schedule_date and schedule_add_date > date:
                if schedule_item.online == setting:
                    if schedule_date == date:
                        for manager_item in manager_list:
                            if manager_item == schedule_item.manager:
                                manager_item.count = manager_item.count - 1
                                if manager_item.count <= 0:
                                    reception_manager_list.append(schedule_item.manager.id)
                        for facility_item in facility_list:
                            if facility_item == schedule_item.online_facility:
                                facility_item.count = facility_item.count - 1
                                if facility_item.count <= 0:
                                    reception_facility_list.append(facility_item.id)
                    else:
                        reception_manager_list.append(schedule_item.manager.id)
                        reception_facility_list.append(schedule_item.online_facility.id)
                else:
                    reception_manager_list.append(schedule_item.manager.id)
                    reception_facility_list.append(schedule_item.online_facility.id)

        for manager_item in ReserveOnlineManagerMenu.objects.filter(shop=auth_login.shop, online=setting).order_by('manager__created_at').all():
            reception_manager = ReceptionOnlineManager.objects.filter(online=setting.online, manager=manager_item.manager, reception_date__year=request.POST.get('year'), reception_date__month=request.POST.get('month'), reception_date__day=request.POST.get('day'), reception_from__lte=schedule_datetime.time(), reception_to__gte=schedule_add_datetime.time(), reception_flg=True).first()
            if reception_manager:
                if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).exists():
                        reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=setting).first()
                        if reception_online_manager_setting.flg:
                            if not manager_item.manager.id in reception_manager_list:
                                manager = manager_item.manager
                                break
                    else:
                        if not manager_item.manager.id in reception_manager_list:
                            manager = manager_item.manager
                            break
                else:
                    if not manager_item.manager.id in reception_manager_list:
                        manager = manager_item.manager
                        break
        facility = None
        for facility_item in ReserveOnlineFacilityMenu.objects.filter(shop=auth_login.shop, online=setting).all():
            if not facility_item.facility.id in reception_facility_list:
                facility = facility_item.facility
                break
        
        course = None
        if request.POST.get('course_id'):
            course = ReserveOnlineCourse.objects.filter(display_id=request.POST.get('course_id')).first()

        if UserFlowSchedule.objects.filter(flow=user_flow, join=0).exists():
            user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow, join=0).order_by('-number').first()
            user_flow_schedule.number = 1
            user_flow_schedule.date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day')
            user_flow_schedule.time = request.POST.get('hour') + ':' + request.POST.get('minute')
            user_flow_schedule.join = 0
            user_flow_schedule.online = setting
            user_flow_schedule.online_course = course
            user_flow_schedule.online_facility = facility
            user_flow_schedule.manager = manager
            user_flow_schedule.question = question
            user_flow_schedule.updated_at = datetime.datetime.now()
            user_flow_schedule.save()
        else:
            UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                flow = user_flow,
                number = 1,
                date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day'),
                time = request.POST.get('hour') + ':' + request.POST.get('minute'),
                join = 0,
                online = setting,
                online_course = course,
                online_facility = facility,
                manager = manager,
                question = question,
                updated_at = datetime.datetime.now()
            )

    return JsonResponse( {}, safe=False )



def create_atelle_id():
    code_list = UserProfile.objects.values_list('atelle_id', flat=True)
    number = 1
    while True:
        code = datetime.datetime.now().strftime('%Y%m%d') + str(number).zfill(2)
        if int(code) not in code_list:
            break
        number += 1
    return int(code)