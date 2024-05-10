from django.shortcuts import redirect

from view import ShopView

from flow.models import HeadFlow
from reserve.models import (
    ReserveBasic, ReserveOfflinePlace, ReserveOnlinePlace, ReserveOfflineCourse, ReserveOnlineCourse,
    ReserveOfflineSetting, ReserveOnlineSetting, ReserveOnlineMeeting, ReserveOfflineFacility, ReserveOnlineFacility,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu, ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
)
from setting.models import ShopOffline, ShopOfflineTime, ShopOnline, ShopOnlineTime
from sign.models import AuthLogin, AuthUser, ManagerProfile

from itertools import chain

import random
import re

class IndexView(ShopView):
    def get(self, request, **kwargs):
        return redirect('/reserve/basic/')

class BasicView(ShopView):
    template_name = 'reserve/basic.html'
    title = '予約設定'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['basic_data'] = ReserveBasic.objects.filter(shop=auth_login.shop).first()
        return context

class PlaceView(ShopView):
    template_name = 'reserve/place.html'
    title = '予約設定'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['offline_place'] = ReserveOfflinePlace.objects.filter(shop=auth_login.shop).first()
        context['offline_course'] = ReserveOfflineCourse.objects.filter(shop=auth_login.shop).order_by('number').all()
        context['online_place'] = ReserveOnlinePlace.objects.filter(shop=auth_login.shop).first()
        context['online_course'] = ReserveOnlineCourse.objects.filter(shop=auth_login.shop).order_by('number').all()
        return context

class SettingView(ShopView):
    template_name = 'reserve/setting.html'
    title = '予約設定'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()

        context['basic_data'] = ReserveBasic.objects.filter(shop=auth_login.shop).first()
        context['offline_list'] = ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for offline_index, offline_item in enumerate(context['offline_list']):
            context['offline_list'][offline_index].type = 1
            context['offline_list'][offline_index].time = ShopOfflineTime.objects.filter(offline=offline_item).order_by('week').all()
        context['online_list'] = ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for online_index, online_item in enumerate(context['online_list']):
            context['online_list'][online_index].type = 2
            context['online_list'][online_index].time = ShopOnlineTime.objects.filter(online=online_item).order_by('week').all()
        context['online_offline_list'] = list(chain(context['offline_list'], context['online_list']))
        for online_offline_index, online_offline_item in enumerate(context['online_offline_list']):
            context['online_offline_list'][online_offline_index].random = random.randint(10000000,99999999)
            if ShopOffline.objects.filter(id=online_offline_item.id).exists():
                context['online_offline_list'][online_offline_index].setting = ReserveOfflineSetting.objects.filter(offline=online_offline_item).order_by('number').all()
                context['online_offline_list'][online_offline_index].setting_count = ReserveOfflineSetting.objects.filter(offline=online_offline_item).count()
                for setting_index, setting_item in enumerate(context['online_offline_list'][online_offline_index].setting):
                    if setting_item.advance:
                        context['online_offline_list'][online_offline_index].setting[setting_index].advance = ReserveOfflineSetting.objects.filter(display_id=setting_item.advance).first()
            if ShopOnline.objects.filter(id=online_offline_item.id).exists():
                context['online_offline_list'][online_offline_index].setting = ReserveOnlineSetting.objects.filter(online=online_offline_item).order_by('number').all()
                context['online_offline_list'][online_offline_index].setting_count = ReserveOnlineSetting.objects.filter(online=online_offline_item).count()
                for setting_index, setting_item in enumerate(context['online_offline_list'][online_offline_index].setting):
                    context['online_offline_list'][online_offline_index].setting[setting_index].random = random.randint(10000000,99999999)
                    context['online_offline_list'][online_offline_index].setting[setting_index].meeting = ReserveOnlineMeeting.objects.filter(online=setting_item).order_by('number').all()
                    if setting_item.advance:
                        context['online_offline_list'][online_offline_index].setting[setting_index].advance = ReserveOnlineSetting.objects.filter(display_id=setting_item.advance).first()
        return context

class FacilityView(ShopView):
    template_name = 'reserve/facility.html'
    title = '予約設定'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['offline_list'] = ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for offline_index, offline_item in enumerate(context['offline_list']):
            context['offline_list'][offline_index].type = 1
            context['offline_list'][offline_index].time = ShopOfflineTime.objects.filter(offline=offline_item).order_by('week').all()
        context['online_list'] = ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for online_index, online_item in enumerate(context['online_list']):
            context['online_list'][online_index].type = 2
            context['online_list'][online_index].time = ShopOnlineTime.objects.filter(online=online_item).order_by('week').all()
        context['online_offline_list'] = list(chain(context['offline_list'], context['online_list']))
        for online_offline_index, online_offline_item in enumerate(context['online_offline_list']):
            context['online_offline_list'][online_offline_index].random = random.randint(10000000,99999999)
            if ShopOffline.objects.filter(id=online_offline_item.id).exists():
                context['online_offline_list'][online_offline_index].facility = ReserveOfflineFacility.objects.filter(offline=online_offline_item).order_by('number').all()
                context['online_offline_list'][online_offline_index].facility_count = ReserveOfflineFacility.objects.filter(offline=online_offline_item).count()
            if ShopOnline.objects.filter(id=online_offline_item.id).exists():
                context['online_offline_list'][online_offline_index].facility = ReserveOnlineFacility.objects.filter(online=online_offline_item).order_by('number').all()
                context['online_offline_list'][online_offline_index].facility_count = ReserveOnlineFacility.objects.filter(online=online_offline_item).count()
        return context

class MenuView(ShopView):
    template_name = 'reserve/menu.html'
    title = '予約設定'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['offline_list'] = ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for offline_index, offline_item in enumerate(context['offline_list']):
            context['offline_list'][offline_index].type = 1
            context['offline_list'][offline_index].time = ShopOfflineTime.objects.filter(offline=offline_item).order_by('week').all()
        context['online_list'] = ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for online_index, online_item in enumerate(context['online_list']):
            context['online_list'][online_index].type = 2
            context['online_list'][online_index].time = ShopOnlineTime.objects.filter(online=online_item).order_by('week').all()
        context['online_offline_list'] = list(chain(context['offline_list'], context['online_list']))

        context['manager_list'] = AuthUser.objects.filter(shop=auth_login.shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all()
        for manager_index, manager_item in enumerate(context['manager_list']):
            context['manager_list'][manager_index].profile = ManagerProfile.objects.filter(manager_id=manager_item.id).first()

        context['facility_list'] = list()
        for online_offline_index, online_offline_item in enumerate(context['online_offline_list']):
            if ShopOffline.objects.filter(id=online_offline_item.id).exists():
                for facility_item in ReserveOfflineFacility.objects.filter(offline=online_offline_item).order_by('number').all():
                    context['facility_list'].append(facility_item)
            if ShopOnline.objects.filter(id=online_offline_item.id).exists():
                for facility_item in ReserveOnlineFacility.objects.filter(online=online_offline_item).order_by('number').all():
                    context['facility_list'].append(facility_item)
            
        context['flow_list'] = list()
        for flow in HeadFlow.objects.order_by('-created_at').all():
            flow_tab_list = flow.description.split('→')
            for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
                if flow_tab_index != 0:
                    flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                    if not flow_chart_name in context['flow_list']:
                        context['flow_list'].append(flow_chart_name)
                    
        for online_offline_index, online_offline_item in enumerate(context['online_offline_list']):
            if ShopOffline.objects.filter(id=online_offline_item.id).exists():
                context['online_offline_list'][online_offline_index].setting = ReserveOfflineSetting.objects.filter(offline=online_offline_item,).order_by('number').all()
                context['online_offline_list'][online_offline_index].setting_count = ReserveOfflineSetting.objects.filter(offline=online_offline_item).count()
                context['online_offline_list'][online_offline_index].facility = ReserveOfflineFacility.objects.filter(offline=online_offline_item).order_by('number').all()
                context['online_offline_list'][online_offline_index].facility_count = ReserveOfflineFacility.objects.filter(offline=online_offline_item).count()

                for setting_index, setting_item in enumerate(context['online_offline_list'][online_offline_index].setting):
                    context['online_offline_list'][online_offline_index].setting[setting_index].manager = list()
                    context['online_offline_list'][online_offline_index].setting[setting_index].facility = list()
                    context['online_offline_list'][online_offline_index].setting[setting_index].flow = list()

                    for manager_index, manager_item in enumerate(context['manager_list']):
                        context['online_offline_list'][online_offline_index].setting[setting_index].manager.append({'index': manager_item.display_id, 'manager': manager_item.display_id, 'menu_flg': ReserveOfflineManagerMenu.objects.filter(shop=auth_login.shop, offline=setting_item, manager=manager_item).exists()})
                    for facility_index, facility_item in enumerate(context['facility_list']):
                        context['online_offline_list'][online_offline_index].setting[setting_index].facility.append({'index': facility_item.display_id, 'facility': facility_item.offline.id, 'menu_flg': ReserveOfflineFacilityMenu.objects.filter(shop=auth_login.shop, offline=setting_item, facility=facility_item).exists()})
                    for flow_index, flow_item in enumerate(context['flow_list']):
                        context['online_offline_list'][online_offline_index].setting[setting_index].flow.append({'index': (flow_index+1), 'flow': flow_item, 'menu_flg': ReserveOfflineFlowMenu.objects.filter(shop=auth_login.shop, offline=setting_item, flow=flow_item).exists()})
            if ShopOnline.objects.filter(id=online_offline_item.id).exists():
                context['online_offline_list'][online_offline_index].setting = ReserveOnlineSetting.objects.filter(online=online_offline_item).order_by('number').all()
                context['online_offline_list'][online_offline_index].setting_count = ReserveOnlineSetting.objects.filter(online=online_offline_item).count()
                context['online_offline_list'][online_offline_index].facility = ReserveOnlineFacility.objects.filter(online=online_offline_item).order_by('number').all()
                context['online_offline_list'][online_offline_index].facility_count = ReserveOnlineFacility.objects.filter(online=online_offline_item).count()

                for setting_index, setting_item in enumerate(context['online_offline_list'][online_offline_index].setting):
                    context['online_offline_list'][online_offline_index].setting[setting_index].manager = list()
                    context['online_offline_list'][online_offline_index].setting[setting_index].facility = list()
                    context['online_offline_list'][online_offline_index].setting[setting_index].flow = list()

                    for manager_index, manager_item in enumerate(context['manager_list']):
                        context['online_offline_list'][online_offline_index].setting[setting_index].manager.append({'index': manager_item.display_id, 'manager': manager_item.display_id, 'menu_flg': ReserveOnlineManagerMenu.objects.filter(shop=auth_login.shop, online=setting_item, manager=manager_item).exists()})
                    for facility_index, facility_item in enumerate(context['facility_list']):
                        context['online_offline_list'][online_offline_index].setting[setting_index].facility.append({'index': facility_item.display_id, 'facility': facility_item.offline.id, 'menu_flg': ReserveOnlineFacilityMenu.objects.filter(shop=auth_login.shop, online=setting_item, facility=facility_item).exists()})
                    for flow_index, flow_item in enumerate(context['flow_list']):
                        context['online_offline_list'][online_offline_index].setting[setting_index].flow.append({'index': (flow_index+1), 'flow': flow_item, 'menu_flg': ReserveOnlineFlowMenu.objects.filter(shop=auth_login.shop, online=setting_item, flow=flow_item).exists()})
        return context