from django.shortcuts import render

from django.views.generic import View
from sign.mixins import HeadLoginMixin

from sign.models import AuthUser, ManagerProfile

class IndexView(HeadLoginMixin, View):
    template_name = 'head/setting/index.html'
    title = '設定'

    def get(self, request, **kwargs):
        manager = request.user
        manager.profile = ManagerProfile.objects.filter(manager=manager).first()

        manager_list = AuthUser.objects.filter(status__gt=0, head_flg=True, delete_flg=False).order_by('created_at').all()
        for manager_index, manager_item in enumerate(manager_list):
            manager_list[manager_index].profile = ManagerProfile.objects.filter(manager=manager_item).first()
            manager_list[manager_index].author_profile = ManagerProfile.objects.filter(manager_id=manager_item.author).first()

        data = {
            'title': self.title,
            'manager': manager,
            'manager_list': manager_list,
            'age_list': [i for i in range(101)],
        }
        return render(self.request, self.template_name, data)
