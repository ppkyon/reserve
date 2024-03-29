from django.urls import path

from setting import views
from setting.action import manager, email, password, offline, online, setting

app_name = 'setting'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('manager/add/', manager.add, name='add_manager'),
    path('manager/add/check/', manager.add_check, name='add_manager_check'),
    path('manager/save/', manager.save, name='save_manager'),
    path('manager/save/check/', manager.save_check, name='save_manager_check'),
    path('manager/delete/', manager.delete, name='delete_manager'),
    path('manager/authority/save/', manager.save_authority, name='save_authority'),
    
    path('email/change/', email.change, name='change_email'),
    path('email/change/check/', email.change_check, name='change_email_check'),

    path('password/change/', password.change, name='change_password'),
    path('password/change/check/', password.change_check, name='change_password_check'),
    path('password/reset/', password.reset, name='reset_password'),

    path('offline/add/', offline.add, name='add_offline'),
    path('offline/add/check/', offline.add_check, name='add_offline_check'),
    path('offline/save/', offline.save, name='save_offline'),
    path('offline/save/check/', offline.save_check, name='save_offline_check'),
    path('offline/delete/', offline.delete, name='delete_offline'),
    
    path('online/add/', online.add, name='add_online'),
    path('online/add/check/', online.add_check, name='add_online_check'),
    path('online/save/', online.save, name='save_online'),
    path('online/save/check/', online.save_check, name='save_online_check'),
    path('online/delete/', online.delete, name='delete_online'),
    
    path('setting/search/', setting.search, name='search'),
    path('setting/get/', setting.get, name='get'),
    path('setting/time/get/', setting.get_time, name='get_time'),
]
