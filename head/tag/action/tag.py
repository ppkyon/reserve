from django.db.models import Q
from django.http import JsonResponse

from table.models import TableSearch
from tag.models import HeadTagGenre, HeadTag

from common import create_code, get_model_field
from table.action import set_search
from head.tag.action.list import get_action_tag_list

import uuid

def save(request):
    if request.POST.get('name'):
        if request.POST.get('id'):
            tag = HeadTag.objects.filter(display_id=request.POST.get('id')).first()
            tag.name = request.POST.get('name')
            tag.save()
        else:
            tag_genre = HeadTagGenre.objects.filter(display_id=request.POST.get('genre')).first()
            tag = HeadTag.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, HeadTag),
                genre = tag_genre,
                name = request.POST.get('name'),
            )

            tag_genre.count = tag_genre.count + 1
            tag_genre.save()

        return JsonResponse( {'id': tag.display_id, 'date': tag.created_at.strftime('%Y/%m/%d %H:%M')}, safe=False )
        
    return JsonResponse( {'id': ''}, safe=False )

def delete(request):
    tag = HeadTag.objects.filter(display_id=request.POST.get('id')).first()
    tag_genre = HeadTagGenre.objects.filter(id=tag.genre.id).first()
    tag_genre.count = tag_genre.count - 1
    tag_genre.save()
    tag.delete()
    return JsonResponse( {}, safe=False )

def favorite(request):
    tag = HeadTag.objects.filter(display_id=request.POST.get('id')).first()
    if tag.favorite_flg:
        tag.favorite_flg = False
    else:
        tag.favorite_flg = True
    tag.save()
    return JsonResponse( {'check': tag.favorite_flg}, safe=False )

def get(request):
    if request.POST.get('url'):
        set_search(request, None, None)

    tag_list = get_action_tag_list(request.POST.get('url'), request.user, HeadTagGenre.objects.filter(display_id=request.POST.get('id')).first())
    for tag_index, tag_item in enumerate( tag_list ):
        tag_list[tag_index]['display_date'] = tag_item['created_at'].strftime('%Y/%m/%d %H:%M')
    return JsonResponse( list(tag_list), safe=False )



def get_all(request):
    tag_genre_list = HeadTagGenre.objects.order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTagGenre)).all()
    tag_list = HeadTag.objects.filter(genre=HeadTagGenre.objects.order_by('-favorite_flg', '-created_at').first()).order_by('-favorite_flg', '-created_at').values(*get_model_field(HeadTag)).all()
    for tag_index, tag_item in enumerate(tag_list):
        tag_list[tag_index]['display_date'] = tag_item['created_at'].strftime('%Y/%m/%d %H:%M')
    return JsonResponse( {'genre_list': list(tag_genre_list), 'tag_list': list(tag_list)}, safe=False )