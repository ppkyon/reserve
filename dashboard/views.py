from django.shortcuts import render

from django.views.generic import View
from sign.mixins import ShopLoginMixin

class IndexView(ShopLoginMixin, View):
    template_name = 'dashboard/index.html'
    title = 'ダッシュボード'

    def get(self, request, **kwargs):
        data = {
            'title': self.title,
        }
        return render(self.request, self.template_name, data)