from django.urls import path

from user import views
from user.action import user, step, schedule, question

app_name = 'user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/', views.DetailView.as_view(), name='detail'),

    path('save/', user.save, name='save'),
    path('save/check', user.save_check, name='save_check'),
    path('paging/', user.paging, name='paging'),
    path('get/', user.get, name='get'),
    path('member/', user.member, name='member'),
    
    path('step/save/', step.save, name='save_step'),
    path('step/save/check', step.save_check, name='save_step_check'),
    path('step/get/', step.get, name='get_step'),
    
    path('schedule/get/', schedule.get, name='get_schedule'),
    path('schedule/send/', schedule.send, name='send_schedule'),
    
    path('question/save/', question.save, name='save_question'),
    path('question/save/check', question.save_check, name='save_question_check'),
    path('question/get/', question.get, name='get_question'),
]
