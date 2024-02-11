from django.shortcuts import render

from django.views.generic import View
from sign.mixins import ShopLoginMixin

from sign.models import AuthUser, ShopLine, ManagerProfile
from line.data import get_info

class IndexView(ShopLoginMixin, View):
    template_name = 'setting/index.html'
    title = '設定'

    def get(self, request, **kwargs):
        manager = request.user
        manager.profile = ManagerProfile.objects.filter(manager=manager).first()

        manager_list = AuthUser.objects.filter(shop=request.shop, status__gt=0, head_flg=False, delete_flg=False).order_by('created_at').all()
        for manager_index, manager_item in enumerate(manager_list):
            manager_list[manager_index].profile = ManagerProfile.objects.filter(manager_id=manager_item.id).first()
            manager_list[manager_index].author_profile = ManagerProfile.objects.filter(manager_id=manager_item.author).first()

        shop = request.shop
        shop.line = ShopLine.objects.filter(shop=shop).first()

        data = {
            'title': self.title,
            'shop': shop,
            'manager': manager,
            'manager_list': manager_list,
            'line_info': get_info(request.shop),
        }
        return render(self.request, self.template_name, data)