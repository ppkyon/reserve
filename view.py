from django.conf import settings
from django.db.models import Q, Subquery, OuterRef
from django.views.generic import TemplateView
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin, BaseListView

from sign.mixins import HeadLoginMixin, CompanyLoginMixin, ShopLoginMixin

from flow.models import ShopFlow, UserFlow
from setting.models import SettingAlert
from sign.models import AuthUser, CompanyProfile, ShopProfile, ManagerProfile, AuthLogin
from table.models import TableNumber, TableSort, TableSearch
from tag.models import UserHashTag
from user.models import LineUser

from dateutil.relativedelta import relativedelta

import datetime
import environ

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
                if shop_flow.period_to and shop_flow.period_to <= datetime.datetime.now() and flow < 3:
                    flow = 3
                elif shop_flow.period_to and shop_flow.period_to <= datetime.datetime.now() + relativedelta(days=+10) and flow < 2:
                    flow = 2
                alert = {
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
        
        query_list = list()
        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if sort:
            if sort.target == 'user_flow__number':
                if sort.sort == 1:
                    sub = UserFlow.objects.filter(user=OuterRef('pk'), end_flg=True).order_by('-number').values("number")
                    query_list = self.model.objects.annotate(active_flow=Subquery(sub.values('id')[:1])).filter(query, Q(proxy_flg=False)).order_by('active_flow', self.default_sort).all()
                elif sort.sort == 2:
                    sub = UserFlow.objects.filter(user=OuterRef('pk'), end_flg=True).order_by('-number').values("number")
                    query_list = self.model.objects.annotate(active_flow=Subquery(sub.values('id')[:1])).filter(query, Q(proxy_flg=False)).order_by('-active_flow', self.default_sort).all()
                else:
                    query_list = self.model.objects.filter(query, Q(proxy_flg=False)).order_by(self.default_sort).all()
            else:
                if sort.sort == 1:
                    query_list = self.model.objects.filter(query, Q(proxy_flg=False)).order_by(sort.target, self.default_sort).all()
                elif sort.sort == 2:
                    query_list = self.model.objects.filter(query, Q(proxy_flg=False)).order_by('-'+sort.target, self.default_sort).all()
                else:
                    query_list = self.model.objects.filter(query, Q(proxy_flg=False)).order_by(self.default_sort).all()
        else:
            query_list = self.model.objects.filter(query, Q(proxy_flg=False)).order_by(self.default_sort).all()

        for query_index, query_item in enumerate(query_list):
            query_list[query_index].active_flow = UserFlow.objects.filter(user=query_item, end_flg=False).order_by('flow_tab__number').first()
            query_list[query_index].tag = UserHashTag.objects.filter(user=query_item).order_by('number').all()
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
        context['table'] = {
            'number': self.get_paginate_by(None),
            'sort': sort,
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
        
        query_list = list()
        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.company, shop=auth_login.shop, manager=self.request.user).first()
        if sort:
            if sort.target == 'user_flow__number':
                if sort.sort == 1:
                    sub = UserFlow.objects.filter(user=OuterRef('pk'), end_flg=True).order_by('-number').values("number")
                    query_list = self.model.objects.annotate(active_flow=Subquery(sub.values('id')[:1])).filter(query, Q(proxy_flg=True)).order_by('active_flow', self.default_sort).all()
                elif sort.sort == 2:
                    sub = UserFlow.objects.filter(user=OuterRef('pk'), end_flg=True).order_by('-number').values("number")
                    query_list = self.model.objects.annotate(active_flow=Subquery(sub.values('id')[:1])).filter(query, Q(proxy_flg=True)).order_by('-active_flow', self.default_sort).all()
                else:
                    query_list = self.model.objects.filter(query, Q(proxy_flg=True)).order_by(self.default_sort).all()
            else:
                if sort.sort == 1:
                    query_list = self.model.objects.filter(query, Q(proxy_flg=True)).order_by(sort.target, self.default_sort).all()
                elif sort.sort == 2:
                    query_list = self.model.objects.filter(query, Q(proxy_flg=True)).order_by('-'+sort.target, self.default_sort).all()
                else:
                    query_list = self.model.objects.filter(query, Q(proxy_flg=True)).order_by(self.default_sort).all()
        else:
            query_list = self.model.objects.filter(query, Q(proxy_flg=True)).order_by(self.default_sort).all()

        for query_index, query_item in enumerate(query_list):
            query_list[query_index].active_flow = UserFlow.objects.filter(user=query_item, end_flg=False).order_by('flow_tab__number').first()
            query_list[query_index].tag = UserHashTag.objects.filter(user=query_item).order_by('number').all()
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
        context['table'] = {
            'number': self.get_paginate_by(None),
            'sort': sort,
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