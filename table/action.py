from django.http import JsonResponse

from sign.models import AuthLogin
from table.models import TableSearch, TableNumber, TableSort, MiniTableNumber, MiniTableSort

import uuid

def number(request):
    if '/head/' in request.POST.get('url'):
        company = None
        shop = None
    elif '/company/' in request.POST.get('url'):
        company = AuthLogin.objects.filter(user=request.user).first().company
        shop = None
    else:
        company = AuthLogin.objects.filter(user=request.user).first().company
        shop = AuthLogin.objects.filter(user=request.user).first().shop
    
    if TableNumber.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company).exists():
        number = TableNumber.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company).first()
        number.number = request.POST.get('number')
        number.save()
    else:
        TableNumber.objects.create(
            id = str(uuid.uuid4()),
            url = request.POST.get('url'),
            company = company,
            shop = shop,
            manager = request.user,
            number = request.POST.get('number'),
        )

    return JsonResponse( {}, safe=False )

def sort(request):
    if '/head/' in request.POST.get('url'):
        company = None
        shop = None
    elif '/company/' in request.POST.get('url'):
        company = AuthLogin.objects.filter(user=request.user).first().company
        shop = None
    else:
        company = AuthLogin.objects.filter(user=request.user).first().company
        shop = AuthLogin.objects.filter(user=request.user).first().shop

    if TableSort.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company).exists():
        sort = TableSort.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company).first()
        if sort.target == request.POST.get('target'):
            if sort.sort == 2:
                sort.delete()
                return JsonResponse( {}, safe=False )
            else:
                sort.sort = sort.sort + 1
        else:
            sort.sort = 1
        sort.target = request.POST.get('target')
        sort.save()
    else:
        TableSort.objects.create(
            id = str(uuid.uuid4()),
            url = request.POST.get('url'),
            company = company,
            shop = shop,
            manager = request.user,
            target = request.POST.get('target'),
            sort = 1,
        )
    return JsonResponse( {}, safe=False )



def mini_number(request):
    if '/head/' in request.POST.get('url'):
        company = None
        shop = None
    elif '/company/' in request.POST.get('url'):
        company = AuthLogin.objects.filter(user=request.user).first().company
        shop = None
    else:
        company = AuthLogin.objects.filter(user=request.user).first().company
        shop = AuthLogin.objects.filter(user=request.user).first().shop
    
    if MiniTableNumber.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company, page=request.POST.get('page'), item=request.POST.get('item')).exists():
        number = MiniTableNumber.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company, page=request.POST.get('page'), item=request.POST.get('item')).first()
        number.page = request.POST.get('page')
        number.item = request.POST.get('item')
        number.number = request.POST.get('number')
        number.save()
    else:
        MiniTableNumber.objects.create(
            id = str(uuid.uuid4()),
            url = request.POST.get('url'),
            company = company,
            shop = shop,
            manager = request.user,
            page = request.POST.get('page'),
            item = request.POST.get('item'),
            number = request.POST.get('number'),
        )

    return JsonResponse( {}, safe=False )

def mini_sort(request):
    if '/head/' in request.POST.get('url'):
        company = None
        shop = None
    elif '/company/' in request.POST.get('url'):
        company = AuthLogin.objects.filter(user=request.user).first().company
        shop = None
    else:
        company = AuthLogin.objects.filter(user=request.user).first().company
        shop = AuthLogin.objects.filter(user=request.user).first().shop

    if MiniTableSort.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company, page=request.POST.get('page'), item=request.POST.get('item')).exists():
        sort = MiniTableSort.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company, page=request.POST.get('page'), item=request.POST.get('item')).first()
        if sort.target == request.POST.get('target'):
            if sort.sort == 2:
                sort.delete()
                return JsonResponse( {}, safe=False )
            else:
                sort.sort = sort.sort + 1
        else:
            sort.sort = 1
        sort.target = request.POST.get('target')
        sort.page = request.POST.get('page')
        sort.item = request.POST.get('item')
        sort.save()
    else:
        MiniTableSort.objects.create(
            id = str(uuid.uuid4()),
            url = request.POST.get('url'),
            company = company,
            shop = shop,
            manager = request.user,
            page = request.POST.get('page'),
            item = request.POST.get('item'),
            target = request.POST.get('target'),
            sort = 1,
        )
    return JsonResponse( {}, safe=False )



def action_search(request, shop, company):
    if request.POST.get('text'):
        if TableSearch.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company).exists():
            search = TableSearch.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company).first()
            search.text = request.POST.get('text')
            search.save()
        else:
            search = TableSearch.objects.create(
                id = str(uuid.uuid4()),
                url = request.POST.get('url'),
                company = company,
                shop = shop,
                manager = request.user,
                text = request.POST.get('text'),
            )
        return search
    else:
        TableSearch.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company).all().delete()
        return None

def action_item_search(request, shop, company, target):
    if request.POST.get(target):
        if TableSearch.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company, item=target).exists():
            search = TableSearch.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company, item=target).first()
            search.text = request.POST.get(target)
            search.save()
        else:
            search = TableSearch.objects.create(
                id = str(uuid.uuid4()),
                url = request.POST.get('url'),
                company = company,
                shop = shop,
                manager = request.user,
                item = target,
                text = request.POST.get(target),
            )
        return search
    else:
        TableSearch.objects.filter(url=request.POST.get('url'), manager=request.user, shop=shop, company=company, item=target).all().delete()
        return None