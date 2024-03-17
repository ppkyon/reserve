from view import ShopView

from sign.models import AuthUser, ShopLine, ManagerProfile
from line.data import get_info

class IndexView(ShopView):
    template_name = 'setting/index.html'
    title = '設定'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['manager'] = self.request.user
        context['manager'].profile = ManagerProfile.objects.filter(manager=context['manager']).first()

        context['manager_list'] = AuthUser.objects.filter(shop=self.request.shop, status__gt=0, head_flg=False, delete_flg=False).order_by('created_at').all()
        for manager_index, manager_item in enumerate(context['manager_list']):
            context['manager_list'][manager_index].profile = ManagerProfile.objects.filter(manager_id=manager_item.id).first()
            context['manager_list'][manager_index].author_profile = ManagerProfile.objects.filter(manager_id=manager_item.author).first()

        context['shop'] = self.request.shop
        context['shop'].line = ShopLine.objects.filter(shop=context['shop']).first()
        
        context['line_info'] = get_info(self.request.shop)
        return context