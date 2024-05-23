from django.urls import path

from line.reserve import views
from line.reserve.action import check, get, save, send

app_name = 'reserve'

urlpatterns = [
    path('<int:login>/', views.IndexView.as_view(), name='index'),
    
    path('check/', check.check, name='check'),

    path('course/get/', get.course, name='get_course'),
    path('date/get/', get.date, name='get_date'),
    path('question/get/', get.question, name='get_question'),
    
    path('temp/save/', save.temp, name='save_temp'),

    path('send/', send.send, name='send'),
]
