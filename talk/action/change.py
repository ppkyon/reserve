from django.http import JsonResponse

from sign.models import AuthLogin, AuthUser, ManagerProfile
from talk.models import TalkPin, TalkStatus, TalkManager, TalkUpdate
from user.models import LineUser

from common import get_model_field
from talk.action.common import get_user_list, get_all_read_count

import uuid

def pin(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('user_id')).first()
    if TalkPin.objects.filter(user=user, manager=request.user).exists():
        pin = TalkPin.objects.filter(user=user).first()
        pin.pin_flg = request.POST.get('pin_flg')
        pin.save()
    else:
        pin = TalkPin.objects.create(
            id = str(uuid.uuid4()),
            user = user,
            manager = request.user,
            pin_flg = request.POST.get('pin_flg'),
        )
    
    pin = TalkPin.objects.filter(user=user).values(*get_model_field(TalkPin)).first()
    
    if not request.user.head_flg and not request.user.company_flg:
        talk_update = TalkUpdate.objects.filter(manager=request.user).first()
        talk_update.update_flg = False
        talk_update.save()
    return JsonResponse( {'user_list': get_user_list(request), 'all_read_count': get_all_read_count(request)}, safe=False )

def status(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('user_id')).first()
    if request.POST.get('status'):
        if TalkStatus.objects.filter(user=user).exists():
            status = TalkStatus.objects.filter(user=user).first()
            status.status = request.POST.get('status')
            status.save()
        else:
            status = TalkStatus.objects.create(
                id = str(uuid.uuid4()),
                user = user,
                status = request.POST.get('status'),
            )
        status = TalkStatus.objects.filter(user=user).values(*get_model_field(TalkStatus)).first()
    else:
        TalkStatus.objects.filter(user=user).delete()
        status = None
    return JsonResponse( {'status': status}, safe=False )

def manager(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    user = LineUser.objects.filter(shop=auth_login.shop, display_id=request.POST.get('user_id')).first()
    if request.POST.get('manager_id'):
        if TalkManager.objects.filter(user=user).exists():
            talk_manager = TalkManager.objects.filter(user=user).first()
            talk_manager.manager = AuthUser.objects.filter(display_id=request.POST.get('manager_id')).first()
            talk_manager.save()
        else:
            talk_manager = TalkManager.objects.create(
                id = str(uuid.uuid4()),
                user = user,
                manager = AuthUser.objects.filter(display_id=request.POST.get('manager_id')).first(),
            )
        manager_profile = ManagerProfile.objects.filter(manager=talk_manager.manager).values(*get_model_field(ManagerProfile)).first()
    else:
        TalkManager.objects.filter(user=user).delete()
        manager_profile = None
    return JsonResponse( {'manager_profile': manager_profile}, safe=False )