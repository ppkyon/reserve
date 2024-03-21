from django.conf import settings
from django.db.models import Q
from django.views.generic import TemplateView
from django.views.generic.list import MultipleObjectMixin, MultipleObjectTemplateResponseMixin, BaseListView

from sign.mixins import HeadLoginMixin, CompanyLoginMixin, ShopLoginMixin

from sign.models import AuthUser, CompanyProfile, ShopProfile, ManagerProfile, AuthLogin
from table.models import TableNumber, TableSort, TableSearch

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

        image = None
        name = None
        if not self.request.user.is_anonymous:
            auth_login = AuthLogin.objects.filter(user=self.request.user).first()
            if auth_login:
                shop = auth_login.shop
                shop_profile = ShopProfile.objects.filter(shop=shop).first()
                if shop_profile:
                    image = shop_profile.shop_logo_image.url
                    name = shop_profile.shop_name
        
        context['side'] = {
            'logo_image': image,
            'logo_name': name,
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
                return self.model.objects.filter(query).order_by(sort.target, self.default_sort).distinct().all()
            if sort.sort == 2:
                return self.model.objects.filter(query).order_by('-'+sort.target, self.default_sort).distinct().all()
            else:
                return self.model.objects.filter(query).order_by(self.default_sort).distinct().all()
        else:
            return self.model.objects.filter(query).order_by(self.default_sort).distinct().all()

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
                return self.model.objects.filter(query).order_by(sort.target, self.default_sort).distinct().all()
            if sort.sort == 2:
                return self.model.objects.filter(query).order_by('-'+sort.target, self.default_sort).distinct().all()
            else:
                return self.model.objects.filter(query).order_by(self.default_sort).distinct().all()
        else:
            return self.model.objects.filter(query).order_by(self.default_sort).distinct().all()
    
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
        query = Q()
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
            if sort.sort == 1:
                return self.model.objects.filter(query).order_by('-favorite_flg', sort.target, self.default_sort).distinct().all()
            if sort.sort == 2:
                return self.model.objects.filter(query).order_by('-favorite_flg', '-'+sort.target, self.default_sort).distinct().all()
            else:
                return self.model.objects.filter(query).order_by('-favorite_flg', self.default_sort).distinct().all()
        else:
            return self.model.objects.filter(query).order_by('-favorite_flg', self.default_sort).distinct().all()
    
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

class HeadListView(MultipleObjectTemplateResponseMixin, BaseListView, HeadBaseLisView):
    pass

class CompanyListView(MultipleObjectTemplateResponseMixin, BaseListView, CompanyBaseLisView):
    pass

class ShopListView(MultipleObjectTemplateResponseMixin, BaseListView, ShopBaseLisView):
    pass