from django.urls import path

from company.shop import views
from company.shop.action import shop

app_name = 'shop'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('add/', shop.add, name='add'),
    path('save/', shop.save, name='save'),
    path('save/check', shop.save_check, name='save_check'),
    path('profile/get', shop.get_profile, name='get_profile'),
]
