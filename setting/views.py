from view import ShopView

from setting.models import ShopOffline, ShopOfflineTime, ShopOnline, ShopOnlineTime, ManagerOffline, ManagerOfflineTime, ManagerOnline, ManagerOnlineTime
from sign.models import AuthUser, ShopLine, ManagerProfile
from table.models import TableSearch

from itertools import chain
from line.data import get_info

import phonenumbers

class IndexView(ShopView):
    template_name = 'setting/index.html'
    title = '設定'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        context['offline_list'] = ShopOffline.objects.filter(shop=self.request.shop).order_by('created_at').all()
        for offline_index, offline_item in enumerate(context['offline_list']):
            context['offline_list'][offline_index].time = ShopOfflineTime.objects.filter(offline=offline_item).order_by('week').all()
        context['online_list'] = ShopOnline.objects.filter(shop=self.request.shop).order_by('created_at').all()
        for online_index, online_item in enumerate(context['online_list']):
            context['online_list'][online_index].time = ShopOnlineTime.objects.filter(online=online_item).order_by('week').all()
        context['online_offline_list'] = list(chain(context['offline_list'], context['online_list']))

        context['search_setting'] = None
        if TableSearch.objects.filter(url=self.request.path, manager=self.request.user).exists():
            search = TableSearch.objects.filter(url=self.request.path, manager=self.request.user).first().text
            if ShopOffline.objects.filter(display_id=search).exists():
                context['search_setting'] = ShopOffline.objects.filter(display_id=search).first()
            if ShopOnline.objects.filter(display_id=search).exists():
                context['search_setting'] = ShopOnline.objects.filter(display_id=search).first()
        if not context['search_setting']:
            for online_offline_item in context['online_offline_list']:
                context['search_setting'] = online_offline_item
                break

        context['manager'] = self.request.user
        context['manager'].profile = ManagerProfile.objects.filter(manager=context['manager']).first()
        if context['manager'].profile and context['manager'].profile.phone_number:
            context['manager'].profile.phone_number = phonenumbers.format_number(phonenumbers.parse(context['manager'].profile.phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
        if context['search_setting']:
            if ShopOfflineTime.objects.filter(offline__id=context['search_setting'].id).exists():
                if ManagerOffline.objects.filter(manager=self.request.user, offline__id=context['search_setting'].id).exists():
                    context['manager'].setting = ManagerOfflineTime.objects.filter(offline=ManagerOffline.objects.filter(manager=self.request.user, offline__id=context['search_setting'].id).first()).order_by('week').all()
                else:
                    context['manager'].setting = ShopOfflineTime.objects.filter(offline__id=context['search_setting'].id).order_by('week', 'number').all()
            if ShopOnlineTime.objects.filter(online__id=context['search_setting'].id).exists():
                if ManagerOnline.objects.filter(manager=self.request.user, online__id=context['search_setting'].id).exists():
                    context['manager'].setting = ManagerOnlineTime.objects.filter(online=ManagerOnline.objects.filter(manager=self.request.user, online__id=context['search_setting'].id).first()).order_by('week').all()
                else:
                    context['manager'].setting = ShopOnlineTime.objects.filter(online__id=context['search_setting'].id).order_by('week', 'number').all()

        context['manager_list'] = AuthUser.objects.filter(shop=self.request.shop, status__gt=0, head_flg=False, delete_flg=False).order_by('created_at').all()
        for manager_index, manager_item in enumerate(context['manager_list']):
            context['manager_list'][manager_index].profile = ManagerProfile.objects.filter(manager_id=manager_item.id).first()
            context['manager_list'][manager_index].author_profile = ManagerProfile.objects.filter(manager_id=manager_item.author).first()
            if context['manager_list'][manager_index].profile and context['manager_list'][manager_index].profile.phone_number:
                context['manager_list'][manager_index].profile.phone_number = phonenumbers.format_number(phonenumbers.parse(context['manager_list'][manager_index].profile.phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
            if context['search_setting']:
                if ShopOfflineTime.objects.filter(offline__id=context['search_setting'].id).exists():
                    if ManagerOffline.objects.filter(manager=self.request.user, offline__id=context['search_setting'].id).exists():
                        context['manager_list'][manager_index].setting = ManagerOfflineTime.objects.filter(offline=ManagerOffline.objects.filter(manager=self.request.user, offline__id=context['search_setting'].id).first()).order_by('week').all()
                    else:
                        context['manager_list'][manager_index].setting = ShopOfflineTime.objects.filter(offline__id=context['search_setting'].id).order_by('week', 'number').all()
                if ShopOnlineTime.objects.filter(online__id=context['search_setting'].id).exists():
                    if ManagerOnline.objects.filter(manager=self.request.user, online__id=context['search_setting'].id).exists():
                        context['manager_list'][manager_index].setting = ManagerOnlineTime.objects.filter(online=ManagerOnline.objects.filter(manager=self.request.user, online__id=context['search_setting'].id).first()).order_by('week').all()
                    else:
                        context['manager_list'][manager_index].setting = ShopOnlineTime.objects.filter(online__id=context['search_setting'].id).order_by('week', 'number').all()

        context['shop'] = self.request.shop
        context['shop'].line = ShopLine.objects.filter(shop=context['shop']).first()
        
        context['line_info'] = get_info(self.request.shop)
        context['age_list'] = [i for i in range(101)]
        return context