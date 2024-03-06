from django.http import JsonResponse

def search(request):
    return JsonResponse( {}, safe=False )

def paging(request):
    return JsonResponse( {}, safe=False )