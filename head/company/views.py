from view import HeadListView

from fixture.models import Prefecture
from sign.models import AuthCompany

class IndexView(HeadListView):
    template_name = 'head/company/index.html'
    title = '企業管理'
    model = AuthCompany
    search_target = ['company_profile__company_name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['prefecture_list'] = Prefecture.objects.order_by('number').all()
        return context
