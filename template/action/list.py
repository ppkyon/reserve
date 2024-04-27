from django.db.models import Q

from sign.models import AuthLogin
from table.models import TableSearch, TableSort, TableNumber
from template.models import (
    ShopTemplateText, ShopTemplateTextItem, ShopTemplateVideo, ShopTemplateRichMessage, ShopTemplateRichMessageItem, ShopTemplateRichVideo,
    ShopTemplateCardType, ShopTemplateCardTypeAnnounce, ShopTemplateCardTypeLocation, ShopTemplateCardTypePerson, ShopTemplateCardTypeImage
)

from common import display_textarea_replace, get_model_field

import time
import re

def get_text_list(request, page):
    url = request.path.replace('paging/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    query = Q(company=auth_login.shop.company)
    query.add(Q(shop=auth_login.shop), Q.AND)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text)|Q(shop_template_text_item__text__icontains=table_search.text), Q.AND)

    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = ShopTemplateText.objects.filter(query, Q(shop_template_text_item__number=1)).order_by('-favorite_flg', sort.target, '-created_at').values(*get_model_field(ShopTemplateText)).all()[start:end]
        elif sort.sort == 2:
            template = ShopTemplateText.objects.filter(query, Q(shop_template_text_item__number=1)).order_by('-favorite_flg', '-'+sort.target, '-created_at').values(*get_model_field(ShopTemplateText)).all()[start:end]
        else:
            template = ShopTemplateText.objects.filter(query, Q(shop_template_text_item__number=1)).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateText)).all()[start:end]
    else:
        template = ShopTemplateText.objects.filter(query, Q(shop_template_text_item__number=1)).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateText)).all()[start:end]
    total = ShopTemplateText.objects.filter(query, Q(shop_template_text_item__number=1)).count()

    remove = re.compile(r"<[^>]*?>")
    for template_index, template_item in enumerate(template):
        template[template_index]['item'] = list(ShopTemplateTextItem.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateTextItem)).all())
        for template_item_index, template_item_item in enumerate(template[template_index]['item']):
            if template_item_item['text']:
                template[template_index]['item'][template_item_index]['text'] = remove.sub('', display_textarea_replace(template_item_item['text']))
        template[template_index]['total'] = total

    return template

def get_video_list(request, page):
    url = request.path.replace('paging/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    query = Q(company=auth_login.shop.company)
    query.add(Q(shop=auth_login.shop), Q.AND)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = ShopTemplateVideo.objects.filter(query).order_by('-favorite_flg', sort.target, '-created_at').values(*get_model_field(ShopTemplateVideo)).all()[start:end]
        elif sort.sort == 2:
            template = ShopTemplateVideo.objects.filter(query).order_by('-favorite_flg', '-'+sort.target, '-created_at').values(*get_model_field(ShopTemplateVideo)).all()[start:end]
        else:
            template = ShopTemplateVideo.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateVideo)).all()[start:end]
    else:
        template = ShopTemplateVideo.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateVideo)).all()[start:end]
    total = ShopTemplateVideo.objects.filter(query).count()

    for template_index, template_item in enumerate(template):
        template[template_index]['video_display_time'] = time.strftime('%M:%S', time.gmtime(template_item['video_time']))
        template[template_index]['total'] = total

    return template

def get_richmessage_list(request, page):
    url = request.path.replace('paging/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    query = Q(company=auth_login.shop.company)
    query.add(Q(shop=auth_login.shop), Q.AND)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = ShopTemplateRichMessage.objects.filter(query).order_by('-favorite_flg', sort.target, '-created_at').values(*get_model_field(ShopTemplateRichMessage)).all()[start:end]
        elif sort.sort == 2:
            template = ShopTemplateRichMessage.objects.filter(query).order_by('-favorite_flg', '-'+sort.target, '-created_at').values(*get_model_field(ShopTemplateRichMessage)).all()[start:end]
        else:
            template = ShopTemplateRichMessage.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateRichMessage)).all()[start:end]
    else:
        template = ShopTemplateRichMessage.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateRichMessage)).all()[start:end]
    total = ShopTemplateRichMessage.objects.filter(query).count()

    for template_index, template_item in enumerate(template):
        template[template_index]['item'] = list(ShopTemplateRichMessageItem.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateRichMessageItem)).all())
        template[template_index]['total'] = total

    return template

def get_richvideo_list(request, page):
    url = request.path.replace('paging/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    query = Q(company=auth_login.shop.company)
    query.add(Q(shop=auth_login.shop), Q.AND)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = ShopTemplateRichVideo.objects.filter(query).order_by('-favorite_flg', sort.target, '-created_at').values(*get_model_field(ShopTemplateRichVideo)).all()[start:end]
        elif sort.sort == 2:
            template = ShopTemplateRichVideo.objects.filter(query).order_by('-favorite_flg', '-'+sort.target, '-created_at').values(*get_model_field(ShopTemplateRichVideo)).all()[start:end]
        else:
            template = ShopTemplateRichVideo.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateRichVideo)).all()[start:end]
    else:
        template = ShopTemplateRichVideo.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateRichVideo)).all()[start:end]
    total = ShopTemplateRichVideo.objects.filter(query).count()

    for template_index, template_item in enumerate(template):
        template[template_index]['video_display_time'] = time.strftime('%M:%S', time.gmtime(template_item['video_time']))
        template[template_index]['total'] = total

    return template

def get_cardtype_list(request, page):
    url = request.path.replace('paging/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    query = Q(company=auth_login.shop.company)
    query.add(Q(shop=auth_login.shop), Q.AND)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = ShopTemplateCardType.objects.filter(query).order_by('-favorite_flg', sort.target, '-created_at').values(*get_model_field(ShopTemplateCardType)).all()[start:end]
        elif sort.sort == 2:
            template = ShopTemplateCardType.objects.filter(query).order_by('-favorite_flg', '-'+sort.target, '-created_at').values(*get_model_field(ShopTemplateCardType)).all()[start:end]
        else:
            template = ShopTemplateCardType.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateCardType)).all()[start:end]
    else:
        template = ShopTemplateCardType.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopTemplateCardType)).all()[start:end]
    total = ShopTemplateCardType.objects.filter(query).count()

    for template_index, template_item in enumerate(template):
        if template_item['type'] == 1:
            template[template_index]['item'] = list(ShopTemplateCardTypeAnnounce.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateCardTypeAnnounce)).all())
        elif template_item['type'] == 2:
            template[template_index]['item'] = list(ShopTemplateCardTypeLocation.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateCardTypeLocation)).all())
        elif template_item['type'] == 3:
            template[template_index]['item'] = list(ShopTemplateCardTypePerson.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateCardTypePerson)).all())
        elif template_item['type'] == 4:
            template[template_index]['item'] = list(ShopTemplateCardTypeImage.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateCardTypeImage)).all())
        template[template_index]['total'] = total

    return template



def get_table_number(request, url):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    number = 5
    table_number = TableNumber.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    if table_number:
        number = table_number.number
    return number