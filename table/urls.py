from django.urls import path

from table import action

app_name = 'table'

urlpatterns = [
    path('number', action.number, name='number'),
    path('sort', action.sort, name='sort'),
]
