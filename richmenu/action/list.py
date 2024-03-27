from django.db.models import Q

from richmenu.models import ShopRichMenu, ShopRichMenuItem
from sign.models import AuthLogin
from table.models import TableNumber, TableSearch, TableSort

from common import get_model_field

def get_list(request, page):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    url = request.path.replace('paging/', '').replace('search/', '')

    page = int(page)
    number = 5
    table_number = TableNumber.objects.filter(url=url, company=auth_login.company, shop=auth_login.shop, manager=request.user).first()
    if table_number:
        number = table_number.number
    
    start = number * ( page - 1 )
    end = number * page

    query = Q(company=auth_login.shop.company)
    query.add(Q(shop=auth_login.shop), Q.AND)
    table_search = TableSearch.objects.filter(url=url, company=auth_login.company, shop=auth_login.shop, manager=request.user).first()
    if table_search:
        query.add(Q(name__icontains=table_search.text)|Q(shop_rich_menu_item__url__icontains=table_search.text)|Q(shop_rich_menu_item__text__icontains=table_search.text), Q.AND)
    
    rich_menu = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=auth_login.shop, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            rich_menu = ShopRichMenu.objects.filter(query).order_by('-favorite_flg', sort.target, '-created_at').values(*get_model_field(ShopRichMenu)).distinct().all()[start:end]
        elif sort.sort == 2:
            rich_menu = ShopRichMenu.objects.filter(query).order_by('-favorite_flg', '-'+sort.target, '-created_at').values(*get_model_field(ShopRichMenu)).distinct().all()[start:end]
        else:
            rich_menu = ShopRichMenu.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopRichMenu)).distinct().all()[start:end]
    else:
        rich_menu = ShopRichMenu.objects.filter(query).order_by('-favorite_flg', '-created_at').values(*get_model_field(ShopRichMenu)).distinct().all()[start:end]
    total = ShopRichMenu.objects.filter(query).distinct().count()
    
    for rich_menu_index, rich_menu_item in enumerate(rich_menu):
        rich_menu[rich_menu_index]['item'] = list(ShopRichMenuItem.objects.filter(rich_menu__id=rich_menu_item['id']).values(*get_model_field(ShopRichMenuItem)).all())
        rich_menu[rich_menu_index]['total'] = total

    return rich_menu