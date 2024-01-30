from django.shortcuts import render

from django.views.generic import View
from sign.mixins import CompanyLoginMixin

class IndexView(CompanyLoginMixin, View):
    template_name = 'company/shop/index.html'
    title = '店舗管理'

    def get(self, request, **kwargs):
        data = {
            'title': self.title,
        }
        return render(self.request, self.template_name, data)
