from django.urls import path

from dashboard import views
from dashboard.action import dashboard, schedule, user

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    path('search/', dashboard.search, name='search'),
    path('search/delete/', dashboard.delete_search, name='delete_search'),
    path('paging/', dashboard.paging, name='paging'),
    path('schedule/check/', schedule.check, name='check_schedule'),
    path('user/check/', user.check, name='check_user'),
]