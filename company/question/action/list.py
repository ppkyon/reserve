from django.db.models import Q

from question.models import CompanyQuestion, CompanyQuestionItem
from sign.models import AuthLogin
from table.models import TableSearch, TableSort, TableNumber

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
        query.add(Q(title__icontains=table_search.text)|Q(name__icontains=table_search.text)|Q(description__icontains=table_search.text), Q.AND)
    
    print(query)
    question = list()
    sort = TableSort.objects.filter(url=url, company=auth_login.company, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            question = CompanyQuestion.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(CompanyQuestion)).all()[start:end]
        elif sort.sort == 2:
            question = CompanyQuestion.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(CompanyQuestion)).all()[start:end]
        else:
            question = CompanyQuestion.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyQuestion)).all()[start:end]
    else:
        question = CompanyQuestion.objects.filter(query).order_by('-created_at').values(*get_model_field(CompanyQuestion)).all()[start:end]
    total = CompanyQuestion.objects.filter(query).count()
    
    for question_index, question_item in enumerate(question):
        question[question_index]['item'] = list(CompanyQuestionItem.objects.filter(question__id=question_item['id']).values(*get_model_field(CompanyQuestionItem)).all())
        question[question_index]['total'] = total

    return question