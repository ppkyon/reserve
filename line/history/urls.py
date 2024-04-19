from django.urls import path

from line.history import views
from line.history.action import check, get, send

app_name = 'history'

urlpatterns = [
    path('<int:login>/', views.IndexView.as_view(), name='index'),
    
    path('check/', check.check, name='check'),
    
    path('date/get/', get.date, name='get_date'),
    path('question/get/', get.question, name='get_question'),
    
    path('send/', send.send, name='send'),
    path('question/', send.question, name='question'),
]
