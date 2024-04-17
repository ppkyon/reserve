from django.urls import path

from line.history import views
from line.history.action import check

app_name = 'history'

urlpatterns = [
    path('<int:login>/', views.IndexView.as_view(), name='index'),
    
    path('check/', check.check, name='check'),
]
