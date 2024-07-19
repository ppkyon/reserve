from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.db import models
from django.http import JsonResponse

from sign.models import AuthLogin, ManagerProfile
from talk.models import TalkMessage, TalkPin, TalkRead, TalkManager, TalkStatus, TalkUpdate
from template.models import (
    ShopTemplateCardType, ShopTemplateCardTypeLocation, ShopTemplateCardTypePerson, ShopTemplateCardTypeImage,
    ShopTemplateCardTypeAnnounce, ShopTemplateCardTypeAnnounceText, ShopTemplateCardTypeAnnounceAction
)
from user.models import LineUser, UserProfile

from common import get_model_field
from talk.action.common import get_user_list, get_all_read_count

def search(request):
    talk_update = TalkUpdate.objects.filter(manager=request.user).first()
    if talk_update:
        talk_update.update_flg = False
        talk_update.save()
    return JsonResponse( {'user_list': get_user_list(request), 'all_read_count': get_all_read_count(request)}, safe=False )

def change(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    line_user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).values(*get_model_field(LineUser)).first()
    line_user['profile'] = UserProfile.objects.filter(user=line_user['id']).values(*get_model_field(UserProfile)).first()
    line_user['message'] = list(TalkMessage.objects.filter(user=line_user['id']).values(*get_model_field(TalkMessage)).order_by('send_date').all())
    for line_message_index, line_message_item in enumerate(line_user['message']):
        line_user['message'][line_message_index]['author_profile'] = ManagerProfile.objects.filter(manager_id=line_message_item['author']).values(*get_model_field(ManagerProfile)).first()
        line_user['message'][line_message_index]['display_date'] = naturalday(line_message_item['send_date'] )
        if line_user['message'][line_message_index]['message_type'] == 7:
            line_user['message'][line_message_index]['template'] = list(ShopTemplateCardType.objects.filter(id=line_message_item['template_id']).values(*get_model_field(ShopTemplateCardType)).all())
            for template_index, template_item in enumerate(line_user['message'][line_message_index]['template']):
                if template_item['type'] == 1:
                    line_user['message'][line_message_index]['template'][template_index]['announce'] = ShopTemplateCardTypeAnnounce.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateCardTypeAnnounce)).first()
                    line_user['message'][line_message_index]['template'][template_index]['text'] = list(ShopTemplateCardTypeAnnounceText.objects.filter(card_type__id=template_item['announce']['id']).values(*get_model_field(ShopTemplateCardTypeAnnounceText)).all())
                    line_user['message'][line_message_index]['template'][template_index]['action'] = list(ShopTemplateCardTypeAnnounceAction.objects.filter(card_type__id=template_item['announce']['id']).values(*get_model_field(ShopTemplateCardTypeAnnounceAction)).all())
                elif template_item['type'] == 2:
                    line_user['message'][line_message_index]['template'][template_index]['location'] = ShopTemplateCardTypeLocation.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateCardTypeLocation)).first()
                elif template_item['type'] == 3:
                    line_user['message'][line_message_index]['template'][template_index]['person'] = ShopTemplateCardTypePerson.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateCardTypePerson)).first()
                elif template_item['type'] == 4:
                    line_user['message'][line_message_index]['template'][template_index]['image'] = ShopTemplateCardTypeImage.objects.filter(template__id=template_item['id']).values(*get_model_field(ShopTemplateCardTypeImage)).first()
        elif line_user['message'][line_message_index]['message_type'] == 9:
            line_user['message'][line_message_index]['sticker'] = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/' + line_user['message'][line_message_index]['sticker_id'] + '/iPhone/sticker_key@2x.png'

    line_user['talk_manager'] = None
    line_user['talk_status'] = None
    if TalkManager.objects.filter(user=line_user['id']).exists():
        line_user['talk_manager'] = ManagerProfile.objects.filter(manager=TalkManager.objects.filter(user=line_user['id']).first().manager).values(*get_model_field(ManagerProfile)).first()
    if TalkStatus.objects.filter(user=line_user['id']).exists():
        line_user['talk_status'] = TalkStatus.objects.filter(user=line_user['id']).first().get_status_display()
    if TalkPin.objects.filter(user=line_user['id']).exists():
        line_user['talk_pin'] = TalkPin.objects.filter(user=line_user['id'], manager=request.user).values(*get_model_field(TalkPin)).first()
    
    if TalkRead.objects.filter(user=line_user['id'], manager=request.user).exists():
        read = TalkRead.objects.filter(user=line_user['id'], manager=request.user).first()
        read.read_count = 0
        read.read_flg = False
        read.save()
    talk_read = TalkRead.objects.filter(user__shop=line_user['shop'], read_flg=False).aggregate(all_read_count=models.Sum('read_count'))

    return JsonResponse( {'line_user': line_user, 'talk_read': talk_read}, safe=False )