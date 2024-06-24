from django.http import JsonResponse

from sign.models import AuthLogin
from table.models import MiniTableSearch

from dashboard.action.list import get_list
from table.action import action_mini_search

def search(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    action_mini_search(request, auth_login.shop, auth_login.company, 'name')
    action_mini_search(request, auth_login.shop, auth_login.company, 'kana')
    action_mini_search(request, auth_login.shop, auth_login.company, 'phone')
    action_mini_search(request, auth_login.shop, auth_login.company, 'email')
    action_mini_search(request, auth_login.shop, auth_login.company, 'age_from')
    action_mini_search(request, auth_login.shop, auth_login.company, 'age_to')
    action_mini_search(request, auth_login.shop, auth_login.company, 'datetime_from')
    action_mini_search(request, auth_login.shop, auth_login.company, 'datetime_to')
    action_mini_search(request, auth_login.shop, auth_login.company, 'time_from')
    action_mini_search(request, auth_login.shop, auth_login.company, 'time_to')
    action_mini_search(request, auth_login.shop, auth_login.company, 'sex')
    action_mini_search(request, auth_login.shop, auth_login.company, 'member')
    action_mini_search(request, auth_login.shop, auth_login.company, 'line')
    action_mini_search(request, auth_login.shop, auth_login.company, 'flow')
    action_mini_search(request, auth_login.shop, auth_login.company, 'manager')
    action_mini_search(request, auth_login.shop, auth_login.company, 'facility')
    return JsonResponse( list(get_list(request, 1)), safe=False )

def delete_search(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    if request.POST.get('item') == 'age' or request.POST.get('item') == 'datetime' or request.POST.get('item') == 'time':
        MiniTableSearch.objects.filter(url=request.POST.get('url'), manager=request.user, shop=auth_login.shop, company=auth_login.company, page=request.POST.get('page'), item=request.POST.get('item')+'_from').all().delete()
        MiniTableSearch.objects.filter(url=request.POST.get('url'), manager=request.user, shop=auth_login.shop, company=auth_login.company, page=request.POST.get('page'), item=request.POST.get('item')+'_to').all().delete()
    else:
        MiniTableSearch.objects.filter(url=request.POST.get('url'), manager=request.user, shop=auth_login.shop, company=auth_login.company, page=request.POST.get('page'), item=request.POST.get('item')).all().delete()
    return JsonResponse( {}, safe=False )

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('number')))), safe=False )