from django.urls import path

from dashboard import views
from dashboard.action import schedule

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    path('save/', schedule.check, name='check_schedule'),
]