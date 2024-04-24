from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse

from PIL import Image

from flow.models import ShopFlowItem, ShopFlowTemplate, UserFlow, UserFlowSchedule
from question.models import UserQuestion, UserQuestionItem, UserQuestionItemChoice

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
                user_question_item.value = urllib.parse.unquote(request.POST.get('value_'+str(user_question_index+1))).replace('歳', ''),
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