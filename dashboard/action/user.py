from django.http import JsonResponse

from user.models import LineUser

def check(request):
    user = LineUser.objects.filter(display_id=request.POST.get('id')).first()
    user.check_flg = True
    user.save()
    return JsonResponse( {}, safe=False )