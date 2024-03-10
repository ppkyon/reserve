from django.db.models import Q

from fixture.models import Prefecture
from sign.models import AuthCompany, CompanyProfile
from table.models import TableNumber, TableSearch, TableSort
from tag.models import HeadTag, CompanyHashTag

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
        query.add(Q(company_profile__company_name__icontains=table_search.text), Q.AND)
    
    company = list()
    sort = TableSort.objects.filter(url=url, company=None, shop=None, manager=request.user).first()
    if sort:
        if sort.sort == 1:
            company = AuthCompany.objects.filter(query).order_by(sort.target, '-created_at').values(*get_model_field(AuthCompany)).all()[start:end]
        elif sort.sort == 2:
            company = AuthCompany.objects.filter(query).order_by('-'+sort.target, '-created_at').values(*get_model_field(AuthCompany)).all()[start:end]
        else:
            company = AuthCompany.objects.filter(query).order_by('-created_at').values(*get_model_field(AuthCompany)).all()[start:end]
    else:
        company = AuthCompany.objects.filter(query).order_by('-created_at').values(*get_model_field(AuthCompany)).all()[start:end]
    total = AuthCompany.objects.filter(query).count()

    for company_index, company_item in enumerate(company):
        company[company_index]['profile'] = CompanyProfile.objects.filter(company__id=company_item['id']).values(*get_model_field(CompanyProfile)).first()
        company[company_index]['total'] = total

        if Prefecture.objects.filter(id=company_item['profile']['company_prefecture']).exists():
            company[company_index]['profile']['prefecture_name'] = Prefecture.objects.filter(id=company_item['profile']['company_prefecture']).first().name
        else:
            company[company_index]['profile']['prefecture_name'] = ''
        company[company_index]['tag'] = list(CompanyHashTag.objects.filter(company__id=company_item['id']).values(*get_model_field(CompanyHashTag)).all())
        for tag_index, tag_item in enumerate(company[company_index]['tag']):
            if HeadTag.objects.filter(id=tag_item['tag']).values(*get_model_field(HeadTag)).exists():
                company[company_index]['tag'][tag_index]['name'] = HeadTag.objects.filter(id=tag_item['tag']).first().name
    return company