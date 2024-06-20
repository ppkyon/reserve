from django.conf import settings
from django.db import models
from django.db.models import Q, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin, BaseListView

from sign.mixins import HeadLoginMixin, CompanyLoginMixin, ShopLoginMixin

from flow.models import HeadFlow, ShopFlow, UserFlow
from setting.models import SettingAlert
from sign.models import AuthUser, CompanyProfile, ShopProfile, ManagerProfile, AuthLogin
from table.models import TableNumber, TableSort, TableSearch
from tag.models import ShopTag, UserHashTag
from talk.models import TalkRead
from user.models import LineUser, UserAlert

from dateutil.relativedelta import relativedelta

import datetime
import environ
import re

env = environ.Env()
env.read_env('.env')

class TopBaseView(TemplateView):
    title = ''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.title
        
        site_name = env('SITE_NAME')
        if env('ENCODING') == 'True':
            site_name = site_name.encode("shift-jis").decode("utf-8", errors="ignore")
        web_index = 'False'
        if env('WEB_INDEX'):
            web_index = env('WEB_INDEX')
        context['env'] = {
            'domain_url': settings.DOMAIN_URL,
            'static_url': settings.STATIC_URL,
            'media_url': settings.MEDIA_URL,
            'site_name': site_name,
            'web_index': web_index,
        }

        manager = None
        if not self.request.user.is_anonymous:
            manager = AuthUser.objects.filter(id=self.request.user.id).first()
            manager.profile = ManagerProfile.objects.filter(manager=manager).first()
        context['header'] = {
            'manager': manager,
        }
        
        return context



class HeadBaseView(HeadLoginMixin, TopBaseView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
    
class CompanyBaseView(CompanyLoginMixin, TopBaseView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        image = None
        name = None
        if not self.request.user.is_anonymous:
            auth_login = AuthLogin.objects.filter(user=self.request.user).first()
            if auth_login:
                company = auth_login.company
                company_profile = CompanyProfile.objects.filter(company=company).first()
                if company_profile:
                    image = company_profile.company_logo_image.url
                    name = company_profile.company_name
        
        context['side'] = {
            'logo_image': image,
            'logo_name': name,
        }
        return context
    
class ShopBaseView(ShopLoginMixin, TopBaseView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        alert = None
        image = None
        name = None
        temp_flg = False
        if not self.request.user.is_anonymous:
            auth_login = AuthLogin.objects.filter(user=self.request.user).first()
            if auth_login:
                shop = auth_login.shop
                shop_profile = ShopProfile.objects.filter(shop=shop).first()
                if shop_profile:
                    image = shop_profile.shop_logo_image.url
                    name = shop_profile.shop_name
                
                flow = 0
                shop_flow = ShopFlow.objects.filter(shop=shop).order_by('-period_to').first()
                if shop_flow:
                    if shop_flow.period_to and shop_flow.period_to <= datetime.datetime.now() and flow < 3:
                        flow = 3
                    elif shop_flow.period_to and shop_flow.period_to <= datetime.datetime.now() + relativedelta(days=+10) and flow < 2:
                        flow = 2
                talk_read = TalkRead.objects.filter(user__delete_flg=False, manager=self.request.user).aggregate(sum_read_count=models.Sum('read_count'))
                user_count = UserAlert.objects.filter(user__shop=shop, user__proxy_flg=False).count()
                temp_count = UserAlert.objects.filter(user__shop=shop, user__proxy_flg=True).count()
                alert = {
                    'reserve': user_count + temp_count,
                    'user': user_count,
                    'temp': temp_count,
                    'talk': talk_read['sum_read_count'],
                    'flow': flow,
                    'setting': SettingAlert.objects.filter(shop=shop).first()
                }

            if LineUser.objects.filter(shop=shop, proxy_flg=True).exists():
                temp_flg = True
        
        context['side'] = {
            'alert': alert,
            'logo_image': image,
            'logo_name': name,
            'temp_flg': temp_flg,
        }
        return context

class HeadView(HeadBaseView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class CompanyView(CompanyBaseView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class ShopView(ShopBaseView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class UserView(ShopBaseView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class TempView(ShopBaseView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context



class HeadBaseLisView(MultipleObjectMixin, HeadBaseView):
    def get_paginate_by(self, queryset):
        number = 5
        table_number = TableNumber.objects.filter(url=self.request.path, company=None, shop=None, manager=self.request.user).first()
        if table_number:
            number = table_number.number
        return number

    def get_queryset(self):
        query = Q()
        if 'company' in self.request.path:
            query.add(Q(status__gte=2), Q.AND)

        search = TableSearch.objects.filter(url=self.request.path, company=None, shop=None, manager=self.request.user).first()
        if search:
            search_query = Q()
            for search_item in self.search_target:
                search_query.add(Q(**{search_item + '__icontains': search.text}), Q.OR)
            query.add(search_query, Q.AND)
        
        sort = TableSort.objects.filter(url=self.request.path, company=None, shop=None, manager=self.request.user).first()
        if sort:
            if sort.sort == 1:
                return self.model.objects.filter(query).order_by(sort.target, self.default_sort).all()
            elif sort.sort == 2:
                return self.model.objects.filter(query).order_by('-'+sort.target, self.default_sort).all()
            else:
                return self.model.objects.filter(query).order_by(self.default_sort).all()
        else:
            return self.model.objects.filter(query).order_by(self.default_sort).all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        sort = TableSort.objects.filter(url=self.request.path, company=None, shop=None, manager=self.request.user).first()
        if not sort:
            if '-' in self.default_sort:
                sort = {
                    'target': self.default_sort.replace('-', ''),
                    'sort': 2,
                }
            else:
                sort = {
                    'target': self.default_sort,
                    'sort': 1,
                }
        
        number = self.get_paginate_by(None)
        count = self.get_queryset().count()
        count_start = 1
        if number > count:
            count_end = count
        else:
            count_end = number
        if count_end == 0:
            count_start = 0
        context['table'] = {
            'number': number,
            'sort': sort,
            'search': TableSearch.objects.filter(url=self.request.path, company=None, shop=None, manager=self.request.user).first(),
            'count': count,
            'count_start': count_start,
            'count_end': count_end,
        }
        return context
    
class CompanyBaseLisView(MultipleObjectMixin, CompanyBaseView):
    def get_paginate_by(self, queryset):
        number = 5
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        table_number = TableNumber.objects.filter(url=self.request.path, company=auth_login.company, shop=None, manager=self.request.user).first()
        if table_number:
            number = table_number.number
        return number

    def get_queryset(self):
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        query = Q(company=auth_login.company)
        if 'shop' in self.request.path:
            query.add(Q(status__gte=2), Q.AND)

        search = TableSearch.objects.filter(url=self.request.path, company=auth_login.company, shop=None, manager=self.request.user).first()
        if search:
            search_query = Q()
            for search_item in self.search_target:
                search_query.add(Q(**{search_item + '__icontains': search.text}), Q.OR)
            query.add(search_query, Q.AND)

        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=None, manager=self.request.user).first()
        if sort:
            if sort.sort == 1:
                return self.model.objects.filter(query).order_by(sort.target, self.default_sort).all()
            elif sort.sort == 2:
                return self.model.objects.filter(query).order_by('-'+sort.target, self.default_sort).all()
            else:
                return self.model.objects.filter(query).order_by(self.default_sort).all()
        else:
            return self.model.objects.filter(query).order_by(self.default_sort).all()
    
    def get_context_data(self, *args, **kwargs):
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context = super().get_context_data(*args, **kwargs)
        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=None, manager=self.request.user).first()
        if not sort:
            if '-' in self.default_sort:
                sort = {
                    'target': self.default_sort.replace('-', ''),
                    'sort': 2,
                }
            else:
                sort = {
                    'target': self.default_sort,
                    'sort': 1,
                }
        
        number = self.get_paginate_by(None)
        count = self.get_queryset().count()
        count_start = 1
        if number > count:
            count_end = count
        else:
            count_end = number
        if count_end == 0:
            count_start = 0
        context['table'] = {
            'number': self.get_paginate_by(None),
            'sort': sort,
            'search': TableSearch.objects.filter(url=self.request.path, company=auth_login.company, shop=None, manager=self.request.user).first(),
            'count': count,
            'count_start': count_start,
            'count_end': count_end,
        }
        return context

class ShopBaseLisView(MultipleObjectMixin, ShopBaseView):
    def get_paginate_by(self, queryset):
        number = 5
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        table_number = TableNumber.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if table_number:
            number = table_number.number
        return number

    def get_queryset(self):
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        query = Q(shop=auth_login.shop)
        if 'flow' in self.request.path:
            query.add(Q(delete_flg=False), Q.AND)

        search = TableSearch.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if search:
            search_query = Q()
            for search_item in self.search_target:
                search_query.add(Q(**{search_item + '__icontains': search.text}), Q.OR)
            query.add(search_query, Q.AND)
            
        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if sort:
            if sort.target == 'shop_template_text_item__text':
                if sort.sort == 1:
                    return self.model.objects.filter(query, Q(shop_template_text_item__number=1)).order_by('-favorite_flg', sort.target, self.default_sort).all()
                elif sort.sort == 2:
                    return self.model.objects.filter(query, Q(shop_template_text_item__number=1)).order_by('-favorite_flg', '-'+sort.target, self.default_sort).all()
                else:
                    return self.model.objects.filter(query).order_by('-favorite_flg', self.default_sort).all()
            else:
                if sort.sort == 1:
                    return self.model.objects.filter(query).order_by('-favorite_flg', sort.target, self.default_sort).all()
                elif sort.sort == 2:
                    return self.model.objects.filter(query).order_by('-favorite_flg', '-'+sort.target, self.default_sort).all()
                else:
                    return self.model.objects.filter(query).order_by('-favorite_flg', self.default_sort).all()
        else:
            return self.model.objects.filter(query).order_by('-favorite_flg', self.default_sort).all()
    
    def get_context_data(self, *args, **kwargs):
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context = super().get_context_data(*args, **kwargs)
        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if not sort:
            if '-' in self.default_sort:
                sort = {
                    'target': self.default_sort.replace('-', ''),
                    'sort': 2,
                }
            else:
                sort = {
                    'target': self.default_sort,
                    'sort': 1,
                }
        
        number = self.get_paginate_by(None)
        count = self.get_queryset().count()
        count_start = 1
        if number > count:
            count_end = count
        else:
            count_end = number
        if count_end == 0:
            count_start = 0
        context['table'] = {
            'number': self.get_paginate_by(None),
            'sort': sort,
            'search': TableSearch.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first(),
            'count': count,
            'count_start': count_start,
            'count_end': count_end,
        }
        return context

class UserBaseLisView(MultipleObjectMixin, ShopBaseView):
    def get_paginate_by(self, queryset):
        number = 5
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        table_number = TableNumber.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if table_number:
            number = table_number.number
        return number

    def get_queryset(self):
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        query = Q(shop=auth_login.shop)

        search = TableSearch.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).all()
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
        
        query_list = list()
        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        flow = UserFlow.objects.filter(user=OuterRef('pk'), end_flg=False).order_by('flow_tab__number').values("flow_tab__number", "flow_tab__name")
        alert = UserAlert.objects.filter(user=OuterRef('pk')).order_by('-status').values("status")
        if search_tag:
            tag = UserHashTag.objects.filter(user=OuterRef('pk'), tag__display_id__in=search_tag).order_by('-created_at').values("tag__display_id")
        else:
            tag = UserHashTag.objects.filter(user=OuterRef('pk'), tag__display_id__in=list()).order_by('-created_at').values("tag__display_id")
        if sort:
            if sort.target == 'user_flow__number':
                if sort.sort == 1:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow=Subquery(flow.values('flow_tab__number')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=False)).order_by('alert', 'status', 'active_flow', self.default_sort).all()
                elif sort.sort == 2:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow=Subquery(flow.values('flow_tab__number')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=False)).order_by('alert', '-status', '-active_flow', self.default_sort).all()
                else:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=False)).order_by('alert', self.default_sort).all()
            else:
                if sort.sort == 1:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=False)).order_by('alert', sort.target, self.default_sort).all()
                elif sort.sort == 2:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=False)).order_by('alert', '-'+sort.target, self.default_sort).all()
                else:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=False)).order_by('alert', self.default_sort).all()
        else:
            query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=False)).order_by('alert', self.default_sort).all()

        for query_index, query_item in enumerate(query_list):
            query_list[query_index].active_flow = UserFlow.objects.filter(user=query_item, end_flg=False).order_by('flow_tab__number').first()
            query_list[query_index].tag = UserHashTag.objects.filter(user=query_item).order_by('number').all()
            query_list[query_index].alert = UserAlert.objects.filter(user=query_item).order_by('number').first()
        return query_list

    
    def get_context_data(self, *args, **kwargs):
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context = super().get_context_data(*args, **kwargs)
        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if not sort:
            if '-' in self.default_sort:
                sort = {
                    'target': self.default_sort.replace('-', ''),
                    'sort': 2,
                }
            else:
                sort = {
                    'target': self.default_sort,
                    'sort': 1,
                }
        
        number = self.get_paginate_by(None)
        count = self.get_queryset().count()
        count_start = 1
        if number > count:
            count_end = count
        else:
            count_end = number
        if count_end == 0:
            count_start = 0

        search = {}
        for search_item in TableSearch.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).order_by('created_at').all():
            search[search_item.item] = search_item.text
            if search_item.item == 'age_from':
                if 'age' in search:
                    search['age'] = search_item.text + search['age']
                else:
                    search['age'] = search_item.text + ' ～ '
            if search_item.item == 'age_to':
                if 'age' in search:
                    search['age'] = search['age'] + search_item.text
                else:
                    search['age'] = ' ～ ' + search_item.text
            if search_item.item == 'date_from':
                if 'date' in search:
                    search['date'] = search_item.text + search['date']
                else:
                    search['date'] = search_item.text + ' ～ '
            if search_item.item == 'date_to':
                if 'date' in search:
                    search['date'] = search['date'] + search_item.text
                else:
                    search['date'] = ' ～ ' + search_item.text
            if search_item.item == 'id_from':
                if 'id' in search:
                    search['id'] = search_item.text + search['id']
                else:
                    search['id'] = search_item.text + ' ～ '
            if search_item.item == 'id_to':
                if 'id' in search:
                    search['id'] = search['id'] + search_item.text
                else:
                    search['id'] = ' ～ ' + search_item.text
            if search_item.item == 'tag':
                for tag_index, tag_value in enumerate(search_item.text.split(",")):
                    if tag_index == 0:
                        if ShopTag.objects.filter(display_id=tag_value).exists():
                            search['tag_all'] = ShopTag.objects.filter(display_id=tag_value).first().name
                    else:
                        if ShopTag.objects.filter(display_id=tag_value).exists():
                            search['tag_all'] = search['tag_all'] + ', ' + ShopTag.objects.filter(display_id=tag_value).first().name
            if search_item.item == 'flow':
                context['flow_list'] = list()
                for flow in HeadFlow.objects.order_by('-created_at').all():
                    flow_tab_list = flow.description.split('→')
                    for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
                        if flow_tab_index != 0:
                            flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                            if not flow_chart_name in context['flow_list']:
                                context['flow_list'].append(flow_chart_name)
                for flow_index, flow_value in enumerate(search_item.text.split(",")):
                    if flow_index == 0:
                        search['flow_all'] = context['flow_list'][int(flow_value)-1]
                    else:
                        search['flow_all'] = search['flow_all'] + ', ' + context['flow_list'][int(flow_value)-1]
        context['table'] = {
            'number': self.get_paginate_by(None),
            'sort': sort,
            'search': search,
            'count': count,
            'count_start': count_start,
            'count_end': count_end,
        }
        return context

class TempBaseLisView(MultipleObjectMixin, ShopBaseView):
    def get_paginate_by(self, queryset):
        number = 5
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        table_number = TableNumber.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if table_number:
            number = table_number.number
        return number

    def get_queryset(self):
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        query = Q(shop=auth_login.shop)

        search = TableSearch.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).all()
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
        
        query_list = list()
        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        flow = UserFlow.objects.filter(user=OuterRef('pk'), end_flg=False).order_by('flow_tab__number').values("flow_tab__number", "flow_tab__name")
        alert = UserAlert.objects.filter(user=OuterRef('pk')).order_by('-status').values("status")
        if search_tag:
            tag = UserHashTag.objects.filter(user=OuterRef('pk'), tag__display_id__in=search_tag).order_by('-created_at').values("tag__display_id")
        else:
            tag = UserHashTag.objects.filter(user=OuterRef('pk'), tag__display_id__in=list()).order_by('-created_at').values("tag__display_id")
        if sort:
            if sort.target == 'user_flow__number':
                if sort.sort == 1:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow=Subquery(flow.values('flow_tab__number')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=True)).order_by('alert', 'status', 'active_flow', self.default_sort).all()
                elif sort.sort == 2:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow=Subquery(flow.values('flow_tab__number')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=True)).order_by('alert', '-status', '-active_flow', self.default_sort).all()
                else:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=True)).order_by('alert', self.default_sort).all()
            else:
                if sort.sort == 1:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=True)).order_by('alert', sort.target, self.default_sort).all()
                elif sort.sort == 2:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=True)).order_by('alert', '-'+sort.target, self.default_sort).all()
                else:
                    query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=True)).order_by('alert', self.default_sort).all()
        else:
            query_list = self.model.objects.annotate(alert=Subquery(alert.values('status')[:1]), active_flow_name=Subquery(flow.values('flow_tab__name')[:1]), all_tag=Subquery(tag.values('tag__display_id')[:1])).filter(query, Q(proxy_flg=True)).order_by('alert', self.default_sort).all()

        for query_index, query_item in enumerate(query_list):
            query_list[query_index].active_flow = UserFlow.objects.filter(user=query_item, end_flg=False).order_by('flow_tab__number').first()
            query_list[query_index].tag = UserHashTag.objects.filter(user=query_item).order_by('number').all()
            query_list[query_index].alert = UserAlert.objects.filter(user=query_item).order_by('number').first()
        return query_list

    
    def get_context_data(self, *args, **kwargs):
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context = super().get_context_data(*args, **kwargs)
        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if not sort:
            if '-' in self.default_sort:
                sort = {
                    'target': self.default_sort.replace('-', ''),
                    'sort': 2,
                }
            else:
                sort = {
                    'target': self.default_sort,
                    'sort': 1,
                }
        
        number = self.get_paginate_by(None)
        count = self.get_queryset().count()
        count_start = 1
        if number > count:
            count_end = count
        else:
            count_end = number
        if count_end == 0:
            count_start = 0
        
        search = {}
        for search_item in TableSearch.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).order_by('created_at').all():
            search[search_item.item] = search_item.text
            if search_item.item == 'age_from':
                if 'age' in search:
                    search['age'] = search_item.text + search['age']
                else:
                    search['age'] = search_item.text + ' ～ '
            if search_item.item == 'age_to':
                if 'age' in search:
                    search['age'] = search['age'] + search_item.text
                else:
                    search['age'] = ' ～ ' + search_item.text
            if search_item.item == 'date_from':
                if 'date' in search:
                    search['date'] = search_item.text + search['date']
                else:
                    search['date'] = search_item.text + ' ～ '
            if search_item.item == 'date_to':
                if 'date' in search:
                    search['date'] = search['date'] + search_item.text
                else:
                    search['date'] = ' ～ ' + search_item.text
            if search_item.item == 'id_from':
                if 'id' in search:
                    search['id'] = search_item.text + search['id']
                else:
                    search['id'] = search_item.text + ' ～ '
            if search_item.item == 'id_to':
                if 'id' in search:
                    search['id'] = search['id'] + search_item.text
                else:
                    search['id'] = ' ～ ' + search_item.text
            if search_item.item == 'tag':
                for tag_index, tag_value in enumerate(search_item.text.split(",")):
                    if tag_index == 0:
                        if ShopTag.objects.filter(display_id=tag_value).exists():
                            search['tag_all'] = ShopTag.objects.filter(display_id=tag_value).first().name
                    else:
                        if ShopTag.objects.filter(display_id=tag_value).exists():
                            search['tag_all'] = search['tag_all'] + ', ' + ShopTag.objects.filter(display_id=tag_value).first().name
            if search_item.item == 'flow':
                context['flow_list'] = list()
                for flow in HeadFlow.objects.order_by('-created_at').all():
                    flow_tab_list = flow.description.split('→')
                    for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
                        if flow_tab_index != 0:
                            flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                            if not flow_chart_name in context['flow_list']:
                                context['flow_list'].append(flow_chart_name)
                for flow_index, flow_value in enumerate(search_item.text.split(",")):
                    if flow_index == 0:
                        search['flow_all'] = context['flow_list'][int(flow_value)-1]
                    else:
                        search['flow_all'] = search['flow_all'] + ', ' + context['flow_list'][int(flow_value)-1]
        context['table'] = {
            'number': self.get_paginate_by(None),
            'sort': sort,
            'search': search,
            'count': count,
            'count_start': count_start,
            'count_end': count_end,
        }
        return context

class HeadListView(MultipleObjectTemplateResponseMixin, BaseListView, HeadBaseLisView):
    pass

class CompanyListView(MultipleObjectTemplateResponseMixin, BaseListView, CompanyBaseLisView):
    pass

class ShopListView(MultipleObjectTemplateResponseMixin, BaseListView, ShopBaseLisView):
    pass

class UserListView(MultipleObjectTemplateResponseMixin, BaseListView, UserBaseLisView):
    pass

class TempListView(MultipleObjectTemplateResponseMixin, BaseListView, TempBaseLisView):
    pass