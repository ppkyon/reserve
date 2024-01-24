from django.urls import path

from table import action

app_name = 'table'

urlpatterns = [
    path('sort', action.sort, name='sort'),
]
