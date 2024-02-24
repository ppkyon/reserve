from django.urls import path

from head.template import views
from head.template.action import text, video, richmessage, richvideo, cardtype, greeting

app_name = 'template'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('text/', views.TextView.as_view(), name='text'),
    path('text/edit/', views.TextEditView.as_view(), name='edit_text'),
    path('video/', views.VideoView.as_view(), name='video'),
    path('video/edit/', views.VideoEditView.as_view(), name='edit_video'),
    path('richmessage/', views.RichMessageView.as_view(), name='richmessage'),
    path('richmessage/edit/', views.RichMessageEditView.as_view(), name='edit_richmessage'),
    path('richvideo/', views.RichVideoView.as_view(), name='richvideo'),
    path('richvideo/edit/', views.RichVideoEditView.as_view(), name='edit_richvideo'),
    path('cardtype/', views.CardTypeView.as_view(), name='cardtype'),
    path('cardtype/edit/', views.CardTypeEditView.as_view(), name='edit_cardtype'),
    path('greeting/', views.GreetingView.as_view(), name='greeting'),

    path('text/save/', text.save, name='save_text'),
    path('text/save/check/', text.save_check, name='save_text_check'),
    path('text/delete/', text.delete, name='delete_text'),
    path('text/copy/', text.copy, name='copy_text'),
    path('text/search/', text.search, name='search_text'),
    path('text/paging/', text.paging, name='paging_text'),
    path('text/get/', text.get, name='get_text'),

    path('video/search/', video.search, name='search_video'),
    
    path('richmessage/search/', richmessage.search, name='search_richmessage'),
    
    path('richvideo/search/', richvideo.search, name='search_richvideo'),
    
    path('cardtype/search/', cardtype.search, name='search_cardtype'),
    
    path('greeting/save/', greeting.save, name='save_greeting'),
    path('greeting/save/check/', greeting.save_check, name='save_greeting_check'),
]