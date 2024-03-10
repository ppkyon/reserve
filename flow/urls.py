from django.urls import path

from flow.data import default

app_name = 'flow'

urlpatterns = [
    path('default/data/add/', default.add, name='add_default_data'),
]
