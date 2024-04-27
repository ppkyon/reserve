from django.db.models import Q

from flow.models import ShopFlowTab, UserFlow
from sign.models import AuthLogin
from table.models import TableNumber
from tag.models import ShopTag, UserHashTag
from user.models import LineUser, UserProfile

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

    query = Q(shop=auth_login.shop)
    query.add(Q(proxy_flg=True), Q.AND)

    user_list = LineUser.objects.filter(query).order_by('-created_at').values(*get_model_field(LineUser)).distinct().all()[start:end]
    total = LineUser.objects.filter(query).distinct().count()

    for user_index, user_item in enumerate(user_list):
        user_list[user_index]['profile'] = UserProfile.objects.filter(user__id=user_item['id']).values(*get_model_field(UserProfile)).first()
        user_list[user_index]['active_flow'] = UserFlow.objects.filter(user__id=user_item['id'], end_flg=False).order_by('flow_tab__number').values(*get_model_field(UserFlow)).first()
        if user_list[user_index]['active_flow']:
            user_list[user_index]['active_flow']['flow_tab'] = ShopFlowTab.objects.filter(id=user_list[user_index]['active_flow']['flow_tab']).values(*get_model_field(ShopFlowTab)).first()
        user_list[user_index]['tag'] = list(UserHashTag.objects.filter(user__id=user_item['id']).order_by('number').values(*get_model_field(UserHashTag)).all())
        for tag_index, tag_item in user_list[user_index]['tag']:
            user_list[user_index]['tag'][tag_index]['tag'] = ShopTag.objects.filter(id=tag_item['tag']['id']).values(*get_model_field(ShopTag)).first()
        user_list[user_index]['total'] = total
    
    return user_list