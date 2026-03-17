from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.db.models import Q

from sign.models import AuthLogin, ManagerProfile
from talk.models import TalkMessage, TalkMessageEmoji, TalkPin, TalkRead, TalkManager, TalkStatus
from user.models import LineUser, UserProfile

from common import get_model_field, display_time

def get_user_list(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    # Get all messages sorted by send_date desc (same query as original)
    if request.POST.get('text'):
        line_user_message = TalkMessage.objects.filter(Q(user__shop=auth_login.shop), Q(Q(user__display_name__icontains=request.POST.get('text'))|Q(user__user_profile__name__icontains=request.POST.get('text')))).order_by('send_date').reverse()
    else:
        line_user_message = TalkMessage.objects.filter(user__shop=auth_login.shop).order_by('send_date').reverse()

    # Deduplicate: get latest message ID per user, preserving send_date desc order
    temp_line_user = set()
    latest_msg_ids_ordered = []
    msg_id_to_user = {}
    for msg in line_user_message.values('id', 'user'):
        if msg['user'] not in temp_line_user:
            temp_line_user.add(msg['user'])
            latest_msg_ids_ordered.append(msg['id'])
            msg_id_to_user[msg['id']] = msg['user']

    if not latest_msg_ids_ordered:
        return []

    user_ids = list(msg_id_to_user.values())

    # Batch fetch message dicts (1 query)
    msg_dicts = {
        m['id']: m for m in TalkMessage.objects.filter(
            id__in=latest_msg_ids_ordered
        ).values(*get_model_field(TalkMessage))
    }

    # Batch fetch pinned user IDs (1 query)
    pinned_user_ids = set(
        TalkPin.objects.filter(
            user__in=user_ids, manager=request.user, pin_flg=True
        ).values_list('user', flat=True)
    )

    # Sort: pinned first (by send_date desc), then non-pinned (by send_date desc)
    # latest_msg_ids_ordered is already in send_date desc order
    pinned = []
    non_pinned = []
    for msg_id in latest_msg_ids_ordered:
        msg_dict = msg_dicts.get(msg_id)
        if msg_dict:
            if msg_dict['user'] in pinned_user_ids:
                pinned.append(msg_dict)
            else:
                non_pinned.append(msg_dict)
    line_user = pinned + non_pinned

    # Batch fetch related data
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

    # Assemble result (same structure as original)
    for line_user_index, line_user_item in enumerate(line_user):
        uid = line_user_item['user']

        line_user[line_user_index]['line_user'] = line_users_dict.get(uid)
        line_user[line_user_index]['line_user_profile'] = profiles_dict.get(uid)

        # line_message: per-user query exactly as original
        line_user[line_user_index]['line_message'] = TalkMessage.objects.filter(line_user_id=line_user_item['line_user_id']).values(*get_model_field(TalkMessage)).order_by('send_date').reverse().first()
        if line_user[line_user_index]['line_message']:
            line_user[line_user_index]['line_message']['text'] = convert_emoji(line_user[line_user_index]['line_message'], line_user[line_user_index]['line_message']['text'])
        line_user[line_user_index]['line_message']['display_date'] = display_time(naturaltime(line_user[line_user_index]['line_message']['send_date']))

        manager_id = user_to_manager_id.get(uid)
        line_user[line_user_index]['talk_manager'] = manager_profiles_dict.get(manager_id) if manager_id else None
        line_user[line_user_index]['talk_status'] = statuses_dict.get(uid)
        line_user[line_user_index]['talk_pin'] = pins_dict.get(uid)
        line_user[line_user_index]['talk_read'] = reads_dict.get(uid)

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