from django.http import JsonResponse

from tag.models import HeadTagGenre, HeadTag

from common import create_code

import uuid

def save(request):
    if request.POST.get('name'):
        if request.POST.get('id'):
            tag_genre = HeadTagGenre.objects.filter(display_id=request.POST.get('id')).first()
            tag_genre.name = request.POST.get('name')
            tag_genre.save()
        else:
            tag_genre = HeadTagGenre.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, HeadTagGenre),
                name = request.POST.get('name'),
                count = 0,
            )
        count = HeadTag.objects.filter(genre=tag_genre).count()
        return JsonResponse( {'id': tag_genre.display_id, 'count': count}, safe=False )

    return JsonResponse( {'id': ''}, safe=False )

def delete(request):
    HeadTagGenre.objects.filter(display_id=request.POST.get('id')).first().delete()
    return JsonResponse( {}, safe=False )

def favorite(request):
    tag_genre = HeadTagGenre.objects.filter(display_id=request.POST.get('id')).first()
    if tag_genre.favorite_flg:
        tag_genre.favorite_flg = False
    else:
        tag_genre.favorite_flg = True
    tag_genre.save()
    return JsonResponse( {'check': tag_genre.favorite_flg}, safe=False )