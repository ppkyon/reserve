from django.urls import path

from head.question import views
from head.question.action import question

app_name = 'question'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('edit/', views.EditView.as_view(), name='edit'),
    
    path('save/', question.save, name='save'),
    path('save/check/', question.save_check, name='save_check'),
    path('copy/', question.copy, name='copy'),
    path('delete/', question.delete, name='delete'),
    path('search/', question.search, name='search'),
    path('paging/', question.paging, name='paging'),
    path('get/', question.get, name='get'),
]