from django.urls import path

from line.reserve import action, views

app_name = 'reserve'

urlpatterns = [
    path('<int:login>/', views.IndexView.as_view(), name='index'),
    
    path('check/', action.check, name='check'),

    path('course/get/', action.get_course, name='get_course'),
    path('date/get/', action.get_date, name='get_date'),
    path('question/get/', action.get_question, name='get_question'),

    path('send/', action.send, name='send'),
]
