from view import CompanyView

from sign.models import AuthUser, ManagerProfile

class IndexView(CompanyView):
    template_name = 'company/setting/index.html'
    title = '設定'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['manager'] = self.request.user
        context['manager'].profile = ManagerProfile.objects.filter(manager=context['manager']).first()

        context['manager_list'] = AuthUser.objects.filter(company=self.request.company, status__gt=0, head_flg=False, delete_flg=False).order_by('created_at').all()
        for manager_index, manager_item in enumerate(context['manager_list']):
            context['manager_list'][manager_index].profile = ManagerProfile.objects.filter(manager=manager_item).first()
            context['manager_list'][manager_index].author_profile = ManagerProfile.objects.filter(manager_id=manager_item.author).first()

        context['age_list'] = [i for i in range(101)]
        return context
