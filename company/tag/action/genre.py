from django.http import JsonResponse

from sign.models import AuthLogin
from tag.models import CompanyTagGenre, CompanyTag

from common import create_code

import uuid

def save(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()

    if request.POST.get('name'):
        if request.POST.get('id'):
            tag_genre = CompanyTagGenre.objects.filter(display_id=request.POST.get('id')).first()
            tag_genre.name = request.POST.get('name')
            tag_genre.save()
        else:
            tag_genre = CompanyTagGenre.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, CompanyTagGenre),
                company = auth_login.company,
                name = request.POST.get('name'),
                count = 0,
            )
        count = CompanyTag.objects.filter(genre=tag_genre).count()
        return JsonResponse( {'id': tag_genre.display_id, 'count': count}, safe=False )

    return JsonResponse( {'id': ''}, safe=False )

def delete(request):
    CompanyTagGenre.objects.filter(display_id=request.POST.get('id')).first().delete()
    return JsonResponse( {}, safe=False )

def favorite(request):
    tag_genre = CompanyTagGenre.objects.filter(display_id=request.POST.get('id')).first()
    if tag_genre.favorite_flg:
        tag_genre.favorite_flg = False
    else:
        tag_genre.favorite_flg = True
    tag_genre.save()
    return JsonResponse( {'check': tag_genre.favorite_flg}, safe=False )