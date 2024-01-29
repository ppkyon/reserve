from django.urls import path

from fixture import action

app_name = 'fixture'

urlpatterns = [
    path('work/get/', action.get_work, name='get_work'),
]
