from django.urls import path

from temp import views
from temp.action import user, step, question

app_name = 'temp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/', views.DetailView.as_view(), name='detail'),

    path('save/', user.save, name='save'),
    path('save/check', user.save_check, name='save_check'),
    path('get/', user.get, name='get'),
    path('member/', user.member, name='member'),
    
    path('step/save/', step.save, name='save_step'),
    path('step/save/check', step.save_check, name='save_step_check'),
    
    path('question/save/', question.save, name='save_question'),
    path('question/save/check', question.save_check, name='save_question_check'),
    path('question/get/', question.get, name='get_question'),
]