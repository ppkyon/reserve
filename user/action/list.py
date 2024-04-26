from django.db.models import Q

from flow.models import UserFlow
from sign.models import AuthLogin
from table.models import TableNumber
from tag.models import UserHashTag
from user.models import LineUser

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

    user_list = LineUser.objects.filter(query).order_by('-created_at').values(*get_model_field(LineUser)).distinct().all()[start:end]
    total = LineUser.objects.filter(query).distinct().count()

    for user_index, user_item in enumerate(user_list):
        user_list[user_index]['active_flow'] = list(UserFlow.objects.filter(user=user_item, end_flg=False).order_by('flow_tab__number').first())
        user_list[user_index]['tag'] = UserHashTag.objects.filter(user=user_item).order_by('number').all()
        user_list[user_index]['total'] = total
    
    return user_list