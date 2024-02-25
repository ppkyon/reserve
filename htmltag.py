from django import template
from django.conf import settings

import math
import time

register = template.Library()

@register.filter(name="multiplication")
def multiplication(value1, value2):
    result = value1 * value2
    return result

@register.filter(name="division")
def division(value1, value2):
    result = value1 / value2
    result = math.ceil(result)
    return result

@register.filter(name="textarea_action_replace")
def textarea_action_replace(value):
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">', '【応募者の名前】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【応募者の名前】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/line-name.png" class="ms-1 me-1">', '【公式LINE名】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/line-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【公式LINE名】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/company-name.png" class="ms-1 me-1">', '【企業名】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/company-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【企業名】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1">', '【担当者名】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【担当者名】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1">', '【担当者電話番号】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【担当者電話番号】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/interview-date.png" class="ms-1 me-1">', '【面接日時】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/interview-date.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【面接日時】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1">', '【会場住所】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【会場住所】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/online-url.png" class="ms-1 me-1">', '【オンラインURL】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/online-url.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【オンラインURL】' )
    return value

@register.filter(name="convert_time")
def convert_time(value):
    return time.strftime('%M:%S', time.gmtime(value))