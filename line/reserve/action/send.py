from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.http import JsonResponse

from PIL import Image

from flow.models import ShopFlowTab, ShopFlowItem, ShopFlowRichMenu, UserFlow, UserFlowSchedule
from question.models import ShopQuestion, ShopQuestionItem, ShopQuestionItemChoice, UserQuestion, UserQuestionItem, UserQuestionItemChoice
from reception.models import ReceptionOfflinePlace, ReceptionOnlinePlace, ReceptionOfflineManager, ReceptionOnlineManager, ReceptionOfflineManagerSetting, ReceptionOnlineManagerSetting
from reserve.models import (
    ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflineSetting, ReserveOnlineSetting, ReserveUserStartDate, ReserveCalendarDate, ReserveCalendarTime, ReserveTempCalendar,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu, ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
)
from richmenu.models import UserRichMenu
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthShop
from user.models import LineUser, UserProfile

from common import create_code
from flow.action.go import go
from line.action.richmenu import create_rich_menu, delete_rich_menu

import base64
import cv2
import datetime
import environ
import io
import os
import pandas
import urllib.parse
import urllib.request
import uuid

env = environ.Env()
env.read_env('.env')

def send(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).first()

    if UserProfile.objects.filter(user=user).exists():
        user_profile = UserProfile.objects.filter(user=user).first()
    else:
        user_profile = UserProfile.objects.create(
            id = str(uuid.uuid4()),
            user = user,
        )

    if not UserFlowSchedule.objects.filter(flow__user=user, number=0, temp_flg=True).exists():
        return JsonResponse( {'temp': True}, safe=False )

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
        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(flow__user=user, number=0, temp_flg=True).all():
            if schedule.join != 2:
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
            schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule_item.offline.time)

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
                                            if people_count > schedule_item.offline_facility.count:
                                                people_count = schedule_item.offline_facility.count
                                        else:
                                            people_total_count = schedule_item.offline_facility.count
                                            while same_count > 0:
                                                people_number = people_number + 1
                                                people_total_count = people_total_count + facility_list[people_number].count
                                                if facility_list[people_number] and not facility_list[people_number] in reception_facility_list:
                                                    facility_count = facility_count - 1
                                                    reception_facility_list.append(facility_list[people_number])
                                                same_count = same_count - 1
                                            if people_count > people_total_count:
                                                people_count = people_total_count
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
        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(flow__user=user, number=0, temp_flg=True).all():
            if schedule.join != 2:
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
                                            if people_count > schedule_item.online_facility.count:
                                                people_count = schedule_item.online_facility.count
                                        else:
                                            people_total_count = schedule_item.online_facility.count
                                            while same_count > 0:
                                                people_number = people_number + 1
                                                people_total_count = people_total_count + facility_list[people_number].count
                                                if facility_list[people_number] and not facility_list[people_number] in reception_facility_list:
                                                    facility_count = facility_count - 1
                                                    reception_facility_list.append(facility_list[people_number])
                                                same_count = same_count - 1
                                            if people_count > people_total_count:
                                                people_count = people_total_count
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

    user.updated_at = datetime.datetime.now()
    user.save()
    
    question = None
    if request.POST.get('question_id'):
        question = ShopQuestion.objects.filter(display_id=request.POST.get('question_id')).first()
        if UserQuestion.objects.filter(user=user, question=question).exists():
            user_question = UserQuestion.objects.filter(user=user, question=question).first()
            user_question.title = question.title
            user_question.name = question.name
            user_question.description =  question.description
            user_question.color = question.color
            user_question.count = question.count
            user_question.save()
        else:
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
        user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user).first()
        setting = ReserveOfflineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        for menu in ReserveOfflineFlowMenu.objects.filter(shop=shop, offline=setting).all():
            flow_tab = ShopFlowTab.objects.filter(flow=user_flow.flow, flow__shop=shop, name=menu.flow).first()
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
                
        target_flg = False
        target_flow_item = None
        target_rich_menu = None
        for flow_item in ShopFlowItem.objects.filter(flow_tab=target_flow_tab).all():
            if flow_item.type == 7:
                target_rich_menu = ShopFlowRichMenu.objects.filter(flow=flow_item).first()
                target_rich_menu = target_rich_menu.rich_menu
            if target_flg:
                target_flow_item = flow_item
                break
            if flow_item.type == 54:
                target_flg = True

        if UserFlow.objects.filter(user__shop=user.shop, user=user, flow_tab=target_flow_tab).exists():
            user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user, flow_tab=target_flow_tab).first()
            user_flow.flow = target_flow_tab.flow
            user_flow.flow_tab = target_flow_tab
            user_flow.flow_item = target_flow_item
            user_flow.name = target_flow_tab.name
            user_flow.richmenu = target_rich_menu
            user_flow.end_flg = False
            user_flow.updated_at = datetime.datetime.now()
            user_flow.save()
        else:
            delete_rich_menu(user)
            if target_rich_menu:
                UserRichMenu.objects.filter(user=user).all().delete()
                UserRichMenu.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    rich_menu = target_rich_menu
                )
                create_rich_menu(user)
            
            user_flow = UserFlow.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                user = user,
                number = UserFlow.objects.filter(user=user).count() + 1,
                flow = target_flow_tab.flow,
                flow_tab = target_flow_tab,
                flow_item = target_flow_item,
                name = target_flow_tab.name,
                richmenu = target_rich_menu,
                end_flg = False,
                updated_at = datetime.datetime.now(),
            )

        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(flow__user=user, number=0, temp_flg=True).all():
            if schedule.join != 2:
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
                                if manager_item.count <= 0 and schedule_item.manager:
                                    reception_manager_list.append(schedule_item.manager.id)
                        for facility_item in facility_list:
                            if facility_item == schedule_item.offline_facility:
                                facility_item.count = facility_item.count - 1
                                if facility_item.count <= 0:
                                    reception_facility_list.append(facility_item.id)
                    else:
                        if schedule_item and schedule_item.manager:
                            reception_manager_list.append(schedule_item.manager.id)
                        if schedule_item and schedule_item.offline_facility:
                            reception_facility_list.append(schedule_item.offline_facility.id)
                else:
                    if schedule_item and schedule_item.manager:
                        reception_manager_list.append(schedule_item.manager.id)
                    if schedule_item and schedule_item.offline_facility:
                        reception_facility_list.append(schedule_item.offline_facility.id)

        manager = None
        for manager_item in ReserveOfflineManagerMenu.objects.filter(shop=shop, offline=setting).order_by('manager__created_at').all():
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
        for facility_item in ReserveOfflineFacilityMenu.objects.filter(shop=shop, offline=setting).order_by('facility__order').all():
            if not facility_item.facility.id in reception_facility_list:
                facility = facility_item.facility
                break
            
        course = None
        if request.POST.get('course_id'):
            course = ReserveOfflineCourse.objects.filter(display_id=request.POST.get('course_id')).first()

        temp_schedule = UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).first()
        UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).all().delete()
        if UserFlowSchedule.objects.filter(flow=user_flow, join=0, temp_flg=False).exclude(number=0).exists():
            user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow, join=0, temp_flg=False).exclude(number=0).order_by('-number').first()
            user_flow_schedule.date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day')
            user_flow_schedule.time = request.POST.get('hour') + ':' + request.POST.get('minute')
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
                number = UserFlowSchedule.objects.filter(flow=user_flow, temp_flg=False).exclude(number=0).count() + 1,
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

        for offline in ShopOffline.objects.filter(shop=shop).order_by('created_at').all():
            for offline_setting in ReserveOfflineSetting.objects.filter(offline=offline).all():
                manager_list = list()
                facility_list = list()
                for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=offline_setting).all():
                    manager_list.append(manager_menu_item.manager)
                for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=offline_setting).order_by('facility__order').all():
                    facility_list.append(facility_menu_item.facility)

                for i in range(2):
                    if i == 1:
                        if temp_schedule and temp_schedule.date:
                            date = datetime.datetime(temp_schedule.date.year, temp_schedule.date.month, temp_schedule.date.day, temp_schedule.time.hour, temp_schedule.time.minute, 0)
                        else:
                            continue
                    if not date:
                        continue

                    if ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), offline=offline_setting).exists():
                        reserve_calendar_date = ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), offline=offline_setting).first()
                    else:
                        reserve_calendar_date = ReserveCalendarDate.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            offline = offline_setting,
                            date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                        )

                    for reception_offline_place in ReceptionOfflinePlace.objects.filter(offline=offline, reception_date__year=date.year, reception_date__month=date.month, reception_date__day=date.day).all():
                        reception_data = list()
                        reserve_calendar_date.flg = reception_offline_place.reception_flg
                        reserve_calendar_date.save()
                        if not reception_offline_place.reception_flg:
                            for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_from.hour, reception_offline_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_to.hour, reception_offline_place.reception_to.minute, 0), freq='15min'):
                                schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
                                    if schedule.join == 0 or schedule.join == 1:
                                        date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                                        temp_user = None
                                        end_flg = False
                                        if schedule.flow:
                                            end_flg = schedule.flow.end_flg
                                            temp_user = schedule.flow.user
                                        if schedule.offline:
                                            reception_data.append({
                                                'from': date,
                                                'to': date + datetime.timedelta(minutes=schedule.offline.time),
                                                'setting': schedule.offline,
                                                'course': schedule.offline_course,
                                                'facility': schedule.offline_facility,
                                                'manager': schedule.manager,
                                                'question': schedule.question,
                                                'meeting': None,
                                                'end_flg': end_flg,
                                                'temp_user': temp_user,
                                                'temp_manager': schedule.temp_manager,
                                                'temp_flg': schedule.temp_flg,
                                            })
                                        elif schedule.online:
                                            reception_data.append({
                                                'from': date,
                                                'to': date + datetime.timedelta(minutes=schedule.online.time),
                                                'setting': schedule.online,
                                                'course': schedule.online_course,
                                                'facility': schedule.online_facility,
                                                'manager': schedule.manager,
                                                'question': schedule.question,
                                                'meeting': None,
                                                'end_flg': end_flg,
                                                'temp_user': temp_user,
                                                'temp_manager': schedule.temp_manager,
                                                'temp_flg': schedule.temp_flg,
                                            })

                            for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_from.hour, reception_offline_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_offline_place.reception_to.hour, reception_offline_place.reception_to.minute, 0), freq=str(offline_setting.unit)+'min'):
                                schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                
                                reception_flg = True
                                reception_manager_list = list()
                                reception_facility_list = list()
                                temp_manager_list = list()
                                temp_user_list = list()
                                manager_count = len(manager_list)
                                facility_count = len(facility_list)
                                schedule_datetime = datetime.datetime(times.year, times.month, times.day, times.hour, times.minute, 0)
                                schedule_datetime = schedule_datetime + datetime.timedelta(minutes=offline_setting.time)
                                for manager_item in manager_list:
                                    reception_manager = ReceptionOfflineManager.objects.filter(offline=offline, manager=manager_item, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                                    if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager).exists():
                                        if ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=offline_setting).exists():
                                            reception_offline_manager_setting = ReceptionOfflineManagerSetting.objects.filter(manager=reception_manager, offline=offline_setting).first()
                                            if not reception_offline_manager_setting.flg:
                                                reception_manager = None
                                    if reception_manager:
                                        if len(reception_data) > 0 :
                                            people_number = 0
                                            people_count = offline_setting.people
                                            same_count = offline_setting.facility

                                            schedule_date = datetime.datetime(times.year, times.month, times.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                            schedule_add_date = schedule_date + datetime.timedelta(minutes=offline_setting.time)
                                            
                                            count_flg = True
                                            for reception in reception_data:
                                                if schedule_add_date > reception['from'] and reception['to'] > schedule_date:
                                                    if manager_count <= 0 or facility_count <= 0:
                                                        break
                                                    else:
                                                        if reception['setting']:
                                                            if reception['setting'].id == offline_setting.id:
                                                                if schedule_date == reception['from']:
                                                                    if count_flg:
                                                                        if reception['facility'] and reception['facility'].count < people_count:
                                                                            same_count = same_count - 1
                                                                            if same_count == 0:
                                                                                if people_count > reception['facility'].count:
                                                                                    people_count = reception['facility'].count
                                                                            else:
                                                                                people_total_count = reception['facility'].count
                                                                                while same_count > 0:
                                                                                    people_number = people_number + 1
                                                                                    people_total_count = people_total_count + facility_list[people_number].count
                                                                                    if facility_list[people_number] and not facility_list[people_number] in reception_facility_list:
                                                                                        facility_count = facility_count - 1
                                                                                        reception_facility_list.append(facility_list[people_number])
                                                                                    same_count = same_count - 1
                                                                                if people_count > people_total_count:
                                                                                    people_count = people_total_count
                                                                        count_flg = False
                                                                    people_count = people_count - 1
                                                                    if people_count <= 0:
                                                                        if reception['manager'] and not reception['manager'] in reception_manager_list:
                                                                            manager_count = manager_count - 1
                                                                            reception_manager_list.append(reception['manager'])
                                                                        if reception['facility'] and not reception['facility'] in reception_facility_list:
                                                                            facility_count = facility_count - 1
                                                                            reception_facility_list.append(reception['facility'])

                                                                        people_number = people_number + 1
                                                                        people_count = offline_setting.people
                                                                        if facility_count > 0 and facility_list[people_number].count < people_count:
                                                                            people_count = facility_list[people_number].count
                                                                else:
                                                                    if reception['manager'] and not reception['manager'] in reception_manager_list:
                                                                        manager_count = manager_count - 1
                                                                        reception_manager_list.append(reception['manager'])
                                                                    if reception['facility'] and not reception['facility'] in reception_facility_list:
                                                                        facility_count = facility_count - 1
                                                                        reception_facility_list.append(reception['facility'])
                                                            else:
                                                                if reception['manager'] and not reception['manager'] in reception_manager_list:
                                                                    manager_count = manager_count - 1
                                                                    reception_manager_list.append(reception['manager'])
                                                                if reception['facility'] and not reception['facility'] in reception_facility_list:
                                                                    facility_count = facility_count - 1
                                                                    reception_facility_list.append(reception['facility'])
                                                    if reception['temp_flg']:
                                                        if reception['temp_manager']:
                                                            temp_manager_list.append(reception['temp_manager'])
                                                        else:
                                                            temp_user_list.append(reception['temp_user'])
                                            if manager_count > 0 and facility_count > 0:
                                                reception_flg = False
                                        else:
                                            schedule_date = datetime.datetime(date.year, date.month, date.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                            if manager_count > 0 and facility_count > 0:
                                                reception_flg = False
                                    else:
                                        if not manager_item in reception_manager_list:
                                            manager_count = manager_count - 1
                                            reception_manager_list.append(manager_item)
                                if manager_count <= 0 or facility_count <= 0:
                                    reception_flg = True
                                
                                if reception_flg:
                                    if ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).exists():
                                        reserve_calendar_time = ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).first()
                                        reserve_calendar_time.count = 0
                                        reserve_calendar_time.save()
                                    else:
                                        reserve_calendar_time = ReserveCalendarTime.objects.create(
                                            id = str(uuid.uuid4()),
                                            calendar = reserve_calendar_date,
                                            time = schedule_time,
                                            count = 0,
                                        )
                                else:
                                    if manager_count < facility_count:
                                        if ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).exists():
                                            reserve_calendar_time = ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).first()
                                            reserve_calendar_time.count = manager_count
                                            reserve_calendar_time.save()
                                        else:
                                            reserve_calendar_time = ReserveCalendarTime.objects.create(
                                                id = str(uuid.uuid4()),
                                                calendar = reserve_calendar_date,
                                                time = schedule_time,
                                                count = manager_count,
                                            )
                                    else:
                                        if ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).exists():
                                            reserve_calendar_time = ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).first()
                                            reserve_calendar_time.count = facility_count
                                            reserve_calendar_time.save()
                                        else:
                                            reserve_calendar_time = ReserveCalendarTime.objects.create(
                                                id = str(uuid.uuid4()),
                                                calendar = reserve_calendar_date,
                                                time = schedule_time,
                                                count = facility_count,
                                            )
                                ReserveTempCalendar.objects.filter(calendar=reserve_calendar_time).all().delete()
                                for temp_manager in temp_manager_list:
                                    ReserveTempCalendar.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_time,
                                        user = None,
                                        manager = temp_manager,
                                    )
                                for temp_user in temp_user_list:
                                    ReserveTempCalendar.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_time,
                                        user = temp_user,
                                        manager = None,
                                    )
        
        for reserve_offline_setting in ReserveOfflineSetting.objects.filter(offline__shop=shop).order_by('number').all():
            if reserve_offline_setting.advance and int(reserve_offline_setting.advance) == setting.display_id:
                ReserveUserStartDate.objects.filter(user=user, offline=reserve_offline_setting).all().delete()
                ReserveUserStartDate.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    offline = reserve_offline_setting,
                    date = add_date,
                )

    if ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).exists():
        user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user).first()
        setting = ReserveOnlineSetting.objects.filter(display_id=request.POST.get('setting_id')).first()
        for menu in ReserveOnlineFlowMenu.objects.filter(shop=shop, online=setting).all():
            flow_tab = ShopFlowTab.objects.filter(flow=user_flow.flow, flow__shop=shop, name=menu.flow).first()
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
        
        target_flg = False
        target_flow_item = None
        target_rich_menu = None
        for flow_item in ShopFlowItem.objects.filter(flow_tab=target_flow_tab).all():
            if flow_item.type == 7:
                target_rich_menu = ShopFlowRichMenu.objects.filter(flow=flow_item).first()
                target_rich_menu = target_rich_menu.rich_menu
            if target_flg:
                target_flow_item = flow_item
                break
            if flow_item.type == 54:
                target_flg = True
        
        if UserFlow.objects.filter(user__shop=user.shop, user=user, flow_tab=target_flow_tab).exists():
            user_flow = UserFlow.objects.filter(user__shop=user.shop, user=user, flow_tab=target_flow_tab).first()
            user_flow.flow = target_flow_tab.flow
            user_flow.flow_tab = target_flow_tab
            user_flow.flow_item = target_flow_item
            user_flow.name = target_flow_tab.name
            user_flow.richmenu = target_rich_menu
            user_flow.end_flg = False
            user_flow.updated_at = datetime.datetime.now()
            user_flow.save()
        else:
            user_flow = UserFlow.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                user = user,
                number = UserFlow.objects.filter(user=user).count() + 1,
                flow = target_flow_tab.flow,
                flow_tab = target_flow_tab,
                flow_item = target_flow_item,
                name = target_flow_tab.name,
                richmenu = target_rich_menu,
                end_flg = False,
                updated_at = datetime.datetime.now(),
            )

        schedule_list = list()
        for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(flow__user=user, number=0, temp_flg=True).all():
            if schedule.join != 2:
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
                                if manager_item.count <= 0 and schedule_item.manager:
                                    reception_manager_list.append(schedule_item.manager.id)
                        for facility_item in facility_list:
                            if facility_item == schedule_item.online_facility:
                                facility_item.count = facility_item.count - 1
                                if facility_item.count <= 0:
                                    reception_facility_list.append(facility_item.id)
                    else:
                        if schedule_item and schedule_item.manager:
                            reception_manager_list.append(schedule_item.manager.id)
                        if schedule_item and schedule_item.offline_facility:
                            reception_facility_list.append(schedule_item.offline_facility.id)
                else:
                    if schedule_item and schedule_item.manager:
                        reception_manager_list.append(schedule_item.manager.id)
                    if schedule_item and schedule_item.offline_facility:
                        reception_facility_list.append(schedule_item.offline_facility.id)

        manager = None
        for manager_item in ReserveOnlineManagerMenu.objects.filter(shop=shop, online=setting).order_by('manager__created_at').all():
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
        for facility_item in ReserveOnlineFacilityMenu.objects.filter(shop=shop, online=setting).all():
            if not facility_item.facility in reception_facility_list:
                facility = facility_item.facility
                break
        
        course = None
        if request.POST.get('course_id'):
            course = ReserveOnlineCourse.objects.filter(display_id=request.POST.get('course_id')).first()

        temp_schedule = UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).first()
        UserFlowSchedule.objects.filter(flow=user_flow, number=0, temp_flg=True).all().delete()
        if UserFlowSchedule.objects.filter(flow=user_flow, join=0, temp_flg=False).exclude(number=0).exists():
            user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow, join=0, temp_flg=False).exclude(number=0).order_by('-number').first()
            user_flow_schedule.date = request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day')
            user_flow_schedule.date = request.POST.get('hour') + ':' + request.POST.get('minute')
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
                number = UserFlowSchedule.objects.filter(flow=user_flow, temp_flg=False).exclude(number=0).count() + 1,
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
        
        for online in ShopOnline.objects.filter(shop=shop).order_by('created_at').all():
            for online_setting in ReserveOnlineSetting.objects.filter(online=online).all():
                manager_list = list()
                facility_list = list()
                for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=online_setting).all():
                    manager_list.append(manager_menu_item.manager)
                for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=online_setting).order_by('facility__order').all():
                    facility_list.append(facility_menu_item.facility)

                for i in range(2):
                    if i == 1:
                        if temp_schedule and temp_schedule.date:
                            date = datetime.datetime(temp_schedule.date.year, temp_schedule.date.month, temp_schedule.date.day, temp_schedule.time.hour, temp_schedule.time.minute, 0)
                        else:
                            continue
                    if not date:
                        continue

                    if ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), online=online_setting).exists():
                        reserve_calendar_date = ReserveCalendarDate.objects.filter(date=datetime.datetime(date.year, date.month, date.day, 0, 0, 0), online=online_setting).first()
                    else:
                        reserve_calendar_date = ReserveCalendarDate.objects.create(
                            id = str(uuid.uuid4()),
                            shop = shop,
                            online = online_setting,
                            date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0),
                        )

                    for reception_online_place in ReceptionOnlinePlace.objects.filter(online=online, reception_date__year=date.year, reception_date__month=date.month, reception_date__day=date.day).all():
                        reception_data = list()
                        reserve_calendar_date.flg = reception_online_place.reception_flg
                        reserve_calendar_date.save()
                        if not reception_online_place.reception_flg:
                            for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_from.hour, reception_online_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_to.hour, reception_online_place.reception_to.minute, 0), freq='15min'):
                                schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                for schedule in UserFlowSchedule.objects.filter(Q(Q(flow__user__shop=shop)|Q(temp_manager__shop=shop)|Q(temp_manager__head_flg=True)|Q(temp_manager__company_flg=True)), date__year=date.year, date__month=date.month, date__day=date.day, time__hour=schedule_time[:schedule_time.find(':')], time__minute=schedule_time[schedule_time.find(':')+1:]).all():
                                    if schedule.join == 0 or schedule.join == 1:
                                        date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                                        temp_user = None
                                        end_flg = False
                                        if schedule.flow:
                                            end_flg = schedule.flow.end_flg
                                            temp_user = schedule.flow.user
                                        if schedule.online:
                                            reception_data.append({
                                                'from': date,
                                                'to': date + datetime.timedelta(minutes=schedule.online.time),
                                                'setting': schedule.online,
                                                'course': schedule.online_course,
                                                'facility': schedule.online_facility,
                                                'manager': schedule.manager,
                                                'question': schedule.question,
                                                'meeting': None,
                                                'end_flg': end_flg,
                                                'temp_user': temp_user,
                                                'temp_manager': schedule.temp_manager,
                                                'temp_flg': schedule.temp_flg,
                                            })
                                        elif schedule.online:
                                            reception_data.append({
                                                'from': date,
                                                'to': date + datetime.timedelta(minutes=schedule.online.time),
                                                'setting': schedule.online,
                                                'course': schedule.online_course,
                                                'facility': schedule.online_facility,
                                                'manager': schedule.manager,
                                                'question': schedule.question,
                                                'meeting': None,
                                                'end_flg': end_flg,
                                                'temp_user': temp_user,
                                                'temp_manager': schedule.temp_manager,
                                                'temp_flg': schedule.temp_flg,
                                            })

                            for times in pandas.date_range(start=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_from.hour, reception_online_place.reception_from.minute, 0), end=datetime.datetime(date.year, date.month, date.day, reception_online_place.reception_to.hour, reception_online_place.reception_to.minute, 0), freq=str(online_setting.unit)+'min'):
                                schedule_time = str(times.hour)+':'+str(times.minute).ljust(2, '0')
                                
                                reception_flg = True
                                reception_manager_list = list()
                                reception_facility_list = list()
                                temp_manager_list = list()
                                temp_user_list = list()
                                manager_count = len(manager_list)
                                facility_count = len(facility_list)
                                schedule_datetime = datetime.datetime(times.year, times.month, times.day, times.hour, times.minute, 0)
                                schedule_datetime = schedule_datetime + datetime.timedelta(minutes=online_setting.time)
                                for manager_item in manager_list:
                                    reception_manager = ReceptionOnlineManager.objects.filter(online=online, manager=manager_item, reception_date__year=schedule_datetime.year, reception_date__month=schedule_datetime.month, reception_date__day=schedule_datetime.day, reception_from__lte=schedule_time, reception_to__gte=schedule_datetime.time(), reception_flg=True).first()
                                    if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager).exists():
                                        if ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=online_setting).exists():
                                            reception_online_manager_setting = ReceptionOnlineManagerSetting.objects.filter(manager=reception_manager, online=online_setting).first()
                                            if not reception_online_manager_setting.flg:
                                                reception_manager = None
                                    if reception_manager:
                                        if len(reception_data) > 0 :
                                            people_number = 0
                                            people_count = online_setting.people
                                            same_count = online_setting.facility

                                            schedule_date = datetime.datetime(times.year, times.month, times.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                            schedule_add_date = schedule_date + datetime.timedelta(minutes=online_setting.time)
                                            
                                            count_flg = True
                                            for reception in reception_data:
                                                if schedule_add_date > reception['from'] and reception['to'] > schedule_date:
                                                    if manager_count <= 0 or facility_count <= 0:
                                                        break
                                                    else:
                                                        if reception['setting']:
                                                            if reception['setting'].id == online_setting.id:
                                                                if schedule_date == reception['from']:
                                                                    if count_flg:
                                                                        if reception['facility'] and reception['facility'].count < people_count:
                                                                            same_count = same_count - 1
                                                                            if same_count == 0:
                                                                                if people_count > reception['facility'].count:
                                                                                    people_count = reception['facility'].count
                                                                            else:
                                                                                people_total_count = reception['facility'].count
                                                                                while same_count > 0:
                                                                                    people_number = people_number + 1
                                                                                    people_total_count = people_total_count + facility_list[people_number].count
                                                                                    if facility_list[people_number] and not facility_list[people_number] in reception_facility_list:
                                                                                        facility_count = facility_count - 1
                                                                                        reception_facility_list.append(facility_list[people_number])
                                                                                    same_count = same_count - 1
                                                                                if people_count > people_total_count:
                                                                                    people_count = people_total_count
                                                                        count_flg = False
                                                                    people_count = people_count - 1
                                                                    if people_count <= 0:
                                                                        if reception['manager'] and not reception['manager'] in reception_manager_list:
                                                                            manager_count = manager_count - 1
                                                                            reception_manager_list.append(reception['manager'])
                                                                        if reception['facility'] and not reception['facility'] in reception_facility_list:
                                                                            facility_count = facility_count - 1
                                                                            reception_facility_list.append(reception['facility'])

                                                                        people_number = people_number + 1
                                                                        people_count = online_setting.people
                                                                        if facility_count > 0 and facility_list[people_number].count < people_count:
                                                                            people_count = facility_list[people_number].count
                                                                else:
                                                                    if reception['manager'] and not reception['manager'] in reception_manager_list:
                                                                        manager_count = manager_count - 1
                                                                        reception_manager_list.append(reception['manager'])
                                                                    if reception['facility'] and not reception['facility'] in reception_facility_list:
                                                                        facility_count = facility_count - 1
                                                                        reception_facility_list.append(reception['facility'])
                                                            else:
                                                                if reception['manager'] and not reception['manager'] in reception_manager_list:
                                                                    manager_count = manager_count - 1
                                                                    reception_manager_list.append(reception['manager'])
                                                                if reception['facility'] and not reception['facility'] in reception_facility_list:
                                                                    facility_count = facility_count - 1
                                                                    reception_facility_list.append(reception['facility'])
                                                    if reception['temp_flg']:
                                                        if reception['temp_manager']:
                                                            temp_manager_list.append(reception['temp_manager'])
                                                        else:
                                                            temp_user_list.append(reception['temp_user'])
                                            if manager_count > 0 and facility_count > 0:
                                                reception_flg = False
                                        else:
                                            schedule_date = datetime.datetime(date.year, date.month, date.day, int(schedule_time[:schedule_time.find(':')]), int(schedule_time[schedule_time.find(':')+1:]), 0)
                                            if manager_count > 0 and facility_count > 0:
                                                reception_flg = False
                                    else:
                                        if not manager_item in reception_manager_list:
                                            manager_count = manager_count - 1
                                            reception_manager_list.append(manager_item)
                                if manager_count <= 0 or facility_count <= 0:
                                    reception_flg = True
                                
                                if reception_flg:
                                    if ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).exists():
                                        reserve_calendar_time = ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).first()
                                        reserve_calendar_time.count = 0
                                        reserve_calendar_time.save()
                                    else:
                                        reserve_calendar_time = ReserveCalendarTime.objects.create(
                                            id = str(uuid.uuid4()),
                                            calendar = reserve_calendar_date,
                                            time = schedule_time,
                                            count = 0,
                                        )
                                else:
                                    if manager_count < facility_count:
                                        if ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).exists():
                                            reserve_calendar_time = ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).first()
                                            reserve_calendar_time.count = manager_count
                                            reserve_calendar_time.save()
                                        else:
                                            reserve_calendar_time = ReserveCalendarTime.objects.create(
                                                id = str(uuid.uuid4()),
                                                calendar = reserve_calendar_date,
                                                time = schedule_time,
                                                count = manager_count,
                                            )
                                    else:
                                        if ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).exists():
                                            reserve_calendar_time = ReserveCalendarTime.objects.filter(calendar=reserve_calendar_date, time=schedule_time).first()
                                            reserve_calendar_time.count = facility_count
                                            reserve_calendar_time.save()
                                        else:
                                            reserve_calendar_time = ReserveCalendarTime.objects.create(
                                                id = str(uuid.uuid4()),
                                                calendar = reserve_calendar_date,
                                                time = schedule_time,
                                                count = facility_count,
                                            )
                                ReserveTempCalendar.objects.filter(calendar=reserve_calendar_time).all().delete()
                                for temp_manager in temp_manager_list:
                                    ReserveTempCalendar.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_time,
                                        user = None,
                                        manager = temp_manager,
                                    )
                                for temp_user in temp_user_list:
                                    ReserveTempCalendar.objects.create(
                                        id = str(uuid.uuid4()),
                                        calendar = reserve_calendar_time,
                                        user = temp_user,
                                        manager = None,
                                    )
        
        for reserve_online_setting in ReserveOnlineSetting.objects.filter(online__shop=shop).order_by('number').all():
            if reserve_online_setting.advance and int(reserve_online_setting.advance) == setting.display_id:
                ReserveUserStartDate.objects.filter(user=user, online=reserve_online_setting).all().delete()
                ReserveUserStartDate.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    online = reserve_online_setting,
                    date = add_date,
                )

    user_flow = UserFlow.objects.filter(user=user, flow_tab=target_flow_tab).first()
    for flow_item in ShopFlowItem.objects.filter(flow_tab=user_flow.flow_tab, x__gte=user_flow.flow_item.x, y__gte=user_flow.flow_item.y).order_by('y', 'x').all():
        if go(user, user_flow.flow, user_flow.flow_tab, flow_item):
            break
    return JsonResponse( {'error': False}, safe=False )