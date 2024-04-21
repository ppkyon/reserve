from view import ShopView

from sign.models import AuthLogin, AuthShop, ShopLine

class IndexView(ShopView):
    template_name = 'proxy/index.html'
    title = '代理予約ページ'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context