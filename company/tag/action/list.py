from django.db.models import Q

from sign.models import AuthLogin
from table.models import TableSearch, TableSort
from tag.models import CompanyTag

from common import get_model_field

def get_tag_list(url, user, genre):
    auth_login = AuthLogin.objects.filter(user=user).first()

    search_query = None
    table_search = TableSearch.objects.filter(url=url, manager=user, shop=None, company=auth_login.company).first()
    if table_search and table_search.text:
        search_query = Q(name__icontains=table_search.text)

    tag_list = None
    sort = TableSort.objects.filter(url=url, manager=user, shop=None, company=auth_login.company).first()
    if search_query:
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', 'name', '-created_at').all()
                elif sort.sort == 2:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-name', '-created_at').all()
                else:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
            elif sort.target == 'created_at':
                if sort.sort == 1:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', 'created_at').all()
                elif sort.sort == 2:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
                else:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
            else:
                tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
        else:
            tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').all()
    else:
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', 'name', '-created_at').all()
                elif sort.sort == 2:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-name', '-created_at').all()
                else:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()
            elif sort.target == 'created_at':
                if sort.sort == 1:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', 'created_at').all()
                elif sort.sort == 2:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()
                else:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()
            else:
                tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()
        else:
            tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').all()

    return tag_list

def get_action_tag_list(url, user, genre):
    auth_login = AuthLogin.objects.filter(user=user).first()

    search_query = None
    table_search = TableSearch.objects.filter(url=url, manager=user, shop=None, company=auth_login.company).first()
    if table_search and table_search.text:
        search_query = Q(name__icontains=table_search.text)

    tag_list = None
    sort = TableSort.objects.filter(url=url, manager=user, shop=None, company=auth_login.company).first()
    if search_query:
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', 'name', '-created_at').values(*get_model_field(CompanyTag)).all()
                elif sort.sort == 2:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-name', '-created_at').values(*get_model_field(CompanyTag)).all()
                else:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
            elif sort.target == 'created_at':
                if sort.sort == 1:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', 'created_at').values(*get_model_field(CompanyTag)).all()
                elif sort.sort == 2:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
                else:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
            else:
                tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
        else:
            tag_list = CompanyTag.objects.filter(Q(genre=genre), search_query).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
    else:
        if sort:
            if sort.target == 'name':
                if sort.sort == 1:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', 'name', '-created_at').values(*get_model_field(CompanyTag)).all()
                elif sort.sort == 2:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-name', '-created_at').values(*get_model_field(CompanyTag)).all()
                else:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
            elif sort.target == 'created_at':
                if sort.sort == 1:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', 'created_at').values(*get_model_field(CompanyTag)).all()
                elif sort.sort == 2:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
                else:
                    tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
            else:
                tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
        else:
            tag_list = CompanyTag.objects.filter(Q(genre=genre)).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()

    return tag_list