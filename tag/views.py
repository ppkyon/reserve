from view import ShopView

from sign.models import AuthLogin
from table.models import TableSort, TableSearch
from tag.models import ShopTagGenre

from tag.action.list import get_tag_list

class IndexView(ShopView):
    template_name = 'tag/index.html'
    title = 'タグ'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        auth_login = AuthLogin.objects.filter(user=self.request.user).first()
        context['tag_genre_list'] = ShopTagGenre.objects.filter(shop=auth_login.shop).order_by('-favorite_flg','-created_at').all()
        context['tag_list'] = get_tag_list(self.request.path, self.request.user, ShopTagGenre.objects.filter(shop=auth_login.shop).order_by('-favorite_flg','-created_at').first())

        sort = TableSort.objects.filter(url=self.request.path, company=auth_login.shop.company, shop=auth_login.shop, manager=self.request.user).first()
        if not sort:
            sort = {
                'target': 'created_at',
                'sort': 2,
            }
        context['table'] = {
            'sort': sort,
            'search': TableSearch.objects.filter(url=self.request.path, company=auth_login.shop.company, shop=auth_login.shop, manager=self.request.user).first(),
        }
        return context
