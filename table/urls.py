from django.urls import path

from table import action

app_name = 'table'

urlpatterns = [
    path('number/', action.number, name='number'),
    path('sort/', action.sort, name='sort'),
    
    path('mini/number/', action.mini_number, name='mini_number'),
    path('mini/sort/', action.mini_sort, name='mini_sort'),
]
