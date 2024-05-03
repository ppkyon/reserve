from view import ShopView, ShopListView

from flow.models import CompanyFlow, ShopFlow
from sign.models import AuthLogin
from template.models import ShopTemplateGreeting

from dateutil.relativedelta import relativedelta

import datetime

class IndexView(ShopListView):
    template_name = 'flow/index.html'
    title = 'フロー設計'
    model = ShopFlow
    search_target = ['name']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()

        alert_status = 0
        alert_message = None
        if ShopFlow.objects.filter(shop=auth_login.shop).exists():
            flow_chart = ShopFlow.objects.filter(shop=auth_login.shop).order_by('-period_to').first()
            if flow_chart.period_to and flow_chart.period_to <= datetime.datetime.now():
                alert_status = 3
                alert_message = '設定している採用フローの表示期限が終了しています。'
            elif flow_chart.period_to and flow_chart.period_to <= datetime.datetime.now() + relativedelta(days=+10):
                alert_status = 2
                alert_message = '設定している採用フローの表示期限がまもなくです。'
        context['alert'] = {
            'status': alert_status,
            'message': alert_message,
        }
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