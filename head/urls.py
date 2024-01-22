from django.urls import path, include

app_name = 'head'

urlpatterns = [
    path('setting/', include('head.setting.urls')),
]