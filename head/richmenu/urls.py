from django.urls import path

from head.richmenu import views
from head.richmenu.action import richmenu

app_name = 'richmenu'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('edit/', views.EditView.as_view(), name='edit'),
    
    path('save/', richmenu.save, name='save'),
    path('save/check/', richmenu.save_check, name='save_check'),
    path('delete/', richmenu.delete, name='delete'),
    path('copy/', richmenu.copy, name='copy'),
    path('search/', richmenu.search, name='search'),
    path('paging/', richmenu.paging, name='paging'),
    path('get/', richmenu.get, name='get'),
    path('all/get/', richmenu.get_all, name='get_all'),
]