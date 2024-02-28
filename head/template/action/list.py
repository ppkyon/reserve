from django.db.models import Q

from table.models import TableSearch, TableSort, TableNumber
from template.models import HeadTemplateText, HeadTemplateTextItem, HeadTemplateVideo, HeadTemplateRichMessage, HeadTemplateRichMessageItem, HeadTemplateRichVideo

from common import display_textarea_replace, get_model_field

import time
import re

def get_text_list(request, page):
    url = request.path.replace('page/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    query = Q()
    table_search = TableSearch.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text)|Q(head_template_text_item__text__icontains=table_search.text), Q.AND)

    template = list()
    sort = TableSort.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = HeadTemplateText.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(HeadTemplateText)).all()[start:end]
        elif sort.sort == 2:
            template = HeadTemplateText.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(HeadTemplateText)).all()[start:end]
        else:
            template = HeadTemplateText.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadTemplateText)).all()[start:end]
    else:
        template = HeadTemplateText.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadTemplateText)).all()[start:end]
    total = HeadTemplateText.objects.filter(query).count()

    remove = re.compile(r"<[^>]*?>")
    for template_index, template_item in enumerate(template):
        template[template_index]['item'] = list(HeadTemplateTextItem.objects.filter(template__id=template_item['id']).values(*get_model_field(HeadTemplateTextItem)).all())
        for template_item_index, template_item_item in enumerate(template[template_index]['item']):
            if template_item_item['text']:
                template[template_index]['item'][template_item_index]['text'] = remove.sub('', display_textarea_replace(template_item_item['text']))
        template[template_index]['total'] = total

    return template

def get_video_list(request, page):
    url = request.path.replace('page/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    query = Q()
    table_search = TableSearch.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = HeadTemplateVideo.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(HeadTemplateVideo)).all()[start:end]
        elif sort.sort == 2:
            template = HeadTemplateVideo.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(HeadTemplateVideo)).all()[start:end]
        else:
            template = HeadTemplateVideo.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadTemplateVideo)).all()[start:end]
    else:
        template = HeadTemplateVideo.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadTemplateVideo)).all()[start:end]
    total = HeadTemplateVideo.objects.filter(query).count()

    for template_index, template_item in enumerate(template):
        template[template_index]['video_display_time'] = time.strftime('%M:%S', time.gmtime(template_item['video_time']))
        template[template_index]['total'] = total

    return template

def get_richmessage_list(request, page):
    url = request.path.replace('page/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    query = Q()
    table_search = TableSearch.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = HeadTemplateRichMessage.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(HeadTemplateRichMessage)).all()[start:end]
        elif sort.sort == 2:
            template = HeadTemplateRichMessage.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(HeadTemplateRichMessage)).all()[start:end]
        else:
            template = HeadTemplateRichMessage.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadTemplateRichMessage)).all()[start:end]
    else:
        template = HeadTemplateRichMessage.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadTemplateRichMessage)).all()[start:end]
    total = HeadTemplateRichMessage.objects.filter(query).count()

    for template_index, template_item in enumerate(template):
        template[template_index]['item'] = list(HeadTemplateRichMessageItem.objects.filter(template__id=template_item['id']).values(*get_model_field(HeadTemplateRichMessageItem)).all())
        template[template_index]['total'] = total

    return template

def get_richvideo_list(request, page):
    url = request.path.replace('page/', '').replace('search/', '')
    page = int(page)
    number = get_table_number(request, url)
    start = number * ( page - 1 )
    end = number * page

    query = Q()
    table_search = TableSearch.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    template = list()
    sort = TableSort.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            template = HeadTemplateRichVideo.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(HeadTemplateRichVideo)).all()[start:end]
        elif sort.sort == 2:
            template = HeadTemplateRichVideo.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(HeadTemplateRichVideo)).all()[start:end]
        else:
            template = HeadTemplateRichVideo.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadTemplateRichVideo)).all()[start:end]
    else:
        template = HeadTemplateRichVideo.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadTemplateRichVideo)).all()[start:end]
    total = HeadTemplateRichVideo.objects.filter(query).count()

    for template_index, template_item in enumerate(template):
        template[template_index]['video_display_time'] = time.strftime('%M:%S', time.gmtime(template_item['video_time']))
        template[template_index]['total'] = total

    return template



def get_table_number(request, url):
    number = 5
    table_number = TableNumber.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if table_number:
        number = table_number.number
    return number