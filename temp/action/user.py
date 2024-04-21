from django.db.models import Q
from django.http import JsonResponse

from flow.models import ShopFlowTab, ShopFlowItem, ShopFlowRichMenu, UserFlow
from richmenu.models import UserRichMenu
from sign.models import AuthLogin
from tag.models import ShopTag, UserHashTag
from user.models import LineUser, UserProfile

from common import create_code, get_model_field
from line.action.richmenu import create_rich_menu, delete_rich_menu

import phonenumbers
import uuid

def save(request):
    birth = None
    if request.POST.get('birth'):
        birth = request.POST.get('birth')
    age = 0
    if request.POST.get('age'):
        age = request.POST.get('age')
    sex = 0
    if request.POST.get('sex'):
        sex = request.POST.get('sex')

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).first()
    if UserProfile.objects.filter(user=user).exists():
        user_profile = UserProfile.objects.filter(user=user).first()
        user_profile.email = request.POST.get('email')
        user_profile.name = request.POST.get('name')
        user_profile.name_kana = request.POST.get('name_kana')
        user_profile.birth = birth
        user_profile.age = age
        user_profile.sex = sex
        user_profile.phone_number = request.POST.get('phone_number').replace('-', '')
        user_profile.memo = request.POST.get('memo')
        user_profile.save()
    else:
        UserProfile.objects.create(
            id = str(uuid.uuid4()),
            user = user,
            email = request.POST.get('email'),
            name = request.POST.get('name'),
            name_kana = request.POST.get('name_kana'),
            birth = birth,
            age = age,
            sex = sex,
            phone_number = request.POST.get('phone_number').replace('-', ''),
            memo = request.POST.get('memo'),
        )
    
    UserHashTag.objects.filter(user=user).all().delete()
    if request.POST.get('tag[]'):
        for tag_index, tag_item in enumerate( request.POST.get('tag[]').split(',') ):
            if not UserHashTag.objects.filter(tag=ShopTag.objects.filter(display_id=tag_item).first()).exists():
                UserHashTag.objects.create(
                    id = str(uuid.uuid4()),
                    user = user,
                    number = (tag_index+1),
                    tag = ShopTag.objects.filter(display_id=tag_item).first()
                )
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )

def get(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).values(*get_model_field(LineUser)).first()

    user['profile'] = UserProfile.objects.filter(user__id=user['id']).values(*get_model_field(UserProfile)).first()
    if user['profile'] and user['profile']['birth']:
        user['profile']['display_birth'] = user['profile']['birth'].strftime('%Y年%m月%d日')
    if user['profile'] and user['profile']['phone_number']:
        user['profile']['phone_number'] = phonenumbers.format_number(phonenumbers.parse(user['profile']['phone_number'], 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
    user['display_date'] = user['created_at'].strftime('%Y年%m月%d日 %H:%M')
    if user['profile']['updated_at']:
        user['profile']['updated_at'] = user['profile']['updated_at'].strftime('%Y/%m/%d')

    user['active_flow'] = UserFlow.objects.filter(user__id=user['id'], end_flg=False).order_by('flow_tab__number').values(*get_model_field(UserFlow)).first()
    user['active_flow']['tab'] = ShopFlowTab.objects.filter(id=user['active_flow']['flow_tab']).values(*get_model_field(ShopFlowTab)).first()
    
    user['tag'] = list(UserHashTag.objects.filter(user__id=user['id']).values(*get_model_field(UserHashTag)).all())
    for user_tag_index, user_tag_item in enumerate(user['tag']):
        user['tag'][user_tag_index]['tag'] = ShopTag.objects.filter(id=user_tag_item['tag']).values(*get_model_field(ShopTag)).first()

    return JsonResponse( user, safe=False )



def member(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('id')).first()
    user.member_flg = True
    user.save()

    for user_flow in UserFlow.objects.filter(user=user, flow_tab__member=0).order_by('number').all():
        user_flow.end_flg = True
        user_flow.save()

    if not UserFlow.objects.filter(Q(user=user), Q(Q(flow_tab__member=1)|Q(flow_tab__member=2))).order_by('number').exists():
        user_flow = UserFlow.objects.filter(user=user).order_by('number').first()
        for flow_tab in ShopFlowTab.objects.filter(Q(flow=user_flow.flow), Q(Q(member=1)|Q(member=2))).order_by('number').all():
            UserFlow.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, UserFlow),
                user = user,
                number = UserFlow.objects.filter(user=user).count() + 1,
                flow = flow_tab.flow,
                flow_tab = flow_tab,
                flow_item = None,
                name = flow_tab.name,
                richmenu = None,
                end_flg = False,
            )
    return JsonResponse( {}, safe=False )