from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.db.models import Q, Subquery, OuterRef

from sign.models import AuthLogin, ManagerProfile
from talk.models import TalkMessage, TalkMessageEmoji, TalkPin, TalkRead, TalkManager, TalkStatus
from user.models import LineUser, UserProfile

from common import get_model_field, display_time

def get_user_list(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    search_text = request.POST.get('text')

    # Build base filter
    if search_text:
        matching_user_ids = list(
            LineUser.objects.filter(
                shop=auth_login.shop
            ).filter(
                Q(display_name__icontains=search_text) |
                Q(user_profile__name__icontains=search_text)
            ).values_list('id', flat=True).distinct()
        )
        if not matching_user_ids:
            return []
        msg_filter = Q(user__in=matching_user_ids)
    else:
        msg_filter = Q(user__shop=auth_login.shop)

    # Get latest message per user in 1 query using subquery
    latest_for_user = Subquery(
        TalkMessage.objects.filter(
            user=OuterRef('user')
        ).order_by('-send_date').values('id')[:1]
    )
    all_messages = list(
        TalkMessage.objects.filter(
            msg_filter,
            id=latest_for_user
        ).values(*get_model_field(TalkMessage))
    )

    if not all_messages:
        return []

    # Collect user IDs
    user_ids = [msg['user'] for msg in all_messages]

    # Batch fetch pinned user IDs (1 query)
    pinned_user_ids = set(
        TalkPin.objects.filter(
            user__in=user_ids, manager=request.user, pin_flg=True
        ).values_list('user', flat=True)
    )

    # Sort: pinned first (by send_date desc), then non-pinned (by send_date desc)
    pinned = [m for m in all_messages if m['user'] in pinned_user_ids]
    non_pinned = [m for m in all_messages if m['user'] not in pinned_user_ids]
    pinned.sort(key=lambda x: x['send_date'], reverse=True)
    non_pinned.sort(key=lambda x: x['send_date'], reverse=True)
    line_user = pinned + non_pinned

    # Batch fetch all related data
    line_users_dict = {
        u['id']: u for u in LineUser.objects.filter(id__in=user_ids).values(*get_model_field(LineUser))
    }
    profiles_dict = {}
    for p in UserProfile.objects.filter(user__in=user_ids).values(*get_model_field(UserProfile)):
        if p['user'] not in profiles_dict:
            profiles_dict[p['user']] = p

    talk_managers_qs = TalkManager.objects.filter(user__in=user_ids)
    user_to_manager_id = {tm.user_id: tm.manager_id for tm in talk_managers_qs}
    manager_ids = list(set(user_to_manager_id.values()))
    manager_profiles_dict = {}
    if manager_ids:
        for mp in ManagerProfile.objects.filter(manager__in=manager_ids).values(*get_model_field(ManagerProfile)):
            if mp['manager'] not in manager_profiles_dict:
                manager_profiles_dict[mp['manager']] = mp

    statuses_dict = {}
    for s in TalkStatus.objects.filter(user__in=user_ids).values(*get_model_field(TalkStatus)):
        if s['user'] not in statuses_dict:
            statuses_dict[s['user']] = s

    pins_dict = {}
    for p in TalkPin.objects.filter(user__in=user_ids, manager=request.user).values(*get_model_field(TalkPin)):
        if p['user'] not in pins_dict:
            pins_dict[p['user']] = p

    reads_dict = {}
    for r in TalkRead.objects.filter(user__in=user_ids, manager=request.user).values(*get_model_field(TalkRead)):
        if r['user'] not in reads_dict:
            reads_dict[r['user']] = r

    # Assemble result (exact same structure as original)
    for item in line_user:
        uid = item['user']

        # line_message: latest message data with emoji conversion and display_date
        line_message = dict(item)
        if line_message:
            line_message['text'] = convert_emoji(line_message, line_message['text'])
        line_message['display_date'] = display_time(naturaltime(line_message['send_date']))

        item['line_user'] = line_users_dict.get(uid)
        item['line_user_profile'] = profiles_dict.get(uid)
        item['line_message'] = line_message

        manager_id = user_to_manager_id.get(uid)
        item['talk_manager'] = manager_profiles_dict.get(manager_id) if manager_id else None
        item['talk_status'] = statuses_dict.get(uid)
        item['talk_pin'] = pins_dict.get(uid)
        item['talk_read'] = reads_dict.get(uid)

    return line_user

def get_all_read_count(request):
    return TalkRead.objects.filter(manager=request.user).aggregate(all_read_count=models.Sum('read_count'))



def convert_emoji(message, text):
    replace_list = []
    for message_emoji in TalkMessageEmoji.objects.filter(message__id=message['id']).order_by('number').all():
        replace_data = {}
        add_index = 0
        if text[message_emoji.index] != '(':
            add_index = add_index + 1
        replace_data['line'] = text[message_emoji.index+add_index:message_emoji.index+add_index+text[message_emoji.index+add_index:].find(')')+1]
        if '(' in replace_data['line'] and ')' in replace_data['line']:
            replace_data['image'] = '<img src="https://stickershop.line-scdn.net/sticonshop/v1/sticon/' + message_emoji.product_id + '/iPhone/' + message_emoji.emoji_id + '.png" width="15" height="15">'
            replace_list.append(replace_data)
    for replace_item in replace_list:
        text = text.replace(replace_item['line'], replace_item['image'])
    return text