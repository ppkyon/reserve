
from view import ShopView

class IndexView(ShopView):
    template_name = 'talk/index.html'
    title = '1対1トーク'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context