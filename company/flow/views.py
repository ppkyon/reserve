from view import CompanyView, CompanyListView

from flow.models import HeadFlow, CompanyFlow
from template.models import CompanyTemplateGreeting

class IndexView(CompanyListView):
    template_name = 'company/flow/index.html'
    title = 'フロー管理'
    model = CompanyFlow
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class EditView(CompanyView):
    template_name = 'company/flow/edit.html'
    title = 'フロー管理'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['head_flow'] = HeadFlow.objects.filter(valid=True).order_by('created_at').all()
        context['flow'] = CompanyFlow.objects.filter(display_id=self.request.GET.get("id")).first()
        context['template_greeting'] = CompanyTemplateGreeting.objects.filter(company=self.request.company).order_by('number').first()
        return context