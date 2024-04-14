from django.shortcuts import redirect

from view import UserView, UserListView

from question.models import UserQuestion
from flow.models import UserFlow, UserFlowSchedule
from sign.models import AuthLogin
from tag.models import UserHashTag
from user.models import LineUser, UserProfile

import phonenumbers

class IndexView(UserListView):
    template_name = 'user/index.html'
    title = 'お客様管理'
    model = LineUser
    search_target = ['title', 'name', 'description']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['age_list'] = [i for i in range(101)]
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
            context['user'].flow[user_flow_index].schedule = UserFlowSchedule.objects.filter(flow=user_flow_item).order_by('number').all()

        context['user'].tag = UserHashTag.objects.filter(user=context['user']).order_by('number').all()

        context['user'].question = UserQuestion.objects.filter(user=context['user']).order_by('-created_at').all()
        
        return context