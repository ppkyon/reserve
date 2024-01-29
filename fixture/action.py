from django.http import JsonResponse

from fixture.models import WorkParent, WorkChild

from common import get_model_field

def get_work(request):
    parent = WorkParent.objects.filter(value=request.POST.get('value')).first()
    child = list(WorkChild.objects.filter(parent=parent).values(*get_model_field(WorkChild)).all())
    return JsonResponse( child, safe=False )