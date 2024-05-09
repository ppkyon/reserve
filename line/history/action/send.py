from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from PIL import Image

from flow.models import ShopFlowItem, ShopFlowTemplate, ShopFlowActionReminder, UserFlow, UserFlowSchedule, UserFlowActionReminder
from question.models import UserQuestion, UserQuestionItem, UserQuestionItemChoice
from reserve.models import ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu

from common import create_code
from line.action.message import push_card_type_message

from sign.models import AuthShop
from user.models import LineUser, UserProfile

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
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()

    user_flow = UserFlow.objects.filter(display_id=request.POST.get('flow_id')).first()
    user_flow_schedule = UserFlowSchedule.objects.filter(display_id=request.POST.get('schedule_id')).first()
    if user_flow_schedule:
        user_flow_schedule.join = 2
        user_flow_schedule.save()

        if user_flow_schedule.offline:
            people_count = user_flow_schedule.offline.people
            manager_list = list()
            facility_list = list()
            if user_flow_schedule.offline:
                for manager_menu_item in ReserveOfflineManagerMenu.objects.filter(offline=user_flow_schedule.offline).all():
                    manager_menu_item.manager.count = people_count
                    manager_list.append(manager_menu_item.manager)
                for facility_menu_item in ReserveOfflineFacilityMenu.objects.filter(offline=user_flow_schedule.offline).order_by('facility__order').all():
                    facility_list.append(facility_menu_item.facility)

            schedule_list = list()
            for schedule in UserFlowSchedule.objects.filter(flow__user__shop=shop, date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(join=2).all():
                schedule_list.append(schedule)

            date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
            add_date = date + datetime.timedelta(minutes=user_flow_schedule.offline.time)

            reception_manager_list = list()
            reception_facility_list = list()
            for schedule_item in schedule_list:
                schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
                schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.offline.time)

                if add_date > schedule_date and schedule_add_date > date:
                    if schedule_item.offline == user_flow_schedule.offline:
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
                            reception_manager_list.append(schedule_item.manager)
                            reception_facility_list.append(schedule_item.offline_facility)
                    else:
                        reception_manager_list.append(schedule_item.manager)
                        reception_facility_list.append(schedule_item.offline_facility)

            manager = None
            for manager_item in ReserveOfflineManagerMenu.objects.filter(shop=shop, offline=user_flow_schedule.offline).order_by('-manager__created_at').all():
                if not manager_item.manager.id in reception_manager_list:
                    manager = manager_item.manager
                    break
            facility = None
            for facility_item in ReserveOfflineFacilityMenu.objects.filter(shop=shop, offline=user_flow_schedule.offline).order_by('facility__order').all():
                if not facility_item.facility.id in reception_facility_list:
                    facility = facility_item.facility
                    break

            user_flow_schedule = UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlowSchedule),
                flow = user_flow,
                number = UserFlowSchedule.objects.filter(flow=user_flow).count() + 1,
                date = datetime.datetime.strptime(request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day') + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                time = datetime.datetime.strptime(request.POST.get('hour') + ':' + request.POST.get('minute') + ':00', '%H:%M:%S'),
                join = 0,
                offline = user_flow_schedule.offline,
                offline_course = user_flow_schedule.offline_course,
                offline_facility = facility,
                manager = manager,
                question = user_flow_schedule.question,
                check_flg = False
            )
        if user_flow_schedule.online:
            people_count = user_flow_schedule.online.people
            manager_list = list()
            facility_list = list()
            if user_flow_schedule.online:
                for manager_menu_item in ReserveOnlineManagerMenu.objects.filter(online=user_flow_schedule.online).all():
                    manager_menu_item.manager.count = people_count
                    manager_list.append(manager_menu_item.manager)
                for facility_menu_item in ReserveOnlineFacilityMenu.objects.filter(online=user_flow_schedule.online).order_by('facility__order').all():
                    facility_list.append(facility_menu_item.facility)

            schedule_list = list()
            for schedule in UserFlowSchedule.objects.filter(flow__user__shop=shop, date__year=request.POST.get('year'), date__month=request.POST.get('month'), date__day=request.POST.get('day')).exclude(join=2).all():
                schedule_list.append(schedule)

            date = datetime.datetime(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day')), int(request.POST.get('hour')), int(request.POST.get('minute')), 0)
            add_date = date + datetime.timedelta(minutes=user_flow_schedule.online.time)

            reception_manager_list = list()
            reception_facility_list = list()
            for schedule_item in schedule_list:
                schedule_date = datetime.datetime(schedule_item.date.year, schedule_item.date.month, schedule_item.date.day, schedule_item.time.hour, schedule_item.time.minute, 0)
                schedule_add_date = schedule_date + datetime.timedelta(minutes=schedule.online.time)

                if add_date > schedule_date and schedule_add_date > date:
                    if schedule_item.online == user_flow_schedule.online:
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
                            reception_manager_list.append(schedule_item.manager)
                            reception_facility_list.append(schedule_item.online_facility)
                    else:
                        reception_manager_list.append(schedule_item.manager)
                        reception_facility_list.append(schedule_item.online_facility)

            manager = None
            for manager_item in ReserveOnlineManagerMenu.objects.filter(shop=shop, online=schedule.online).order_by('-manager__created_at').all():
                if not manager_item.manager.id in reception_manager_list:
                    manager = manager_item.manager
                    break
            facility = None
            for facility_item in ReserveOnlineFacilityMenu.objects.filter(shop=shop, online=schedule.online).order_by('facility__order').all():
                if not facility_item.facility.id in reception_facility_list:
                    facility = facility_item.facility
                    break

            user_flow_schedule = UserFlowSchedule.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlowSchedule),
                flow = user_flow,
                number = UserFlowSchedule.objects.filter(flow=user_flow).count() + 1,
                date = datetime.datetime.strptime(request.POST.get('year') + '-' + request.POST.get('month') + '-' + request.POST.get('day') + ' 00:00:00', '%Y-%m-%d %H:%M:%S'),
                time = datetime.datetime.strptime(request.POST.get('hour') + ':' + request.POST.get('minute') + ':00', '%H:%M:%S'),
                join = 0,
                online = user_flow_schedule.online,
                online_course = user_flow_schedule.online_course,
                online_facility = facility,
                manager = manager,
                question = user_flow_schedule.question,
                check_flg = False
            )
            
    target_flow_item = None
    action_flow_item = None
    flow_flg = False
    action_flg = False
    for flow_item in ShopFlowItem.objects.filter(flow_tab=user_flow.flow_tab).order_by('y', 'x').all():
        if flow_flg:
            if action_flg:
                action_flow_item = flow_item
                break
            if flow_item.type == 6:
                flow_template = ShopFlowTemplate.objects.filter(flow=flow_item).first()
                push_card_type_message(user_flow.user, flow_template.template_cardtype, None)
            if flow_item.type == 51:
                target_flow_item = flow_item
                action_flg = True
        if flow_item.type == 54:
            flow_flg = True
    
    user_flow.flow_item = target_flow_item
    user_flow.save()
    
    shop_flow_action_reminder = ShopFlowActionReminder.objects.filter(flow=action_flow_item).first()
    action_date = datetime.datetime(user_flow_schedule.date.year, user_flow_schedule.date.month, user_flow_schedule.date.day, user_flow_schedule.time.hour, user_flow_schedule.time.minute, 0)
    action_date = action_date - datetime.timedelta(shop_flow_action_reminder.date)
    action_date = datetime.datetime(action_date.year, action_date.month, action_date.day, shop_flow_action_reminder.time, 0, 0)
    if UserFlowActionReminder.objects.filter(user=user_flow.user, flow=user_flow).exists():
        user_flow_action_reminder = UserFlowActionReminder.objects.filter(user=user_flow.user, flow=user_flow).first()
        user_flow_action_reminder.action_date = action_date
        user_flow_action_reminder.save()
    else:
        UserFlowActionReminder.objects.create(
            id = str(uuid.uuid4()),
            user = user_flow.user,
            flow = user_flow,
            template_text = shop_flow_action_reminder.template_text,
            template_video = shop_flow_action_reminder.template_video,
            template_richmessage = shop_flow_action_reminder.template_richmessage,
            template_richvideo = shop_flow_action_reminder.template_richvideo,
            template_cardtype = shop_flow_action_reminder.template_cardtype,
            action_date = action_date,
        )
    return JsonResponse( {}, safe=False )

def question(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('shop_id')).first()
    user = LineUser.objects.filter(line_user_id=request.POST.get('user_id'), shop=shop).first()

    if UserProfile.objects.filter(user=user).exists():
        user_profile = UserProfile.objects.filter(user=user).first()
    else:
        user_profile = UserProfile.objects.create(
            id = str(uuid.uuid4()),
            user = user,
        )
    user.updated_at = datetime.datetime.now()
    user.save()

    user_question = UserQuestion.objects.filter(display_id=request.POST.get('question_id')).first()
    for user_question_index, user_question_item in enumerate(UserQuestionItem.objects.filter(question=user_question).order_by('number').all()):
        if request.POST.get('type_'+str(user_question_index+1)) == '1':
            if request.POST.get('text_'+str(user_question_index+1)):
                user_question_item.text = urllib.parse.unquote(request.POST.get('text_'+str(user_question_index+1)))
                user_question_item.save()
                user_profile.name = urllib.parse.unquote(request.POST.get('text_'+str(user_question_index+1)))
                user_profile.save()
            else:
                user_question_item.text = None
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '2':
            if request.POST.get('text_'+str(user_question_index+1)):
                user_question_item.text = urllib.parse.unquote(request.POST.get('text_'+str(user_question_index+1)))
                user_question_item.save()
                user_profile.name_kana = urllib.parse.unquote(request.POST.get('text_'+str(user_question_index+1)))
                user_profile.save()
            else:
                user_question_item.text = None
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '3':
            if request.POST.get('value_'+str(user_question_index+1)):
                user_question_item.value = urllib.parse.unquote(request.POST.get('value_'+str(user_question_index+1))).replace('歳', '')
                user_question_item.save()
                user_profile.age = urllib.parse.unquote(request.POST.get('value_'+str(user_question_index+1))).replace('歳', '')
                user_profile.save()
            else:
                user_question_item.value = 0
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '4':
            if request.POST.get('value_'+str(user_question_index+1)):
                if request.POST.get('value_'+str(user_question_index+1)):
                    user_question_item.value = 0
                    user_question_item.save()
                elif urllib.parse.unquote(request.POST.get('value_'+str(user_question_index+1))) == '男性':
                    user_question_item.value = 1
                    user_question_item.save()
                    user_profile.sex = 1
                elif urllib.parse.unquote(request.POST.get('value_'+str(user_question_index+1))) == '女性':
                    user_question_item.value = 2
                    user_question_item.save()
                    user_profile.sex = 2
                user_profile.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '5':
            if request.POST.get('text_'+str(user_question_index+1)):
                user_question_item.text = urllib.parse.unquote(request.POST.get('text_'+str(user_question_index+1))).replace( '-', '')
                user_question_item.save()
                user_profile.phone_number = urllib.parse.unquote(request.POST.get('text_'+str(user_question_index+1))).replace( '-', '')
                user_profile.save()
            else:
                user_question_item.text = None
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '6':
            if request.POST.get('email_'+str(user_question_index+1)):
                user_question_item.email = urllib.parse.unquote(request.POST.get('email_'+str(user_question_index+1)))
                user_question_item.save()
                user_profile.email = urllib.parse.unquote(request.POST.get('email_'+str(user_question_index+1)))
                user_profile.save()
            else:
                user_question_item.email = None
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '7':
            if request.POST.get('date_'+str(user_question_index+1)):
                user_question_item.date = urllib.parse.unquote(request.POST.get('date_'+str(user_question_index+1))).replace( '/', '-')
                user_question_item.save()
                today = datetime.date.today()
                birthday = datetime.datetime.strptime(urllib.parse.unquote(request.POST.get('date_'+str(user_question_index+1))).replace( '/', '-'), '%Y-%m-%d')
                user_profile.age = (int(today.strftime("%Y%m%d")) - int(birthday.strftime("%Y%m%d"))) // 10000
                user_profile.birth = urllib.parse.unquote(request.POST.get('date_'+str(user_question_index+1))).replace( '/', '-')
                user_profile.save()
            else:
                user_question_item.date = None
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '8':
            if request.POST.get('text_'+str(user_question_index+1)):
                user_question_item.text = urllib.parse.unquote(request.POST.get('text_'+str(user_question_index+1)))
                user_question_item.save()
                user_profile.address = urllib.parse.unquote(request.POST.get('text_'+str(user_question_index+1)))
                user_profile.save()
            else:
                user_question_item.text = None
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '9':
            if request.POST.get('image_'+str(user_question_index+1)):
                if ';base64,' in request.POST.get('image_'+str(user_question_index+1)):
                    format, imgstr = request.POST.get('image_'+str(user_question_index+1)).split(';base64,') 
                    ext = format.split('/')[-1]
                    data = ContentFile(base64.b64decode(request.POST.get('image_url_'+str(user_question_index+1)).replace( ' ', '+' )), name='temp.' + ext)
                else:
                    data = request.POST.get('image_url_'+str(user_question_index+1))
                user_question_item.image = data
                user_question_item.save()
                user_profile.image = data
                user_profile.save()
            else:
                user_question_item.image = None
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '10':
            if request.POST.get('image_'+str(user_question_index+1)):
                if ';base64,' in request.POST.get('image_'+str(user_question_index+1)):
                    format, imgstr = request.POST.get('image_'+str(user_question_index+1)).split(';base64,') 
                    ext = format.split('/')[-1]
                    data = ContentFile(base64.b64decode(request.POST.get('image_url_'+str(user_question_index+1)).replace( ' ', '+' )), name='temp.' + ext)
                else:
                    data = request.POST.get('image_url_'+str(user_question_index+1))
                user_question_item.image = data
                user_question_item.save()
            else:
                user_question_item.image = None
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '11':
            if request.POST.get('video_'+str(user_question_index+1)):
                if ';base64,' in request.POST.get('video_'+str(user_question_index+1)):
                    format, imgstr = request.POST.get('video_'+str(user_question_index+1)).split(';base64,') 
                    ext = format.split('/')[-1] 
                    data = ContentFile(base64.b64decode(request.POST.get('video_'+str(user_question_index+1)).replace( ' ', '+' )), name='temp.' + ext)
                else:
                    data = request.POST.get('video_url_'+str(user_question_index+1))
                user_question_item.video = data
                user_question_item.video_thumbnail = None
                user_question_item.save()

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
                user_question_item.video = None
                user_question_item.video_thumbnail = None
                user_question_item.save()
        elif request.POST.get('type_'+str(user_question_index+1)) == '99':
            if request.POST.get('choice_type_'+str(user_question_index+1)) == '1':
                for user_question_choice_index, user_question_choice_item in enumerate(UserQuestionItemChoice.objects.filter(question=user_question_item).order_by('number').all()):
                    if request.POST.get('text_'+str(user_question_index+1)+'_'+str(user_question_choice_index+1)):
                        user_question_choice_item.text = urllib.parse.unquote(request.POST.get('text_'+str(user_question_index+1)+'_'+str(user_question_choice_index+1)))
                        user_question_choice_item.save()
                    else:
                        user_question_choice_item.text = None
                        user_question_choice_item.save()
            elif request.POST.get('choice_type_'+str(user_question_index+1)) == '2':
                for user_question_choice_index, user_question_choice_item in enumerate(UserQuestionItemChoice.objects.filter(question=user_question_item).order_by('number').all()):
                    if request.POST.get('choice_value_'+str(user_question_index+1)) == str(user_question_choice_item.number):
                        user_question_choice_item.text = 1
                        user_question_choice_item.save()
                    else:
                        user_question_choice_item.text = 0
                        user_question_choice_item.save()
            elif request.POST.get('choice_type_'+str(user_question_index+1)) == '3':
                choice_value = request.POST.getlist('choice_value_'+str(user_question_index+1)+'%5B%5D')
                for user_question_choice_index, user_question_choice_item in enumerate(UserQuestionItemChoice.objects.filter(question=user_question_item).order_by('number').all()):
                    if str(user_question_choice_item.number) in choice_value:
                        user_question_choice_item.text = 1
                        user_question_choice_item.save()
                    else:
                        user_question_choice_item.text = 0
                        user_question_choice_item.save()
            elif request.POST.get('choice_type_'+str(user_question_index+1)) == '4':
                for user_question_choice_index, user_question_choice_item in enumerate(UserQuestionItemChoice.objects.filter(question=user_question_item).order_by('number').all()):
                    if request.POST.get('choice_text_'+str(user_question_index+1)) == user_question_choice_item.text:
                        user_question_choice_item.text = 1
                        user_question_choice_item.save()
                    else:
                        user_question_choice_item.text = 0
                        user_question_choice_item.save()
            elif request.POST.get('choice_type_'+str(user_question_index+1)) == '5':
                for user_question_choice_index, user_question_choice_item in enumerate(UserQuestionItemChoice.objects.filter(question=user_question_item).order_by('number').all()):
                    if request.POST.get('date_'+str(user_question_index+1)+'_'+str(user_question_choice_index+1)):
                        user_question_choice_item.date = urllib.parse.unquote(request.POST.get('date_'+str(user_question_index+1)+'_'+str(user_question_choice_index+1))).replace( '/', '-')
                        user_question_choice_item.save()
                    else:
                        user_question_choice_item.date = None
                        user_question_choice_item.save()
            elif request.POST.get('choice_type_'+str(user_question_index+1)) == '6':
                for user_question_choice_index, user_question_choice_item in enumerate(UserQuestionItemChoice.objects.filter(question=user_question_item).order_by('number').all()):
                    if request.POST.get('time_'+str(user_question_index+1)+'_'+str(user_question_choice_index+1)):
                        user_question_choice_item.time = urllib.parse.unquote(request.POST.get('time_'+str(user_question_index+1)+'_'+str(user_question_choice_index+1)))
                        user_question_choice_item.save()
                    else:
                        user_question_choice_item.time = None
                        user_question_choice_item.save()
            elif request.POST.get('choice_type_'+str(user_question_index+1)) == '7':
                for user_question_choice_index, user_question_choice_item in enumerate(UserQuestionItemChoice.objects.filter(question=user_question_item).order_by('number').all()):
                    if request.POST.get('date_time_'+str(user_question_index+1)+'_'+str(user_question_choice_index+1)):
                        user_question_choice_item.date = urllib.parse.unquote(request.POST.get('date_time_'+str(user_question_index+1)+'_'+str(user_question_choice_index+1))).replace( '/', '-')
                        user_question_choice_item.save()
                    else:
                        user_question_choice_item.date = None
                        user_question_choice_item.save()
    return JsonResponse( {}, safe=False )