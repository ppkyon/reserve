from django.http import JsonResponse

from dashboard.action.list import get_list

def paging(request):
    return JsonResponse( list(get_list(request, int(request.POST.get('number')))), safe=False )