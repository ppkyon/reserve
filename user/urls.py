from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/', views.DetailView.as_view(), name='detail'),
]
