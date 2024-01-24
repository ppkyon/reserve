from django.urls import path, include

app_name = 'head'

urlpatterns = [
    path('setting/', include('head.setting.urls')),
    path('tag/', include('head.tag.urls')),
]