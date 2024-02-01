from django.shortcuts import render

from django.views.generic import View
from sign.mixins import CompanyLoginMixin

from sign.models import AuthShop, ShopProfile, AuthLogin
from tag.models import ShopHashTag

class IndexView(CompanyLoginMixin, View):
    template_name = 'company/shop/index.html'
    title = '店舗管理'

    def get(self, request, **kwargs):
        auth_login = AuthLogin.objects.filter(user=request.user).first()
        shop_list = AuthShop.objects.filter(company=auth_login.company, status__gte=2, delete_flg=False).order_by('-created_at').all()
        for shop_index, shop_item in enumerate(shop_list):
            shop_list[shop_index].profile = ShopProfile.objects.filter(shop=shop_item).first()
            shop_list[shop_index].tag = ShopHashTag.objects.filter(shop=shop_item).all()[0:6]

        data = {
            'title': self.title,
            'shop_list': shop_list,
        }
        return render(self.request, self.template_name, data)
