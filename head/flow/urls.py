from django.urls import path

from head.flow import views
from head.flow.action import flow

app_name = 'flow'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('search/', flow.search, name='search'),
    path('paging/', flow.paging, name='paging'),
]