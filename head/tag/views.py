from django.db.models import Q
from django.shortcuts import render

from django.views.generic import View
from sign.mixins import HeadLoginMixin

from table.models import TableSearch
from tag.models import HeadTagGenre, HeadTag

from head.tag.action.list import get_tag_list

class IndexView(HeadLoginMixin, View):
    template_name = 'head/tag/index.html'
    title = 'タグ'

    def get(self, request, **kwargs):
        data = {
            'title': self.title,
            'tag_genre_list': HeadTagGenre.objects.order_by('-favorite_flg','-created_at').all(),
            'tag_list': get_tag_list(request.path, request.user, HeadTagGenre.objects.order_by('-favorite_flg','-created_at').first())
        }
        return render(self.request, self.template_name, data)
