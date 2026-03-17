from django.db import models
from django.db.models import Subquery, OuterRef

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

        # Get latest message per user in 1 query using subquery
        latest_for_user = Subquery(
            TalkMessage.objects.filter(
                user=OuterRef('user')
            ).order_by('-send_date').values('id')[:1]
        )
        line_user_message = list(
            TalkMessage.objects.filter(
                user__shop=auth_login.shop,
                user__delete_flg=False,
                id=latest_for_user
            ).select_related('user').order_by('-send_date')
        )

        # Collect user IDs for batch queries
        user_ids = [msg.user_id for msg in line_user_message]

        # Batch fetch pinned user IDs (1 query)
        pinned_ids = set(
            TalkPin.objects.filter(
                user__in=user_ids, manager=self.request.user, pin_flg=True
            ).values_list('user_id', flat=True)
        ) if user_ids else set()

        # Sort: pinned first (by send_date desc), then non-pinned (by send_date desc)
        context['line_user'] = list()
        temp_line_user = set()
        for msg in line_user_message:
            if msg.user_id in pinned_ids and msg.user_id not in temp_line_user:
                context['line_user'].append(msg)
                temp_line_user.add(msg.user_id)
        for msg in line_user_message:
            if msg.user_id not in temp_line_user:
                context['line_user'].append(msg)
                temp_line_user.add(msg.user_id)

        # Batch fetch profiles (1 query)
        profiles_dict = {p.user_id: p for p in UserProfile.objects.filter(user__in=user_ids)} if user_ids else {}

        for line_user_index, line_user_item in enumerate(context['line_user']):
            context['line_user'][line_user_index].profile = profiles_dict.get(line_user_item.user_id)
            context['line_user'][line_user_index].message = line_user_item
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
            context['line_message_user'].profile = profiles_dict.get(user.id) if user else None
            if context['line_message_user'] and not context['line_message_user'].profile:
                context['line_message_user'].profile = UserProfile.objects.filter(user=context['line_message_user']).first()
            if TalkRead.objects.filter(user=context['line_message_user'], manager=self.request.user).exists():
                read = TalkRead.objects.filter(user=context['line_message_user'], manager=self.request.user).first()
                read.read_count = 0
                read.read_flg = False
                read.save()

        # Batch fetch related data for all users
        talk_managers_dict = {}
        mgr_profile_dict = {}
        if user_ids:
            talk_managers_qs = TalkManager.objects.filter(user__in=user_ids)
            talk_managers_dict = {tm.user_id: tm.manager_id for tm in talk_managers_qs}
            manager_ids = list(set(talk_managers_dict.values()))
            if manager_ids:
                mgr_profile_dict = {mp.manager_id: mp for mp in ManagerProfile.objects.filter(manager__in=manager_ids)}

        statuses_dict = {s.user_id: s for s in TalkStatus.objects.filter(user__in=user_ids)} if user_ids else {}
        pins_dict = {p.user_id: p for p in TalkPin.objects.filter(user__in=user_ids, manager=self.request.user)} if user_ids else {}
        reads_dict = {r.user_id: r for r in TalkRead.objects.filter(user__in=user_ids, manager=self.request.user)} if user_ids else {}

        for line_user_index, line_user_item in enumerate(context['line_user']):
            uid = line_user_item.user_id
            manager_id = talk_managers_dict.get(uid)
            if manager_id:
                context['line_user'][line_user_index].message_manager = mgr_profile_dict.get(manager_id)
            else:
                context['line_user'][line_user_index].message_manager = None
            if statuses_dict.get(uid):
                context['line_user'][line_user_index].message_status = statuses_dict.get(uid)
            else:
                context['line_user'][line_user_index].message_status = None
            if pins_dict.get(uid):
                context['line_user'][line_user_index].message_pin = pins_dict.get(uid)
            else:
                context['line_user'][line_user_index].message_pin = None
            if reads_dict.get(uid):
                context['line_user'][line_user_index].message_read = reads_dict.get(uid)
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
        manager_qs = list(AuthUser.objects.filter(shop=auth_login.shop, authority__gte=2, status__gte=3, head_flg=False, delete_flg=False).order_by('created_at').all())
        context['manager'] = manager_qs
        if manager_qs:
            mgr_profiles_for_list = {mp.manager_id: mp for mp in ManagerProfile.objects.filter(manager__in=manager_qs)}
            for manager_index, manager_item in enumerate(context['manager']):
                context['manager'][manager_index].profile = mgr_profiles_for_list.get(manager_item.id)
        else:
            for manager_index, manager_item in enumerate(context['manager']):
                context['manager'][manager_index].profile = None

        talk_read = TalkRead.objects.filter(user__delete_flg=False, manager=self.request.user).aggregate(sum_read_count=models.Sum('read_count'))
        context['all_talk_read'] = talk_read['sum_read_count']

        return context