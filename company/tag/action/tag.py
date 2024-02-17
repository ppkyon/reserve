from django.http import JsonResponse

from sign.models import AuthLogin
from tag.models import CompanyTagGenre, CompanyTag

from table.action import action_search
from company.tag.action.list import get_action_tag_list

from common import create_code, get_model_field

import uuid

def save(request):
    if request.POST.get('name'):
        if request.POST.get('id'):
            tag = CompanyTag.objects.filter(display_id=request.POST.get('id')).first()
            tag.name = request.POST.get('name')
            tag.save()
        else:
            tag_genre = CompanyTagGenre.objects.filter(display_id=request.POST.get('genre')).first()
            tag = CompanyTag.objects.create(
                id = str(uuid.uuid4()),
                display_id = create_code(12, CompanyTag),
                genre = tag_genre,
                name = request.POST.get('name'),
            )

            tag_genre.count = tag_genre.count + 1
            tag_genre.save()

        return JsonResponse( {'id': tag.display_id, 'date': tag.created_at.strftime('%Y/%m/%d %H:%M')}, safe=False )
        
    return JsonResponse( {'id': ''}, safe=False )

def delete(request):
    tag = CompanyTag.objects.filter(display_id=request.POST.get('id')).first()
    tag_genre = CompanyTagGenre.objects.filter(id=tag.genre.id).first()
    tag_genre.count = tag_genre.count - 1
    tag_genre.save()
    tag.delete()
    return JsonResponse( {}, safe=False )

def favorite(request):
    tag = CompanyTag.objects.filter(display_id=request.POST.get('id')).first()
    if tag.favorite_flg:
        tag.favorite_flg = False
    else:
        tag.favorite_flg = True
    tag.save()
    return JsonResponse( {'check': tag.favorite_flg}, safe=False )

def get(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    action_search(request, None, auth_login.company)

    tag_list = get_action_tag_list(request.POST.get('url'), request.user, CompanyTagGenre.objects.filter(display_id=request.POST.get('id')).first())
    for tag_index, tag_item in enumerate( tag_list ):
        tag_list[tag_index]['display_date'] = tag_item['created_at'].strftime('%Y/%m/%d %H:%M')
    return JsonResponse( list(tag_list), safe=False )



def get_all(request):
    auth_login = AuthLogin.objects.filter(user=request.user).first()
    tag_genre_list = CompanyTagGenre.objects.filter(company=auth_login.company).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTagGenre)).all()
    tag_list = CompanyTag.objects.filter(genre=CompanyTagGenre.objects.filter(company=auth_login.company).order_by('-favorite_flg', '-created_at').first()).order_by('-favorite_flg', '-created_at').values(*get_model_field(CompanyTag)).all()
    for tag_index, tag_item in enumerate(tag_list):
        tag_list[tag_index]['display_date'] = tag_item['created_at'].strftime('%Y/%m/%d %H:%M')
    return JsonResponse( {'genre_list': list(tag_genre_list), 'tag_list': list(tag_list)}, safe=False )