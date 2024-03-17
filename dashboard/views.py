from django.shortcuts import redirect

from view import ShopView

class IndexView(ShopView):
    def get(self, request, **kwargs):
        return redirect('/dashboard/')

class DashboardView(ShopView):
    template_name = 'dashboard/index.html'
    title = 'ダッシュボード'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context