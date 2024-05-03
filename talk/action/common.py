from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.db.models import Q

from sign.models import AuthLogin, ManagerProfile
from talk.models import TalkMessage, TalkPin, TalkRead, TalkManager, TalkStatus
from user.models import LineUser, UserProfile

from common import get_model_field, display_time

def get_user_list(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    temp_line_user = list()
    line_user = list()
    if request.POST.get('text'):
        line_user_message = TalkMessage.objects.filter(Q(user__shop=auth_login.shop), Q(Q(user__display_name__icontains=request.POST.get('text'))|Q(user__user_profile__name__icontains=request.POST.get('text')))).order_by('send_date').reverse().all()
    else:
        line_user_message = TalkMessage.objects.filter(user__shop=auth_login.shop).order_by('send_date').reverse().all()
        
    for line_user_message_item in line_user_message:
        if TalkPin.objects.filter(user=line_user_message_item.user, manager=request.user, pin_flg=True).exists():
            if not line_user_message_item.user.id in temp_line_user:
                line_user.append(TalkMessage.objects.filter(id=line_user_message_item.id).values(*get_model_field(TalkMessage)).first())
                temp_line_user.append(line_user_message_item.user.id)
    for line_user_message_item in line_user_message:
        if not line_user_message_item.user.id in temp_line_user:
            line_user.append(TalkMessage.objects.filter(id=line_user_message_item.id).values(*get_model_field(TalkMessage)).first())
            temp_line_user.append(line_user_message_item.user.id)

    for line_user_index, line_user_item in enumerate(line_user):
        line_user[line_user_index]['line_user'] = LineUser.objects.filter(shop=auth_login.shop, id=line_user_item['user']).values(*get_model_field(LineUser)).first()
        line_user[line_user_index]['line_user_profile'] = UserProfile.objects.filter(user__id=line_user_item['line_user']['id']).values(*get_model_field(UserProfile)).first()
        line_user[line_user_index]['line_message'] = TalkMessage.objects.filter(line_user_id=line_user_item['line_user_id']).values(*get_model_field(TalkMessage)).order_by('send_date').reverse().first()
        line_user[line_user_index]['line_message']['display_date'] = display_time(naturaltime(line_user[line_user_index]['line_message']['send_date']))

        if TalkManager.objects.filter(user=line_user_item['user']).exists():
            line_user[line_user_index]['talk_manager'] = ManagerProfile.objects.filter(manager=TalkManager.objects.filter(user=line_user_item['user']).first().manager).values(*get_model_field(ManagerProfile)).first()
        else:
            line_user[line_user_index]['talk_manager'] = None
        if TalkStatus.objects.filter(user=line_user_item['user']).exists():
            line_user[line_user_index]['talk_status'] = TalkStatus.objects.filter(user=line_user_item['user']).values(*get_model_field(TalkStatus)).first()
        else:
            line_user[line_user_index]['talk_status'] = None
        if TalkPin.objects.filter(user=line_user_item['user'], manager=request.user).exists():
            line_user[line_user_index]['talk_pin'] = TalkPin.objects.filter(user=line_user_item['user'], manager=request.user).values(*get_model_field(TalkPin)).first()
        else:
            line_user[line_user_index]['talk_pin'] = None
        if TalkRead.objects.filter(user=line_user_item['user'], manager=request.user).exists():
            line_user[line_user_index]['talk_read'] = TalkRead.objects.filter(user=line_user_item['user'], manager=request.user).values(*get_model_field(TalkRead)).first()
        else:
            line_user[line_user_index]['talk_read'] = None
    
    return line_user

def get_all_read_count(request):
    return TalkRead.objects.filter(manager=request.user).aggregate(all_read_count=models.Sum('read_count'))