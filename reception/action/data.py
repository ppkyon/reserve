from django.http import JsonResponse

from reception.models import ReceptionData
from sign.models import AuthLogin

from common import create_code

import uuid

def save(request):
    auto_flg = False
    if request.POST.get('auto_flg') == '1':
        auto_flg = True

    auth_login = AuthLogin.objects.filter(user=request.user).first()
    if ReceptionData.objects.filter(shop=auth_login.shop).exists():
        reception = ReceptionData.objects.filter(shop=auth_login.shop).first()
        reception.auto_flg = auto_flg
        reception.save()
    else:
        ReceptionData.objects.create(
            id = str(uuid.uuid4()),
            display_id = create_code(12, ReceptionData),
            shop = auth_login.shop,
            auto_flg = auto_flg,
        )
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )