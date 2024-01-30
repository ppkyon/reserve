from django.urls import path

from company.shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
