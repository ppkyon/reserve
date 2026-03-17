from django.db import models

from view import ShopView

from sign.models import AuthLogin, AuthUser, ManagerProfile
from talk.models import TalkMessage, TalkPin, TalkRead, TalkManager, TalkStatus, TalkUpdate
from user.models import LineUser, UserProfile

class IndexView(ShopView):
    template_name = 'talk/index.html'
    title = '1対1トーク'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()

        line_user_message = list()
        for line_user_item in LineUser.objects.filter(shop=auth_login.shop, delete_flg=False).all():
            if TalkMessage.objects.filter(user=line_user_item).exists():
                line_user_message.append(TalkMessage.objects.filter(user=line_user_item).order_by('send_date').reverse().first())
        line_user_message = sorted(line_user_message, key=lambda x: x.send_date, reverse=True)

        context['line_user'] = list()
        temp_line_user = list()
        for line_user_message_item in line_user_message:
            if TalkPin.objects.filter(user=line_user_message_item.user, manager=self.request.user, pin_flg=True).exists():
                if not line_user_message_item.user.id in temp_line_user:
                    context['line_user'].append(line_user_message_item)
                    temp_line_user.append(line_user_message_item.user.id)
        for line_user_message_item in line_user_message:
            if not line_user_message_item.user.id in temp_line_user:
                context['line_user'].append(line_user_message_item)
                temp_line_user.append(line_user_message_item.user.id)
                break
        
        for line_user_index, line_user_item in enumerate(context['line_user']):
            context['line_user'][line_user_index].profile = UserProfile.objects.filter(user=line_user_item.user).first()
            context['line_user'][line_user_index].message = TalkMessage.objects.filter(user=line_user_item.user).order_by('send_date').reverse().first()
            if context['line_user'][line_user_index].message and context['line_user'][line_user_index].message.text:
                context['line_user'][line_user_index].message.text = context['line_user'][line_user_index].message.text.replace('\\n',' ').replace('\\r','')

        user = None
        context['line_message'] = None
        context['line_message_user'] = None
        context['line_message_user_id'] = None
        if self.request.GET.get("id"):
            context['line_message_user_id'] = self.request.GET.get("id")
            user = LineUser.objects.filter(display_id=self.request.GET.get("id")).first()
        else:
            if len(context['line_user']) > 0:
                context['line_message_user_id'] = context['line_user'][0].user.display_id
                user = context['line_user'][0].user
        if len(context['line_user']) > 0:
            context['line_message_user'] = user
            context['line_message_user'].profile = UserProfile.objects.filter(user=context['line_message_user']).first()
            if TalkRead.objects.filter(user=context['line_message_user'], manager=self.request.user).exists():
                read = TalkRead.objects.filter(user=context['line_message_user'], manager=self.request.user).first()
                read.read_count = 0
                read.read_flg = False
                read.save()

        for line_user_index, line_user_item in enumerate(context['line_user']):
            if TalkManager.objects.filter(user=line_user_item.user).exists():
                context['line_user'][line_user_index].message_manager = ManagerProfile.objects.filter(manager=TalkManager.objects.filter(user=line_user_item.user).first().manager).first()
            else:
                context['line_user'][line_user_index].message_manager = None
            if TalkStatus.objects.filter(user=line_user_item.user).exists():
                context['line_user'][line_user_index].message_status = TalkStatus.objects.filter(user=line_user_item.user).first()
            else:
                context['line_user'][line_user_index].message_status = None
            if TalkPin.objects.filter(user=line_user_item.user, manager=self.request.user).exists():
                context['line_user'][line_user_index].message_pin = TalkPin.objects.filter(user=line_user_item.user, manager=self.request.user).first()
            else:
                context['line_user'][line_user_index].message_pin = None
            if TalkRead.objects.filter(user=line_user_item.user, manager=self.request.user).exists():
                context['line_user'][line_user_index].message_read = TalkRead.objects.filter(user=line_user_item.user, manager=self.request.user).first()
            else:
                context['line_user'][line_user_index].message_read = None

        if context['line_message']:
            context['line_message_user'].message_manager = None
            context['line_message_user'].message_status = None
            context['line_message_user'].message_pin = None
            context['line_message_user'].message_read = None
            if TalkManager.objects.filter(user=context['line_message_user']).exists():
                context['line_message_user'].message_manager = ManagerProfile.objects.filter(manager=TalkManager.objects.filter(user=context['line_message_user']).first().manager).first()
            if TalkStatus.objects.filter(user=context['line_message_user']).exists():
                context['line_message_user'].message_status = TalkStatus.objects.filter(user=context['line_message_user']).first()
            if TalkPin.objects.filter(user=context['line_message_user'], manager=self.request.user).exists():
                context['line_message_user'].message_pin = TalkPin.objects.filter(user=context['line_message_user'], manager=self.request.user).first()
            if TalkRead.objects.filter(user=context['line_message_user'], manager=self.request.user).exists():
                context['line_message_user'].message_read = TalkRead.objects.filter(user=context['line_message_user'], manager=self.request.user).first()

        if TalkUpdate.objects.filter(manager=self.request.user).exists():
            talk_update = TalkUpdate.objects.filter(manager=self.request.user).first()
            talk_update.update_flg = False
            talk_update.save()

        context['status_list'] = TalkStatus._meta.get_field('status').choices
        context['manager'] = AuthUser.objects.filter(shop=auth_login.shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all()
        for manager_index, manager_item in enumerate(context['manager']):
            context['manager'][manager_index].profile = ManagerProfile.objects.filter(manager=manager_item).first()

        talk_read = TalkRead.objects.filter(user__delete_flg=False, manager=self.request.user).aggregate(sum_read_count=models.Sum('read_count'))
        context['all_talk_read'] = talk_read['sum_read_count']

        return context