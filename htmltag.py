from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.templatetags.static import static

from pathlib import Path

import datetime
import locale
import math
import time

register = template.Library()

@register.simple_tag
def variable(value=None):
    return value

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
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1">', '【予約日時】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【予約日時】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1">', '【会場住所】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【会場住所】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/online-url.png" class="ms-1 me-1">', '【オンラインURL】' )
    value = value.replace( '<img src="' + settings.STATIC_URL + 'img/textarea/online-url.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【オンラインURL】' )
    
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1">', '【応募者の名前】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/display-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【応募者の名前】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/line-name.png" class="ms-1 me-1">', '【公式LINE名】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/line-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【公式LINE名】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/company-name.png" class="ms-1 me-1">', '【企業名】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/company-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【企業名】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1">', '【担当者名】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/manager-name.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【担当者名】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1">', '【担当者電話番号】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/manager-phone.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【担当者電話番号】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1">', '【予約日時】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/reserve-date.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【予約日時】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1">', '【会場住所】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/offline-address.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【会場住所】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/online-url.png" class="ms-1 me-1">', '【オンラインURL】' )
    value = value.replace( '<img src="' + settings.DOMAIN_URL + settings.STATIC_URL + 'img/textarea/online-url.png" class="ms-1 me-1" style="font-size: 12.8px;">', '【オンラインURL】' )
    return value

@register.filter(name="convert_time")
def convert_time(value):
    return time.strftime('%M:%S', time.gmtime(value))

@register.filter(name="add_num")
def add_num(value1=None, value2=None):
    return str(value1) + str(value2)

@register.filter(is_safe=True)
@stringfilter
def display_day(value):
    if '年' in value:
        locale.setlocale(locale.LC_TIME, 'ja_JP')
        date = datetime.datetime.strptime(value, '%Y年%m月%d日')
        return value.split('年')[1] + '(' + date.strftime('%a') + ')'
    else:
        return value

@register.filter(is_safe=True)
@stringfilter
def display_time(value):
    if '前' in value.split(',')[0]:
        return value.split(',')[0]
    else:
        if '今' in value:
            return value.split(',')[0]
        else:
            return value.split(',')[0] + '前'



@register.simple_tag
def static_cache(filepath) -> str:
    res_path = static(filepath)
    full_filepath = Path(getattr(settings, 'STATICFILES_DIRS', '')[0]).joinpath(filepath)
    file_mtime = str(int(full_filepath.stat().st_mtime))
    res_path += '?v=' + file_mtime
    return res_path