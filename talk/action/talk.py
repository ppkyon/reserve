from django.http import JsonResponse

from talk.models import TalkUpdate

def update(request):
    talk_update = TalkUpdate.objects.filter(manager=request.user).first()
    if talk_update:
        return JsonResponse( {'update': talk_update.update_flg}, safe=False )
    else:
        return JsonResponse( {'update': False}, safe=False )