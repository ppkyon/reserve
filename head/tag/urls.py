from django.urls import path

from head.tag.action import genre, tag, list
from head.tag import views

app_name = 'tag'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('genre/save/', genre.save, name='save_genre'),
    path('genre/delete/', genre.delete, name='delete_genre'),
    path('genre/favorite/', genre.favorite, name='favorite_genre'),
    
    path('tag/save/', tag.save, name='save_tag'),
    path('tag/delete/', tag.delete, name='delete_tag'),
    path('tag/favorite/', tag.favorite, name='favorite_tag'),
    path('tag/get/', tag.get, name='get_tag'),
    
    path('tag/all/get/', tag.get_all, name='get_all_tag'),
]
