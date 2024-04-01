from django.urls import path

from reserve import views
from reserve.action import basic, place, setting, facility, menu

app_name = 'reserve'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('basic/', views.BasicView.as_view(), name='basic'),
    path('place/', views.PlaceView.as_view(), name='place'),
    path('setting/', views.SettingView.as_view(), name='setting'),
    path('facility/', views.FacilityView.as_view(), name='facility'),
    path('menu/', views.MenuView.as_view(), name='menu'),
    
    path('basic/save', basic.save, name='save_basic'),
    path('basic/save/check/', basic.save_check, name='save_basic_check'),
    path('place/save', place.save, name='save_place'),
    path('place/save/check/', place.save_check, name='save_place_check'),
    path('setting/save', setting.save, name='save_setting'),
    path('setting/save/check/', setting.save_check, name='save_setting_check'),
    path('facility/save', facility.save, name='save_facility'),
    path('facility/save/check/', facility.save_check, name='save_facility_check'),
    path('menu/save', menu.save, name='save_menu'),
    path('menu/save/check/', menu.save_check, name='save_menu_check'),
]
