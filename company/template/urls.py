from django.urls import path

from company.template import views
from company.template.action import text, video, richmessage, richvideo, cardtype, greeting

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
    path('text/all/get/', text.get_all, name='get_all_text'),

    path('video/save/', video.save, name='save_video'),
    path('video/save/check/', video.save_check, name='save_video_check'),
    path('video/delete/', video.delete, name='delete_video'),
    path('video/copy/', video.copy, name='copy_video'),
    path('video/search/', video.search, name='search_video'),
    path('video/paging/', video.paging, name='paging_video'),
    path('video/get/', video.get, name='get_video'),
    path('video/all/get/', video.get_all, name='get_all_video'),
    
    path('richmessage/save/', richmessage.save, name='save_richmessage'),
    path('richmessage/save/check/', richmessage.save_check, name='save_richmessage_check'),
    path('richmessage/delete/', richmessage.delete, name='delete_richmessage'),
    path('richmessage/copy/', richmessage.copy, name='copy_richmessage'),
    path('richmessage/search/', richmessage.search, name='search_richmessage'),
    path('richmessage/paging/', richmessage.paging, name='paging_richmessage'),
    path('richmessage/get/', richmessage.get, name='get_richmessage'),
    path('richmessage/all/get/', richmessage.get_all, name='get_all_richmessage'),
    
    path('richvideo/save/', richvideo.save, name='save_richvideo'),
    path('richvideo/save/check/', richvideo.save_check, name='save_richvideo_check'),
    path('richvideo/delete/', richvideo.delete, name='delete_richvideo'),
    path('richvideo/copy/', richvideo.copy, name='copy_richvideo'),
    path('richvideo/search/', richvideo.search, name='search_richvideo'),
    path('richvideo/paging/', richvideo.paging, name='paging_richvideo'),
    path('richvideo/get/', richvideo.get, name='get_richvideo'),
    path('richvideo/all/get/', richvideo.get_all, name='get_all_richvideo'),
    
    path('cardtype/save/', cardtype.save, name='save_cardtype'),
    path('cardtype/save/check/', cardtype.save_check, name='save_cardtype_check'),
    path('cardtype/delete/', cardtype.delete, name='delete_cardtype'),
    path('cardtype/copy/', cardtype.copy, name='copy_cardtype'),
    path('cardtype/search/', cardtype.search, name='search_cardtype'),
    path('cardtype/paging/', cardtype.paging, name='paging_cardtype'),
    path('cardtype/get/', cardtype.get, name='get_cardtype'),
    path('cardtype/all/get/', cardtype.get_all, name='get_all_cardtype'),
    
    path('greeting/save/', greeting.save, name='save_greeting'),
    path('greeting/save/check/', greeting.save_check, name='save_greeting_check'),
]