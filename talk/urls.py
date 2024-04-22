from django.urls import path

from talk import views

app_name = 'talk'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
