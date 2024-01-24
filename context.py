from django.conf import settings

from sign.models import AuthUser, ManagerProfile, AuthLogin
from table.models import TableSearch, TableNumber, TableSort

import environ

env = environ.Env()
env.read_env('.env')

def env_data(request):
    site_name = env('SITE_NAME')
    if env('ENCODING') == 'True':
        site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")

    data = {
        'env_static_url': settings.STATIC_URL,
        'env_site_name': site_name,
    }
    return data

def header_data(request):
    manager = None
    if not request.user.is_anonymous:
        manager = AuthUser.objects.filter(id=request.user.id).first()
        manager.profile = ManagerProfile.objects.filter(manager=manager).first()

    data = {
        'header_manager': manager
    }
    return data

def table_data(request):
    if request.user.is_anonymous:
        data = {
            
        }
    else:
        if '/head/' in request.path:
            company = None
            shop = None
        elif '/company/' in request.path:
            company = AuthLogin.objects.filter(user=request.user).first().company
            shop = None
        else:
            company = AuthLogin.objects.filter(user=request.user).first().company
            shop = AuthLogin.objects.filter(user=request.user).first().shop

        search = ''
        if TableSearch.objects.filter(url=request.path, manager=request.user, shop=shop, company=company).exists():
            search = TableSearch.objects.filter(url=request.path, manager=request.user, shop=shop, company=company).first().text
        number = 5
        if TableNumber.objects.filter(url=request.path, manager=request.user, shop=shop, company=company).exists():
            number = TableNumber.objects.filter(url=request.path, manager=request.user, shop=shop, company=company).first().number
        target = None
        sort = None
        if TableSort.objects.filter(url=request.path, manager=request.user, shop=shop, company=company).exists():
            target = TableSort.objects.filter(url=request.path, manager=request.user, shop=shop, company=company).first().target
            sort = TableSort.objects.filter(url=request.path, manager=request.user, shop=shop, company=company).first().sort

        data = {
            'table_search': search,
            'table_number': number,
            'table_sort_target': target,
            'table_sort': sort
        }
    return data