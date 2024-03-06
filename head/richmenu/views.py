from view import HeadView, HeadListView

from richmenu.models import HeadRichMenu

class IndexView(HeadListView):
    template_name = 'head/richmenu/index.html'
    title = 'リッチメニュー管理'
    model = HeadRichMenu
    search_target = ['name', 'head_rich_menu_item__url', 'head_rich_menu_item__text']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class EditView(HeadView):
    template_name = 'head/richmenu/edit.html'
    title = 'リッチメニュー管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rich_menu'] = HeadRichMenu.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['rich_menu']:
            context['rich_menu'] = HeadRichMenu.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['rich_menu']:
                context['rich_menu'].display_id = ''
                context['rich_menu'].name = context['rich_menu'].name + ' コピー'
        return context