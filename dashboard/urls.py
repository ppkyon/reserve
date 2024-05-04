from django.urls import path

from dashboard import views
from dashboard.action import schedule, user

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    path('schedule/check/', schedule.check, name='check_schedule'),
    path('user/check/', user.check, name='check_user'),
]