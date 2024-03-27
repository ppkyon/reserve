from django.shortcuts import render

from django.views.generic import View

from sign.models import AuthShop, ShopLine

class IndexView(View):
    template_name = 'line/analytics/index.html'

    def get(self, request, **kwargs):
        if request.GET.get("liff.state"):
            id = request.GET.get("liff.state")[0:request.GET.get("liff.state").find('&')].replace( '/?id=', '' ).replace( '?id=', '' )
            number = request.GET.get("liff.state")[request.GET.get("liff.state").find('&'):request.GET.get("liff.state").rfind('&')].replace( '&number=', '' )
            type = request.GET.get("liff.state")[request.GET.get("liff.state").rfind('&'):].replace( '&type=', '' )
        else:
            id = request.GET.get("id")
            number = request.GET.get("number")
            type = request.GET.get("type")

        shop = AuthShop.objects.filter(display_id=kwargs.get("login")).first()
        shop_line = ShopLine.objects.filter(shop=shop).first()

        data = {
            'shop_id': kwargs.get("login"),
            'id': id,
            'number': number,
            'type': type,
            'liff_id': shop_line.analytics_id,
        }
        return render(self.request, self.template_name, data)
