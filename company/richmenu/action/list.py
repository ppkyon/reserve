from django.db.models import Q

from richmenu.models import CompanyRichMenu, CompanyRichMenuItem
from sign.models import AuthLogin
from table.models import TableNumber, TableSearch, TableSort

from common import get_model_field

def get_list(request, page):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    url = request.path.replace('paging/', '').replace('search/', '')

    page = int(page)
    number = 5
    table_number = TableNumber.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if table_number:
        number = table_number.number
    
    start = number * ( page - 1 )
    end = number * page

    query = Q(company=auth_login.company)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text)|Q(company_rich_menu_item__url__icontains=table_search.text)|Q(company_rich_menu_item__text__icontains=table_search.text), Q.AND)
    
    rich_menu = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            rich_menu = CompanyRichMenu.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(CompanyRichMenu)).distinct().all()[start:end]
        elif sort.sort == 2:
            rich_menu = CompanyRichMenu.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(CompanyRichMenu)).distinct().all()[start:end]
        else:
            rich_menu = CompanyRichMenu.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyRichMenu)).distinct().all()[start:end]
    else:
        rich_menu = CompanyRichMenu.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyRichMenu)).distinct().all()[start:end]
    total = CompanyRichMenu.objects.filter(query).distinct().count()
    
    for rich_menu_index, rich_menu_item in enumerate(rich_menu):
        rich_menu[rich_menu_index]['item'] = list(CompanyRichMenuItem.objects.filter(rich_menu__id=rich_menu_item['id']).values(*get_model_field(CompanyRichMenuItem)).all())
        rich_menu[rich_menu_index]['total'] = total

    return rich_menu