from django.urls import path, include

app_name = 'company'

urlpatterns = [
    path('flow/', include('company.flow.urls')),
    path('question/', include('company.question.urls')),
    path('richmenu/', include('company.richmenu.urls')),
    path('setting/', include('company.setting.urls')),
    path('shop/', include('company.shop.urls')),
    path('tag/', include('company.tag.urls')),
    path('template/', include('company.template.urls')),
]