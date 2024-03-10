from django.urls import path

from head.flow import views
from head.flow.action import flow

app_name = 'flow'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('edit/', views.EditView.as_view(), name='edit'),
    
    path('save/', flow.save, name='save'),
    path('save/check/', flow.save_check, name='save_check'),
    path('search/', flow.search, name='search'),
    path('paging/', flow.paging, name='paging'),
    path('valid/', flow.valid, name='valid'),
]