from django.http import JsonResponse

from sign.models import AuthUser, CompanyProfile, ShopProfile

def check_email(request):
    if AuthUser.objects.filter(email=request.POST.get('head_email')).exists():
        return JsonResponse( {'check': False}, safe=False )
    if AuthUser.objects.filter(email=request.POST.get('manager_email')).exists():
        return JsonResponse( {'check': False}, safe=False )
    if CompanyProfile.objects.filter(head_email=request.POST.get('head_email')).exists() or CompanyProfile.objects.filter(manager_email=request.POST.get('head_email')).exists():
        return JsonResponse( {'check': False}, safe=False )
    if CompanyProfile.objects.filter(head_email=request.POST.get('manager_email')).exists() or CompanyProfile.objects.filter(manager_email=request.POST.get('manager_email')).exists():
        return JsonResponse( {'check': False}, safe=False )
    if ShopProfile.objects.filter(head_email=request.POST.get('head_email')).exists() or ShopProfile.objects.filter(manager_email=request.POST.get('head_email')).exists():
        return JsonResponse( {'check': False}, safe=False )
    if ShopProfile.objects.filter(head_email=request.POST.get('manager_email')).exists() or ShopProfile.objects.filter(manager_email=request.POST.get('manager_email')).exists():
        return JsonResponse( {'check': False}, safe=False )
    return JsonResponse( {'check': True}, safe=False )