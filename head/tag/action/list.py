from django.db.models import Q

from table.models import TableSearch, TableSort
from tag.models import HeadTag

from common import get_model_field

def get_tag_list(url, user, genre):
    search_query = None
    table_search = TableSearch.objects.filter(url=url, manager=user, shop=None, company=None).first()
    if table_search and table_search.text:
        search_query = Q(name__icontains=table_search.text)

    tag_list = None
    sort = TableSort.objects.filter(url=url, manager=user, shop=None, company=None).first()
    if search_query:
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', 'name', '-created_at').all()
                elif sort.sort == 2:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-name', '-created_at').all()
                else:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
            elif sort.target == 'created_at':
                if sort.sort == 1:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', 'created_at').all()
                elif sort.sort == 2:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
                else:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
            else:
                tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
        else:
            tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
    else:
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', 'name', '-created_at').all()
                elif sort.sort == 2:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-name', '-created_at').all()
                else:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()
            elif sort.target == 'created_at':
                if sort.sort == 1:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', 'created_at').all()
                elif sort.sort == 2:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()
                else:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()
            else:
                tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()
        else:
            tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()

    return tag_list

def get_action_tag_list(url, user, genre):
    search_query = None
    table_search = TableSearch.objects.filter(url=url, manager=user, shop=None, company=None).first()
    if table_search and table_search.text:
        search_query = Q(name__icontains=table_search.text)

    tag_list = None
    sort = TableSort.objects.filter(url=url, manager=user, shop=None, company=None).first()
    if search_query:
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', 'name', '-created_at').values(*get_model_field(HeadTag)).all()
                elif sort.sort == 2:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-name', '-created_at').values(*get_model_field(HeadTag)).all()
                else:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
            elif sort.target == 'created_at':
                if sort.sort == 1:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', 'created_at').values(*get_model_field(HeadTag)).all()
                elif sort.sort == 2:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
                else:
                    tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
            else:
                tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
        else:
            tag_list = HeadTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
    else:
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', 'name', '-created_at').values(*get_model_field(HeadTag)).all()
                elif sort.sort == 2:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-name', '-created_at').values(*get_model_field(HeadTag)).all()
                else:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
            elif sort.target == 'created_at':
                if sort.sort == 1:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', 'created_at').values(*get_model_field(HeadTag)).all()
                elif sort.sort == 2:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
                else:
                    tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
            else:
                tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
        else:
            tag_list = HeadTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()

    return tag_list