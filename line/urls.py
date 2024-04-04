from django.urls import path, include

from line import callback

app_name = 'line'

urlpatterns = [
    path('callback/<int:login>/', callback.callback, name='callback'),
    
    path('relationship/', include('line.analytics.urls')),
    path('reserve/', include('line.reserve.urls')),
]
