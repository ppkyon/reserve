from view import HeadView

class IndexView(HeadView):
    template_name = 'head/flow/index.html'
    title = 'フロー管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context