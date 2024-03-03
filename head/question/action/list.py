from django.db.models import Q

from question.models import HeadQuestion, HeadQuestionItem
from table.models import TableSearch, TableSort, TableNumber

from common import get_model_field

def get_list(request, page):
    url = request.path.replace('paging/', '').replace('search/', '')

    page = int(page)
    number = 5
    table_number = TableNumber.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if table_number:
        number = table_number.number
    
    start = number * ( page - 1 )
    end = number * page

    query = Q()
    table_search = TableSearch.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if table_search:
        query.add(Q(title__icontains=table_search.text)|Q(name__icontains=table_search.text)|Q(description__icontains=table_search.text), Q.AND)
    
    question = list()
    sort = TableSort.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            question = HeadQuestion.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(HeadQuestion)).all()[start:end]
        elif sort.sort == 2:
            question = HeadQuestion.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(HeadQuestion)).all()[start:end]
        else:
            question = HeadQuestion.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadQuestion)).all()[start:end]
    else:
        question = HeadQuestion.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadQuestion)).all()[start:end]
    total = HeadQuestion.objects.filter(query).count()
    
    for question_index, question_item in enumerate(question):
        question[question_index]['item'] = list(HeadQuestionItem.objects.filter(question__id=question_item['id']).values(*get_model_field(HeadQuestionItem)).all())
        question[question_index]['total'] = total

    return question