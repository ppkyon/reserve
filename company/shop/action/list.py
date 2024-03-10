from django.db.models import Q

from fixture.models import Prefecture
from sign.models import AuthLogin, AuthShop, ShopProfile
from table.models import TableNumber, TableSearch, TableSort
from tag.models import CompanyTag, ShopHashTag

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
        query.add(Q(shop_profile__shop_name__icontains=table_search.text), Q.AND)
    
    shop = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            shop = AuthShop.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(AuthShop)).all()[start:end]
        elif sort.sort == 2:
            shop = AuthShop.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(AuthShop)).all()[start:end]
        else:
            shop = AuthShop.objects.filter(query).order_by('-created_at').values(*get_model_field(AuthShop)).all()[start:end]
    else:
        shop = AuthShop.objects.filter(query).order_by('-created_at').values(*get_model_field(AuthShop)).all()[start:end]
    total = AuthShop.objects.filter(query).count()

    for shop_index, shop_item in enumerate(shop):
        shop[shop_index]['profile'] = ShopProfile.objects.filter(shop__id=shop_item['id']).values(*get_model_field(ShopProfile)).first()
        shop[shop_index]['total'] = total

        if Prefecture.objects.filter(id=shop_item['profile']['shop_prefecture']).exists():
            shop[shop_index]['profile']['prefecture_name'] = Prefecture.objects.filter(id=shop_item['profile']['shop_prefecture']).first().name
        else:
            shop[shop_index]['profile']['prefecture_name'] = ''
        shop[shop_index]['tag'] = list(ShopHashTag.objects.filter(shop__id=shop_item['id']).values(*get_model_field(ShopHashTag)).all())
        for tag_index, tag_item in enumerate(shop[shop_index]['tag']):
            if CompanyTag.objects.filter(id=tag_item['tag']).values(*get_model_field(CompanyTag)).exists():
                shop[shop_index]['tag'][tag_index]['name'] = CompanyTag.objects.filter(id=tag_item['tag']).first().name
    return shop