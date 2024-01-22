from django.urls import path

from head.setting import views
from head.setting.action import manager, email, password

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
]
