from django.db.models import Q

from sign.models import AuthLogin
from table.models import TableSearch, TableSort, TableNumber
from template.models import (
    CompanyTemplateText, CompanyTemplateTextItem, CompanyTemplateVideo, CompanyTemplateRichMessage, CompanyTemplateRichMessageItem, CompanyTemplateRichVideo,
    CompanyTemplateCardType, CompanyTemplateCardTypeAnnounce, CompanyTemplateCardTypeLocation, CompanyTemplateCardTypePerson, CompanyTemplateCardTypeImage
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
    query = Q(company=auth_login.company)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text)|Q(company_template_text_item__text__icontains=table_search.text), Q.AND)

    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = CompanyTemplateText.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(CompanyTemplateText)).all()[start:end]
        elif sort.sort == 2:
            template = CompanyTemplateText.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(CompanyTemplateText)).all()[start:end]
        else:
            template = CompanyTemplateText.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateText)).all()[start:end]
    else:
        template = CompanyTemplateText.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateText)).all()[start:end]
    total = CompanyTemplateText.objects.filter(query).count()

    remove = re.compile(r"<[^>]*?>")
    for template_index, template_item in enumerate(template):
        template[template_index]['item'] = list(CompanyTemplateTextItem.objects.filter(template__id=template_item['id']).values(*get_model_field(CompanyTemplateTextItem)).all())
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
    query = Q(company=auth_login.company)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = CompanyTemplateVideo.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(CompanyTemplateVideo)).all()[start:end]
        elif sort.sort == 2:
            template = CompanyTemplateVideo.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(CompanyTemplateVideo)).all()[start:end]
        else:
            template = CompanyTemplateVideo.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateVideo)).all()[start:end]
    else:
        template = CompanyTemplateVideo.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateVideo)).all()[start:end]
    total = CompanyTemplateVideo.objects.filter(query).count()

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
    query = Q(company=auth_login.company)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = CompanyTemplateRichMessage.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(CompanyTemplateRichMessage)).all()[start:end]
        elif sort.sort == 2:
            template = CompanyTemplateRichMessage.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(CompanyTemplateRichMessage)).all()[start:end]
        else:
            template = CompanyTemplateRichMessage.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateRichMessage)).all()[start:end]
    else:
        template = CompanyTemplateRichMessage.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateRichMessage)).all()[start:end]
    total = CompanyTemplateRichMessage.objects.filter(query).count()

    for template_index, template_item in enumerate(template):
        template[template_index]['item'] = list(CompanyTemplateRichMessageItem.objects.filter(template__id=template_item['id']).values(*get_model_field(CompanyTemplateRichMessageItem)).all())
        template[template_index]['total'] = total

    return template

def get_richvideo_list(request, page):
    url = request.path.replace('paging/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    query = Q(company=auth_login.company)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = CompanyTemplateRichVideo.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(CompanyTemplateRichVideo)).all()[start:end]
        elif sort.sort == 2:
            template = CompanyTemplateRichVideo.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(CompanyTemplateRichVideo)).all()[start:end]
        else:
            template = CompanyTemplateRichVideo.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateRichVideo)).all()[start:end]
    else:
        template = CompanyTemplateRichVideo.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateRichVideo)).all()[start:end]
    total = CompanyTemplateRichVideo.objects.filter(query).count()

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
    query = Q(company=auth_login.company)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = CompanyTemplateCardType.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(CompanyTemplateCardType)).all()[start:end]
        elif sort.sort == 2:
            template = CompanyTemplateCardType.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(CompanyTemplateCardType)).all()[start:end]
        else:
            template = CompanyTemplateCardType.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateCardType)).all()[start:end]
    else:
        template = CompanyTemplateCardType.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyTemplateCardType)).all()[start:end]
    total = CompanyTemplateCardType.objects.filter(query).count()

    for template_index, template_item in enumerate(template):
        if template_item['type'] == 1:
            template[template_index]['item'] = list(CompanyTemplateCardTypeAnnounce.objects.filter(template__id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypeAnnounce)).all())
        elif template_item['type'] == 2:
            template[template_index]['item'] = list(CompanyTemplateCardTypeLocation.objects.filter(template__id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypeLocation)).all())
        elif template_item['type'] == 3:
            template[template_index]['item'] = list(CompanyTemplateCardTypePerson.objects.filter(template__id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypePerson)).all())
        elif template_item['type'] == 4:
            template[template_index]['item'] = list(CompanyTemplateCardTypeImage.objects.filter(template__id=template_item['id']).values(*get_model_field(CompanyTemplateCardTypeImage)).all())
        template[template_index]['total'] = total

    return template



def get_table_number(request, url):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    number = 5
    table_number = TableNumber.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if table_number:
        number = table_number.number
    return number