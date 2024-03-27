from view import UserView, UserListView

from user.models import LineUser

class IndexView(UserListView):
    template_name = 'user/index.html'
    title = 'お客様管理'
    model = LineUser
    search_target = ['title', 'name', 'description']
    default_sort = '-created_at'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class DetailView(UserView):
    template_name = 'user/detail.html'
    title = 'お客様管理 - 詳細 -'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context