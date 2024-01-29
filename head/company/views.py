from django.shortcuts import render

from django.views.generic import View
from sign.mixins import HeadLoginMixin

from fixture.models import Prefecture
from sign.models import AuthCompany, CompanyProfile
from tag.models import CompanyHashTag

class IndexView(HeadLoginMixin, View):
    template_name = 'head/company/index.html'
    title = '企業管理'

    def get(self, request, **kwargs):
        company_list = AuthCompany.objects.filter(status__gte=2, delete_flg=False).order_by('-created_at').all()
        for company_index, company_item in enumerate(company_list):
            company_list[company_index].profile = CompanyProfile.objects.filter(company=company_item).first()
            company_list[company_index].tag = CompanyHashTag.objects.filter(company=company_item).all()[0:6]

        data = {
            'title': self.title,
            'company_list': company_list,
            'prefecture_list': Prefecture.objects.order_by('number').all()
        }
        return render(self.request, self.template_name, data)
