from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from PIL import Image

from flow.models import UserFlow, UserFlowSchedule, UserFlowActionReminder, UserFlowActionMessage
from sign.models import CompanyProfile, ManagerProfile
from user.models import UserProfile

import cv2
import datetime
import io
import itertools
import phonenumbers
import string
import random
import uuid

def create_code(dig, model, other_models=[]):
    code_list = model.objects.values_list('display_id', flat=True)

    other_code_list = []
    if other_models:
        for m in other_models:
            other_code_list.append(m.objects.values_list('display_id', flat=True))
        other_code_list = itertools.chain.from_iterable(other_code_list)
    
    min = 10 ** (dig - 1)
    max = 10 ** dig - 1
    while True:
        code = random.randint(min, max)
        if code not in code_list and code not in other_code_list:
            break

    return code

def create_token():
    return uuid.uuid4().hex

def create_password():
    random_list = [random.choice(string.ascii_letters + string.digits) for i in range(8)]
    return ''.join(random_list)

def create_expiration_date(hours):
    now = datetime.datetime.now()
    return now + datetime.timedelta(hours=hours)



def display_time(time):
    if '前' in time.split(',')[0]:
        return time.split(',')[0]
    else:
        return time.split(',')[0] + '前'

def display_textarea_replace( text ):
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">', '【応募者の名前】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【応募者の名前】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/line-name.png" class="ms-1 me-1">', '【公式LINE名】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/line-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【公式LINE名】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/company-name.png" class="ms-1 me-1">', '【企業名】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/company-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【企業名】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1">', '【担当者名】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【担当者名】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1">', '【担当者電話番号】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【担当者電話番号】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1">', '【予約日時】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【予約日時】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1">', '【会場住所】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【会場住所】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/online-url.png" class="ms-1 me-1">', '【オンラインURL】' )
    text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/online-url.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【オンラインURL】' )
    return text

def send_textarea_replace( text, line_data, user ):
    text = text.replace( '<br>', '\n' )
    text = text.replace( '</div>', '\n' )
    for user_profile in user.user_profile.all():
        if user_profile.name:
            text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">', user_profile.name )
            text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', user_profile.name )
        else:
            text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">', user.display_name )
            text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', user.display_name )
        break
    
    if line_data and line_data.display_name:
        text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/line-name.png" class="ms-1 me-1">', line_data.display_name )
        text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/line-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', line_data.display_name )
    
    company_profile = CompanyProfile.objects.filter(company=user.shop.company).first()
    if company_profile and company_profile.company_name:
        text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/company-name.png" class="ms-1 me-1">', company_profile.company_name )
        text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/company-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', company_profile.company_name )

    manager = None
    reserve_date = None
    place_address = None
    if UserFlowActionReminder.objects.filter(user=user, action_date__lte=datetime.datetime.now()).exists():
        for reminder_item in UserFlowActionReminder.objects.filter(user=user, action_date__lte=datetime.datetime.now()).order_by('flow__number').all():
            import logging
            logger = logging.getLogger('development')
            logger.info(reminder_item.flow)
            for schedule in UserFlowSchedule.objects.filter(flow=reminder_item.flow, cancel_flg=False).order_by('number').all():
                manager = schedule.manager
                date = datetime.datetime(schedule.date.year, schedule.date.month, schedule.date.day, schedule.time.hour, schedule.time.minute, 0)
                if schedule.online:
                    add_date = date + datetime.timedelta(minutes=schedule.online.time)
                elif schedule.offline:
                    add_date = date + datetime.timedelta(minutes=schedule.offline.time)
                    place_address = schedule.offline.offline.address
                if schedule.date.weekday() == 0:
                    week = '(月)'
                elif schedule.date.weekday() == 1:
                    week = '(火)'
                elif schedule.date.weekday() == 2:
                    week = '(水)'
                elif schedule.date.weekday() == 3:
                    week = '(木)'
                elif schedule.date.weekday() == 4:
                    week = '(金)'
                elif schedule.date.weekday() == 5:
                    week = '(土)'
                elif schedule.date.weekday() == 6:
                    week = '(日)'
                reserve_date = str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日' + week + str(date.hour) + ':' + str(date.minute).zfill(2) + '～' + str(add_date.hour) + ':' + str(add_date.minute).zfill(2)
                break

    if manager:
        manager_profile = ManagerProfile.objects.filter(manager=manager).first()
        if manager_profile:
            text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1">', manager_profile.family_name + manager_profile.first_name )
            text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', manager_profile.family_name + manager_profile.first_name )
        if manager_profile and manager_profile.phone_number:
            text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1">', phonenumbers.format_number(phonenumbers.parse(manager_profile.phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL) )
            text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1" style="font-size: 12.8px;">', phonenumbers.format_number(phonenumbers.parse(manager_profile.phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL) )
    
    if reserve_date:
        text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1">', reserve_date )
        text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1" style="font-size: 12.8px;">', reserve_date )

    if place_address:
        text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1">', place_address )
        text = text.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1" style="font-size: 12.8px;">', place_address )

    return text

def send_action_replace( text, line_data, user ):
    display_name = user.display_name
    if UserProfile.objects.filter(user=user).exists():
        profile = UserProfile.objects.filter(user=user).first()
        if profile.name:
            display_name = profile.name
    if display_name:
        text = text.replace( '【応募者名】', display_name )
    if line_data and line_data.display_name:
        text = text.replace( '【公式LINE名】', line_data.display_name )

    company_profile = CompanyProfile.objects.filter(company=user.shop.company).first()
    if company_profile and company_profile.company_name:
        text = text.replace( '【企業名】', company_profile.company_name )
    
    reserve_date = ''
    for user_flow in UserFlow.objects.filter(user=user, end_flg=False).order_by('number').all():
        user_flow_schedule = UserFlowSchedule.objects.filter(flow=user_flow).order_by('-updated_at').first()
        if user_flow_schedule:
            date = datetime.datetime(user_flow_schedule.date.year, user_flow_schedule.date.month, user_flow_schedule.date.day, user_flow_schedule.time.hour, user_flow_schedule.time.minute, 0)
            if user_flow_schedule.online:
                add_date = date + datetime.timedelta(minutes=user_flow_schedule.online.time)
            elif user_flow_schedule.offline:
                add_date = date + datetime.timedelta(minutes=user_flow_schedule.offline.time)

            if user_flow_schedule.date.weekday() == 0:
                week = '(月)'
            elif user_flow_schedule.date.weekday() == 1:
                week = '(火)'
            elif user_flow_schedule.date.weekday() == 2:
                week = '(水)'
            elif user_flow_schedule.date.weekday() == 3:
                week = '(木)'
            elif user_flow_schedule.date.weekday() == 4:
                week = '(金)'
            elif user_flow_schedule.date.weekday() == 5:
                week = '(土)'
            elif user_flow_schedule.date.weekday() == 6:
                week = '(日)'
            reserve_date = str(date.year) + '年' + str(date.month) + '月' + str(date.day) + '日' + week + str(date.hour) + ':' + str(date.minute).zfill(2) + '～' + str(add_date.hour) + ':' + str(add_date.minute).zfill(2)
    
    text = text.replace( '【予約日時】', reserve_date )
    return text



def resize_image(image, width, height, type):

    h, w = image.shape[:2]
    aspect = w / h
    if width / height >= aspect:
        nh = height
        nw = round(nh * aspect)
    else:
        nw = width
        nh = round(nw / aspect)

    image = cv2.resize(image, dsize=(nw, nh))
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if type == 'png':
        trans = Image.new('RGBA', image.size, (0, 0, 0, 0))
    elif type == 'jpg':
        trans = Image.new('RGBA', image.size, (0, 0, 0, 0)).convert('RGB')
    width = image.size[0]
    height = image.size[1]
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel( (x, y) )
            
            if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                continue
            
            trans.putpixel( (x, y), pixel )
    image_io = io.BytesIO()
    if type == 'png':
        trans.save(image_io, format="PNG")
        image_file = InMemoryUploadedFile(image_io, field_name=None, name=str(uuid.uuid4()).replace('-', '') + '.png', content_type="image/png", size=image_io.getbuffer().nbytes, charset=None)
    elif type == 'jpg':
        trans.save(image_io, format="JPEG")
        image_file = InMemoryUploadedFile(image_io, field_name=None, name=str(uuid.uuid4()).replace('-', '') + '.jpg', content_type="image/jpeg", size=image_io.getbuffer().nbytes, charset=None)

    return image_file



def get_model_field(model, old=False):
    if old:
        field_list = list()
        for field_index, field_value in enumerate(model._meta.get_fields()):
            field_list.append(field_value.name)
        return field_list
    else:
        meta_fields = model._meta.get_fields()
        filtered_fields = filter(
            lambda x: not isinstance(x, models.ManyToOneRel),
            meta_fields
        )
        meta_field_names = map(lambda x: x.name, filtered_fields)
        return list(meta_field_names)