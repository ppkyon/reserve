from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

from PIL import Image

import cv2
import datetime
import io
import itertools
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