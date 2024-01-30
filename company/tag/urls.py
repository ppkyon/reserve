from django.urls import path

from company.tag import views

app_name = 'tag'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
