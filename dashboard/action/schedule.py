from django.http import JsonResponse

from flow.models import UserFlowSchedule

def check(request):
    schedule = UserFlowSchedule.objects.filter(display_id=request.POST.get('id')).first()
    schedule.check_flg = True
    schedule.save()
    return JsonResponse( {}, safe=False )