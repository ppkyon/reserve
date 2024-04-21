from django.urls import path

from proxy import views
from proxy.action import check, get, send

app_name = 'proxy'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('check/', check.check, name='check'),

    path('course/get/', get.course, name='get_course'),
    path('date/get/', get.date, name='get_date'),
    path('question/get/', get.question, name='get_question'),

    path('send/', send.send, name='send'),
]