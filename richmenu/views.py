from view import ShopView, ShopListView

from richmenu.models import ShopRichMenu

class IndexView(ShopListView):
    template_name = 'richmenu/index.html'
    title = 'リッチメニュー'
    model = ShopRichMenu
    search_target = ['name', 'shop_rich_menu_item__url', 'shop_rich_menu_item__text']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class EditView(ShopView):
    template_name = 'richmenu/edit.html'
    title = 'リッチメニュー'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rich_menu'] = ShopRichMenu.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['rich_menu']:
            context['rich_menu'] = ShopRichMenu.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['rich_menu']:
                context['rich_menu'].display_id = ''
                context['rich_menu'].name = context['rich_menu'].name + ' コピー'
        return context