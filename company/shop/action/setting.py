from django.http import JsonResponse

from sign.models import AuthShop, ShopNotice

import uuid

def save_notice(request):
    shop = AuthShop.objects.filter(display_id=request.POST.get('id')).first()
    if ShopNotice.objects.filter(shop=shop).exists():
        shop_notice = ShopNotice.objects.filter(shop=shop).first()
        shop_notice.channel_id = request.POST.get('channel_id')
        shop_notice.channel_secret = request.POST.get('channel_secret')
        shop_notice.channel_access_token = request.POST.get('channel_access_token')
        shop_notice.bot_id = request.POST.get('bot_id')
        shop_notice.follow_url = request.POST.get('follow_url')
        shop_notice.line_flg = request.POST.get('line_flg')
        shop_notice.mail_flg = request.POST.get('mail_flg')
        shop_notice.save()
    else:
        ShopNotice.objects.create(
            id = str(uuid.uuid4()),
            shop = shop,
            channel_id = request.POST.get('channel_id'),
            channel_secret = request.POST.get('channel_secret'),
            channel_access_token = request.POST.get('channel_access_token'),
            bot_id = request.POST.get('bot_id'),
            follow_url = request.POST.get('follow_url'),
            line_flg = request.POST.get('line_flg'),
            mail_flg = request.POST.get('mail_flg'),
        )
    return JsonResponse( {}, safe=False )