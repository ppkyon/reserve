from view import CompanyView, CompanyListView

from richmenu.models import CompanyRichMenu

class IndexView(CompanyListView):
    template_name = 'company/richmenu/index.html'
    title = 'リッチメニュー管理'
    model = CompanyRichMenu
    search_target = ['name', 'company_rich_menu_item__url', 'company_rich_menu_item__text']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class EditView(CompanyView):
    template_name = 'company/richmenu/edit.html'
    title = 'リッチメニュー管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rich_menu'] = CompanyRichMenu.objects.filter(display_id=self.request.GET.get("id")).first()
        if not context['rich_menu']:
            context['rich_menu'] = CompanyRichMenu.objects.filter(display_id=self.request.GET.get("copy")).first()
            if context['rich_menu']:
                context['rich_menu'].display_id = ''
                context['rich_menu'].name = context['rich_menu'].name + ' コピー'
        return context