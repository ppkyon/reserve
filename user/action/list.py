from django.db.models import Q, OuterRef, Subquery

from flow.models import HeadFlow, ShopFlowTab, UserFlow
from sign.models import AuthLogin
from table.models import TableNumber, TableSort, TableSearch
from tag.models import ShopTag, UserHashTag
from user.models import LineUser, UserProfile, UserAlert

from common import get_model_field

import re

def get_list(request, page):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    url = request.path.replace('paging/', '').replace('search/', '')

    page = int(page)
    number = 5
    table_number = TableNumber.objects.filter(url=url, company=auth_login.company, shop=auth_login.shop, manager=request.user).first()
    if table_number:
        number = table_number.number
    
    start = number * ( page - 1 )
    end = number * page

    query = Q(shop=auth_login.shop)
    query.add(Q(proxy_flg=False), Q.AND)

    search = TableSearch.objects.filter(url=url, company=auth_login.company, shop=auth_login.shop, manager=request.user).all()
    search_query = Q()
    search_tag = None
    for search_item in search:
        if search_item.item == 'name':
            search_query.add(Q(**{'user_profile__name__icontains': search_item.text}), Q.AND)
        elif search_item.item == 'kana':
            search_query.add(Q(**{'user_profile__name_kana__icontains': search_item.text}), Q.AND)
        elif search_item.item == 'phone':
            search_query.add(Q(**{'user_profile__phone_number__icontains': search_item.text.replace('-', '')}), Q.AND)
        elif search_item.item == 'email':
            search_query.add(Q(**{'user_profile__email__icontains': search_item.text.replace('-', '')}), Q.AND)
        elif search_item.item == 'age_from':
            search_query.add(Q(**{'user_profile__age__gte': search_item.text.replace('歳', '')}), Q.AND)
        elif search_item.item == 'age_to':
            search_query.add(Q(**{'user_profile__age__lte': search_item.text.replace('歳', '')}), Q.AND)
        elif search_item.item == 'date_from':
            search_query.add(Q(**{'created_at__gte': search_item.text.replace('/', '-') + ' 00:00:00'}), Q.AND)
        elif search_item.item == 'date_to':
            search_query.add(Q(**{'created_at__lte': search_item.text.replace('/', '-') + ' 23:59:59'}), Q.AND)
        elif search_item.item == 'id_from':
            search_query.add(Q(**{'user_profile__atelle_id__gte': search_item.text.replace('#', '')}), Q.AND)
        elif search_item.item == 'id_to':
            search_query.add(Q(**{'user_profile__atelle_id__lte': search_item.text.replace('#', '')}), Q.AND)
        elif search_item.item == 'sex':
            search_query.add(Q(**{'user_profile__sex': search_item.text}), Q.AND)
        elif search_item.item == 'member':
            if search_item.text == '1':
                search_query.add(Q(**{'member_flg': True}), Q.AND)
            elif search_item.text == '2':
                search_query.add(Q(**{'member_flg': False}), Q.AND)
        elif search_item.item == 'tag':
            search_tag = search_item.text.split(",")
            search_query.add(Q(**{'all_tag__in': search_tag}), Q.AND)
        elif search_item.item == 'flow':
            search_flow = search_item.text.split(",")
            flow_list = list()
            for flow in HeadFlow.objects.order_by('-created_at').all():
                flow_tab_list = flow.description.split('→')
                for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
                    if str(flow_tab_index) in search_flow:
                        flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                        if not flow_chart_name in flow_list:
                            flow_list.append(flow_chart_name)
            search_query.add(Q(**{'active_flow_name__in': flow_list}), Q.AND)
    query.add(search_query, Q.AND)

    sort = TableSort.objects.filter(url=url, company=auth_login.shop.company, shop=auth_login.shop, manager=request.user).first()
    flow = UserFlow.objects.filter(user=OuterRef('pk'), end_flg=False).order_by('flow_tab__number').values("flow_tab__number", "flow_tab__name")
    alert = UserAlert.objects.filter(user=OuterRef('pk')).order_by('-status').values("status")
    if search_tag:
        tag = UserHashTag.objects.filter(user=OuterRef('pk'), tag__display_id__in=search_tag).order_by('-created_at').values("tag__display_id")
    else:
        tag = UserHashTag.objects.filter(user=OuterRef('pk'), tag__display_id__in=list()).order_by('-created_at').values("tag__display_id")
    if sort:
        if sort.target == 'user_flow__number':
            if sort.sort == 1:
                user_list = LineUser.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow=Subquery(flow.values('flow_tab__number')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query).order_by('alert', 'active_flow', '-created_at').values(*get_model_field(LineUser)).all()[start:end]
            elif sort.sort == 2:
                user_list = LineUser.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow=Subquery(flow.values('flow_tab__number')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query).order_by('alert', '-active_flow', '-created_at').values(*get_model_field(LineUser)).all()[start:end]
            else:
                user_list = LineUser.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query).order_by('alert', '-created_at').values(*get_model_field(LineUser)).all()[start:end]
        else:
            if sort.sort == 1:
                user_list = LineUser.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query).order_by('alert', sort.target, '-created_at').values(*get_model_field(LineUser)).all()[start:end]
            elif sort.sort == 2:
                user_list = LineUser.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query).order_by('alert', '-'+sort.target, '-created_at').values(*get_model_field(LineUser)).all()[start:end]
            else:
                user_list = LineUser.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query).order_by('alert', '-created_at').values(*get_model_field(LineUser)).all()[start:end]
    else:
        user_list = LineUser.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query).order_by('alert', '-created_at').values(*get_model_field(LineUser)).all()[start:end]
    total = LineUser.objects.annotate(active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query).distinct().count()

    for user_index, user_item in enumerate(user_list):
        user_list[user_index]['profile'] = UserProfile.objects.filter(user__id=user_item['id']).values(*get_model_field(UserProfile)).first()
        user_list[user_index]['active_flow'] = UserFlow.objects.filter(user__id=user_item['id'], end_flg=False).order_by('flow_tab__number').values(*get_model_field(UserFlow)).first()
        if user_list[user_index]['active_flow']:
            user_list[user_index]['active_flow']['flow_tab'] = ShopFlowTab.objects.filter(id=user_list[user_index]['active_flow']['flow_tab']).values(*get_model_field(ShopFlowTab)).first()
        user_list[user_index]['tag'] = list(UserHashTag.objects.filter(user__id=user_item['id']).order_by('number').values(*get_model_field(UserHashTag)).all())
        for tag_index, tag_item in enumerate(user_list[user_index]['tag']):
            user_list[user_index]['tag'][tag_index]['tag'] = ShopTag.objects.filter(id=tag_item['tag']).values(*get_model_field(ShopTag)).first()
        user_list[user_index]['alert'] = UserAlert.objects.filter(user__id=user_item['id']).order_by('number').values(*get_model_field(UserAlert)).first()
        user_list[user_index]['total'] = total
    
    return user_list