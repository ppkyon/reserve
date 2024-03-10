from django.db.models import Q

from flow.models import HeadFlow
from table.models import TableNumber, TableSearch, TableSort

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
        query.add(Q(name__icontains=table_search.text), Q.AND)
    
    flow = list()
    sort = TableSort.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            flow = HeadFlow.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(HeadFlow)).all()[start:end]
        elif sort.sort == 2:
            flow = HeadFlow.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(HeadFlow)).all()[start:end]
        else:
            flow = HeadFlow.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadFlow)).all()[start:end]
    else:
        flow = HeadFlow.objects.filter(query).order_by('-created_at').values(*get_model_field(HeadFlow)).all()[start:end]
    total = HeadFlow.objects.filter(query).count()

    for flow_index, flow_item in enumerate(flow):
        flow[flow_index]['total'] = total
    
    return flow