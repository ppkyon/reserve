from view import HeadView

from sign.models import AuthUser, ManagerProfile

class IndexView(HeadView):
    template_name = 'head/setting/index.html'
    title = '設定'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        manager = self.request.user
        manager.profile = ManagerProfile.objects.filter(manager=manager).first()
        context['manager'] = manager
        
        manager_list = AuthUser.objects.filter(status__gt=0, head_flg=True, delete_flg=False).order_by('created_at').all()
        for manager_index, manager_item in enumerate(manager_list):
            manager_list[manager_index].profile = ManagerProfile.objects.filter(manager=manager_item).first()
            manager_list[manager_index].author_profile = ManagerProfile.objects.filter(manager_id=manager_item.author).first()
        context['manager_list'] = manager_list

        context['age_list'] = [i for i in range(101)]
        return context
