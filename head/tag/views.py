from view import HeadView

from table.models import TableSearch, TableSort
from tag.models import HeadTagGenre

from head.tag.action.list import get_tag_list

class IndexView(HeadView):
    template_name = 'head/tag/index.html'
    title = 'タグ'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tag_genre_list'] = HeadTagGenre.objects.order_by('-favorite_flg','-created_at').all()
        context['tag_list'] = get_tag_list(self.request.path, self.request.user, HeadTagGenre.objects.order_by('-favorite_flg','-created_at').first())
        
        sort = TableSort.objects.filter(url=self.request.path, company=None, shop=None, manager=self.request.user).first()
        if not sort:
            sort = {
                'target': 'created_at',
                'sort': 2,
            }
        context['table'] = {
            'sort': sort,
            'search': TableSearch.objects.filter(url=self.request.path, company=None, shop=None, manager=self.request.user).first(),
        }
        return context
