from django.shortcuts import render, redirect

from view import CompanyView, CompanyListView

from fixture.models import Prefecture
from sign.models import AuthShop, ShopProfile, ShopLine
from tag.models import CompanyTag, ShopHashTag

import phonenumbers

class IndexView(CompanyListView):
    template_name = 'company/shop/index.html'
    title = '店舗管理'
    model = AuthShop
    search_target = ['shop_profile__shop_name']
    default_sort = '-created_at'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['prefecture_list'] = Prefecture.objects.order_by('number').all()
        return context

class DetailView(CompanyView):
    template_name = 'company/shop/detail.html'
    title = '店舗詳細'

    def get(self, request, **kwargs):
        shop = AuthShop.objects.filter(display_id=request.GET.get("id")).first()
        if shop.delete_flg:
            return redirect('company:shop:index')
        return render(self.request, self.template_name, self.get_context_data())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['shop'] = AuthShop.objects.filter(display_id=self.request.GET.get("id")).first()
        context['shop'].line = ShopLine.objects.filter(shop=context['shop']).first()
        context['shop'].profile = ShopProfile.objects.filter(shop=context['shop']).first()
        context['shop'].profile.shop_postcode = str(context['shop'].profile.shop_postcode)[0:3] + '-' + str(context['shop'].profile.shop_postcode)[3:7]
        context['shop'].profile.shop_phone_number = phonenumbers.format_number(phonenumbers.parse(context['shop'].profile.shop_phone_number, 'JP'), phonenumbers.PhoneNumberFormat.NATIONAL)
        
        tag_list = list()
        for user_tag_item in ShopHashTag.objects.filter(shop=context['shop']).order_by('number').all()[0:6]:
            tag_list.append( CompanyTag.objects.filter(id=user_tag_item.tag.id).first())
        context['shop'].tag = tag_list
        return context