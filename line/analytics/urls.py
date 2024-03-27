from django.urls import path

from . import action, views

app_name = 'analytics'

urlpatterns = [
    path('<int:login>/', views.IndexView.as_view(), name='index'),
    
    path('url/', action.url, name='url'),
]
