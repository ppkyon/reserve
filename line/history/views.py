from django.conf import settings
from django.shortcuts import render

from django.views.generic import View

from sign.models import AuthShop, ShopLine

class IndexView(View):
    template_name = 'line/history/index.html'
    title = '予約履歴'

    def get(self, request, **kwargs):
        shop = AuthShop.objects.filter(display_id=kwargs.get("login")).first()
        shop_line = ShopLine.objects.filter(shop=shop).first()

        data = {
            'static_url': settings.STATIC_URL,
            'media_url': settings.MEDIA_URL,
            'title': self.title,
            'shop_id': kwargs.get("login"),
            'liff_id': shop_line.history_id,
        }
        return render(self.request, self.template_name, data)
