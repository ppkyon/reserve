from view import ShopView, ShopListView

from flow.models import CompanyFlow, ShopFlow
from sign.models import AuthLogin
from template.models import ShopTemplateGreeting

class IndexView(ShopListView):
    template_name = 'flow/index.html'
    title = 'フロー設計'
    model = ShopFlow
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class EditView(ShopView):
    template_name = 'flow/edit.html'
    title = 'フロー設計'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['company_flow'] = CompanyFlow.objects.filter(company=auth_login.shop.company, valid=True).order_by('created_at').all()
        context['flow'] = ShopFlow.objects.filter(display_id=self.request.GET.get("id")).first()
        
        context['template_greeting'] = ShopTemplateGreeting.objects.filter(company=auth_login.shop.company, shop=auth_login.shop).order_by('number').first()
        return context