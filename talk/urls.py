from django.urls import path

from talk import views
from talk.action import talk, user, change, send

app_name = 'talk'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('talk/update', talk.update, name='update_talk'),
    
    path('user/search', user.search, name='search_user'),
    path('user/change', user.change, name='change_user'),
    
    path('text/send', send.text, name='send_text'),
    path('image/send', send.image, name='send_image'),
    path('video/send', send.video, name='send_video'),
    path('template/send', send.template, name='send_template'),
    
    path('pin/change', change.pin, name='change_pin'),
    path('status/change', change.status, name='change_status'),
    path('manager/change', change.manager, name='change_manager'),
]
