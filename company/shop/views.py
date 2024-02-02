from django.shortcuts import render, redirect

from django.views.generic import View
from sign.mixins import CompanyLoginMixin

from fixture.models import Prefecture
from sign.models import AuthShop, ShopProfile, ShopLine, AuthLogin
from tag.models import CompanyTag, ShopHashTag

import phonenumbers

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
            'prefecture_list': Prefecture.objects.order_by('number').all()
        }
        return render(self.request, self.template_name, data)

class DetailView(CompanyLoginMixin, View):
    template_name = 'company/shop/detail.html'
    title = '店舗詳細'

    def get(self, request, **kwargs):
        shop = AuthShop.objects.filter(display_id=request.GET.get("id")).first()
        if shop.delete_flg:
            return redirect('company:shop:index')
        
        shop.line = ShopLine.objects.filter(shop=shop).first()
        shop.profile = ShopProfile.objects.filter(shop=shop).first()
        shop.profile.shop_postcode = str(shop.profile.shop_postcode)[0:3] + '-' + str(shop.profile.shop_postcode)[3:7]
        shop.profile.shop_phone_number = phonenumbers.format_number(phonenumbers.parse(shop.profile.shop_phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
        
        tag_list = list()
        for user_tag_item in ShopHashTag.objects.filter(shop=shop).order_by('number').all()[0:6]:
            tag_list.append( CompanyTag.objects.filter(id=user_tag_item.tag.id).first())
        shop.tag = tag_list

        data = {
            'title': self.title,
            'shop': shop,
            'prefecture_list': Prefecture.objects.order_by('number').all()
        }
        return render(self.request, self.template_name, data)
