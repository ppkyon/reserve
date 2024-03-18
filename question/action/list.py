from django.db.models import Q

from question.models import ShopQuestion, ShopQuestionItem
from sign.models import AuthLogin
from table.models import TableSearch, TableSort, TableNumber

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
    table_search = TableSearch.objects.filter(url=url, company=auth_login.company, shop=auth_login.shop, manager=request.user).first()
    if table_search:
        query.add(Q(title__icontains=table_search.text)|Q(name__icontains=table_search.text)|Q(description__icontains=table_search.text), Q.AND)
    
    question = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=auth_login.shop, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            question = ShopQuestion.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(ShopQuestion)).all()[start:end]
        elif sort.sort == 2:
            question = ShopQuestion.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(ShopQuestion)).all()[start:end]
        else:
            question = ShopQuestion.objects.filter(query).order_by('-created_at').values(*get_model_field(ShopQuestion)).all()[start:end]
    else:
        question = ShopQuestion.objects.filter(query).order_by('-created_at').values(*get_model_field(ShopQuestion)).all()[start:end]
    total = ShopQuestion.objects.filter(query).count()
    
    for question_index, question_item in enumerate(question):
        question[question_index]['item'] = list(ShopQuestionItem.objects.filter(question__id=question_item['id']).values(*get_model_field(ShopQuestionItem)).all())
        question[question_index]['total'] = total

    return question