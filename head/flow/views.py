from view import HeadView, HeadListView

from flow.models import HeadFlow
from template.models import HeadTemplateGreeting

class IndexView(HeadListView):
    template_name = 'head/flow/index.html'
    title = 'フロー管理'
    model = HeadFlow
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class EditView(HeadView):
    template_name = 'head/flow/edit.html'
    title = 'フロー管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['flow'] = HeadFlow.objects.filter(display_id=self.request.GET.get("id")).first()
        context['template_greeting'] = HeadTemplateGreeting.objects.order_by('number').first()
        return context