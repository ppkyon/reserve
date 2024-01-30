from django.urls import path, include

app_name = 'company'

urlpatterns = [
    path('setting/', include('company.setting.urls')),
    path('shop/', include('company.shop.urls')),
    path('tag/', include('company.tag.urls')),
]