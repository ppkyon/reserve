from django.urls import path, include

app_name = 'head'

urlpatterns = [
    path('company/', include('head.company.urls')),
    path('flow/', include('head.flow.urls')),
    path('question/', include('head.question.urls')),
    path('richmenu/', include('head.richmenu.urls')),
    path('setting/', include('head.setting.urls')),
    path('tag/', include('head.tag.urls')),
    path('template/', include('head.template.urls')),
]