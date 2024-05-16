from django.contrib.auth.views import LogoutView

from view import ShopView

class IndexView(ShopView):
    template_name = 'proxy/index.html'
    title = '代理予約ページ'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class LogoutView(LogoutView):
    next_page = '/simple/login'