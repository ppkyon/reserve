from django.shortcuts import render

from django.views.generic import View
from sign.mixins import CompanyLoginMixin

from sign.models import AuthLogin
from tag.models import CompanyTagGenre

from company.tag.action.list import get_tag_list

class IndexView(CompanyLoginMixin, View):
    template_name = 'company/tag/index.html'
    title = 'タグ'

    def get(self, request, **kwargs):
        auth_login = AuthLogin.objects.filter(user=request.user).first()
        data = {
            'title': self.title,
            'tag_genre_list': CompanyTagGenre.objects.filter(company=auth_login.company).order_by('-favorite_flg','-created_at').all(),
            'tag_list': get_tag_list(request.path, request.user, CompanyTagGenre.objects.filter(company=auth_login.company).order_by('-favorite_flg','-created_at').first())
        }
        return render(self.request, self.template_name, data)
