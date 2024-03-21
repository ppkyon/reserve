from django.urls import path

from flow import views
from flow.action import flow
from flow.data import default

app_name = 'flow'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('edit/', views.EditView.as_view(), name='edit'),
    
    path('save/', flow.save, name='save'),
    path('save/check/', flow.save_check, name='save_check'),
    path('favorite/', flow.favorite, name='favorite'),
    path('search/', flow.search, name='search'),
    path('paging/', flow.paging, name='paging'),

    path('default/data/add/', default.add, name='add_default_data'),
]
