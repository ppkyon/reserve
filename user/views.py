from django.shortcuts import redirect

from view import UserView, UserListView

from question.models import UserQuestion
from flow.models import HeadFlow, ShopFlowTab, UserFlow, UserFlowSchedule
from reserve.models import (
    ReserveOfflineSetting, ReserveOnlineSetting,
    ReserveOfflineManagerMenu, ReserveOnlineManagerMenu, ReserveOfflineFacilityMenu, ReserveOnlineFacilityMenu, ReserveOfflineFlowMenu, ReserveOnlineFlowMenu
)
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthLogin
from tag.models import ShopTag, UserHashTag
from user.models import LineUser, UserProfile, UserAlert

from itertools import chain

import phonenumbers
import re

class IndexView(UserListView):
    template_name = 'user/index.html'
    title = 'お客様管理'
    model = LineUser
    search_target = ['title', 'name', 'description']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context = super().get_context_data(*args, **kwargs)
        context['age_list'] = [i for i in range(101)]
        context['tag_list'] = ShopTag.objects.filter(genre__shop=auth_login.shop).all()
        for tag_index, tag_item in enumerate(context['tag_list']):
            if 'tag' in context['table']['search'] and str(tag_item.display_id) in context['table']['search']['tag']:
                context['tag_list'][tag_index].check = True
            else:
                context['tag_list'][tag_index].check = False
        context['flow_list'] = list()
        for flow in HeadFlow.objects.order_by('-created_at').all():
            flow_tab_list = flow.description.split('→')
            for flow_tab_index, flow_tab_item in enumerate(flow_tab_list):
                if flow_tab_index != 0:
                    flow_chart_name = re.sub('\(.*?\)','',flow_tab_item).strip()
                    if not flow_chart_name in context['flow_list']:
                        context['flow_list'].append(flow_chart_name)
        context['flow_list'].append('ブロック')
        context['flow_check_list'] = {}
        for flow_index, flow_item in enumerate(context['flow_list']):
            if 'flow' in context['table']['search'] and str(flow_index+1) in context['table']['search']['flow']:
                context['flow_check_list'][flow_item] = True
            else:
                context['flow_check_list'][flow_item] = False
        if 'flow' in context['table']['search'] and str(0) in context['table']['search']['flow']:
            context['flow_check_list']['ブロック'] = True
        else:
            context['flow_check_list']['ブロック'] = False
        return context

class DetailView(UserView):
    template_name = 'user/detail.html'
    title = 'お客様管理 - 詳細 -'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()

        context['user'] = LineUser.objects.filter(shop=auth_login.shop, display_id=self.request.GET.get("id")).first()
        if context['user'].delete_flg:
            return redirect('user:index')
        
        context['user'].profile = UserProfile.objects.filter(user=context['user']).first()
        if context['user'].profile and context['user'].profile.phone_number:
            context['user'].profile.phone_number = phonenumbers.format_number(phonenumbers.parse(context['user'].profile.phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
        
        context['user'].active_flow = UserFlow.objects.filter(user=context['user'], end_flg=False).order_by('flow_tab__number').first()
        context['user'].flow = UserFlow.objects.filter(user=context['user']).order_by('number').all()
        for user_flow_index, user_flow_item in enumerate(context['user'].flow):
            context['user'].flow[user_flow_index].schedule = UserFlowSchedule.objects.filter(flow=user_flow_item, temp_flg=False).exclude(number=0).order_by('number').all()
            for user_flow_schedule_index, user_flow_schedule_item in enumerate(context['user'].flow[user_flow_index].schedule):
                if user_flow_schedule_item.offline:
                    context['user'].flow[user_flow_index].schedule[user_flow_schedule_index].manager_list = ReserveOfflineManagerMenu.objects.filter(shop=auth_login.shop, offline=user_flow_schedule_item.offline).all()
                    context['user'].flow[user_flow_index].schedule[user_flow_schedule_index].facility_list = ReserveOfflineFacilityMenu.objects.filter(shop=auth_login.shop, offline=user_flow_schedule_item.offline).all()
                elif user_flow_schedule_item.online:
                    context['user'].flow[user_flow_index].schedule[user_flow_schedule_index].manager_list = ReserveOnlineManagerMenu.objects.filter(shop=auth_login.shop, online=user_flow_schedule_item.online).all()
                    context['user'].flow[user_flow_index].schedule[user_flow_schedule_index].facility_list = ReserveOnlineFacilityMenu.objects.filter(shop=auth_login.shop, online=user_flow_schedule_item.online).all()
            context['user'].flow[user_flow_index].alert = UserAlert.objects.filter(user=context['user'], number=user_flow_item.number).first()

        context['user'].tag = UserHashTag.objects.filter(user=context['user']).order_by('number').all()

        context['user'].question = UserQuestion.objects.filter(user=context['user']).order_by('-created_at').all()

        context['setting_list'] = list()
        for user_flow_index, user_flow_item in enumerate(context['user'].flow):
            if not user_flow_item.end_flg:
                for user_flow_schedule_item in UserFlowSchedule.objects.filter(flow=user_flow_item, temp_flg=False).exclude(number=0).order_by('number').all():
                    if user_flow_schedule_item.join == 0:
                        if user_flow_schedule_item.offline:
                            context['setting_list'].append(user_flow_schedule_item.offline)
                        elif user_flow_schedule_item.online:
                            context['setting_list'].append(user_flow_schedule_item.online)
        
        context['menu_list'] = list()
        user_flow = UserFlow.objects.filter(user=context['user']).first()
        offline_list = ShopOffline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for offline_index, offline_item in enumerate(offline_list):
            offline_list[offline_index].type = 1
        online_list = ShopOnline.objects.filter(shop=auth_login.shop).order_by('created_at').all()
        for online_index, online_item in enumerate(online_list):
            online_list[online_index].type = 2
        online_offline_list = list(chain(offline_list, online_list))
        if context['user'].member_flg:
            for flow_tab in ShopFlowTab.objects.filter(flow=user_flow.flow, member=1).order_by('number').all():
                check_flow = UserFlow.objects.filter(user=user_flow.user, flow_tab=flow_tab).first()
                if not check_flow:
                    for online_offline_item in online_offline_list:
                        if online_offline_item.type == 1:
                            setting = ReserveOfflineSetting.objects.filter(offline=online_offline_item, display_flg=True).all()
                            for setting_item in setting:
                                if ReserveOfflineFlowMenu.objects.filter(offline=setting_item, flow=flow_tab.name).exists():
                                    if setting_item.advance:
                                        advance_setting = ReserveOfflineSetting.objects.filter(display_id=setting_item.advance).first()
                                        if advance_setting:
                                            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user_flow.user, offline=advance_setting, temp_flg=False).exclude(number=0).first()
                                            if advance_schedule and advance_schedule.date and advance_schedule.time:
                                                context['menu_list'].append(setting_item)
                                        else:
                                            context['menu_list'].append(setting_item)
                                    else:
                                        context['menu_list'].append(setting_item)
                        elif online_offline_item.type == 2:
                            setting = ReserveOnlineSetting.objects.filter(online=online_offline_item, display_flg=True).all()
                            for setting_item in setting:
                                if ReserveOnlineFlowMenu.objects.filter(online=setting_item, flow=flow_tab.name).exists():
                                    if setting_item.advance:
                                        advance_setting = ReserveOnlineSetting.objects.filter(display_id=setting_item.advance).first()
                                        if advance_setting:
                                            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user_flow.user, online=advance_setting, temp_flg=False).exclude(number=0).first()
                                            if advance_schedule and advance_schedule.date and advance_schedule.time:
                                                context['menu_list'].append(setting_item)
                                        else:
                                            context['menu_list'].append(setting_item)
                                    else:
                                        context['menu_list'].append(setting_item)
        else:
            for flow_tab in ShopFlowTab.objects.filter(flow=user_flow.flow, member=0).order_by('number').all():
                check_flow = UserFlow.objects.filter(user=user_flow.user, flow_tab=flow_tab).first()
                if not check_flow:
                    for online_offline_item in online_offline_list:
                        if online_offline_item.type == 1:
                            setting = ReserveOfflineSetting.objects.filter(offline=online_offline_item, display_flg=True).all()
                            for setting_item in setting:
                                if ReserveOfflineFlowMenu.objects.filter(offline=setting_item, flow=flow_tab.name).exists():
                                    if setting_item.advance:
                                        advance_setting = ReserveOfflineSetting.objects.filter(display_id=setting_item.advance).first()
                                        if advance_setting:
                                            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user_flow.user, offline=advance_setting, temp_flg=False).exclude(number=0).first()
                                            if advance_schedule and advance_schedule.date and advance_schedule.time:
                                                context['menu_list'].append(setting_item)
                                        else:
                                            context['menu_list'].append(setting_item)
                                    else:
                                        context['menu_list'].append(setting_item)
                        elif online_offline_item.type == 2:
                            setting = ReserveOnlineSetting.objects.filter(online=online_offline_item, display_flg=True).all()
                            for setting_item in setting:
                                if ReserveOnlineFlowMenu.objects.filter(online=setting_item, flow=flow_tab.name).exists():
                                    if setting_item.advance:
                                        advance_setting = ReserveOnlineSetting.objects.filter(display_id=setting_item.advance).first()
                                        if advance_setting:
                                            advance_schedule = UserFlowSchedule.objects.filter(flow__user=user_flow.user, online=advance_setting, temp_flg=False).exclude(number=0).first()
                                            if advance_schedule and advance_schedule.date and advance_schedule.time:
                                                context['menu_list'].append(setting_item)
                                        else:
                                            context['menu_list'].append(setting_item)
                                    else:
                                        context['menu_list'].append(setting_item)

        context['age_list'] = [i for i in range(101)]
        return context