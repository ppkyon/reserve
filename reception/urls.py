from django.urls import path

from reception import views
from reception.action import data, place, manager

app_name = 'reception'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('place/', views.PlaceView.as_view(), name='place'),
    path('manager/', views.ManagerView.as_view(), name='manager'),
    
    path('data/save/', data.save, name='save_data'),
    path('data/save/check/', data.save_check, name='save_data_check'),
    path('place/save', place.save, name='save_place'),
    path('place/save/check/', place.save_check, name='save_place_check'),
    path('manager/save', manager.save, name='save_manager'),
    path('manager/save/check/', manager.save_check, name='save_manager_check'),
    
    path('place/setting/get/', place.get, name='get_place'),
    path('manager/setting/get/', manager.get, name='get_manager'),
]
