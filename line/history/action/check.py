from django.http import JsonResponse

def check(request):
    return JsonResponse( {}, safe=False )