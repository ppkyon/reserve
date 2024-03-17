from django.urls import path

from company.shop import views
from company.shop.action import shop, setting

app_name = 'shop'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/', views.DetailView.as_view(), name='detail'),
    
    path('add/', shop.add, name='add'),
    path('save/', shop.save, name='save'),
    path('save/check', shop.save_check, name='save_check'),
    path('delete/', shop.delete, name='delete'),
    path('search/', shop.search, name='search'),
    path('paging/', shop.paging, name='paging'),
    path('start/', shop.start, name='start'),
    path('profile/get', shop.get_profile, name='get_profile'),
    
    path('line/save/', shop.save_line, name='save_line'),

    path('notice/setting/save/', setting.save_notice, name='save_notice'),
]
