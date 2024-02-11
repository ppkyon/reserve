from django.shortcuts import render, redirect

from django.views.generic import View
from sign.mixins import ShopLoginMixin

class IndexView(ShopLoginMixin, View):
    def get(self, request, **kwargs):
        return redirect('/dashboard/')

class DashboardView(ShopLoginMixin, View):
    template_name = 'dashboard/index.html'
    title = 'ダッシュボード'

    def get(self, request, **kwargs):
        data = {
            'title': self.title,
        }
        return render(self.request, self.template_name, data)