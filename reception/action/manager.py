from django.http import JsonResponse

def save(request):
    return JsonResponse( {}, safe=False )

def save_check(request):
    return JsonResponse( {'check': True}, safe=False )



def get(request):
    return JsonResponse( {}, safe=False )