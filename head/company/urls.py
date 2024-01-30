from django.urls import path

from head.company import views
from head.company.action import company

app_name = 'company'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('add/', company.add, name='add'),
    path('save/', company.save, name='save'),
    path('save/check', company.save_check, name='save_check'),
    path('start/', company.start, name='start'),
    path('profile/get', company.get_profile, name='get_profile'),
]
