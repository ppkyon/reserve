from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from sign import views as sign_views

urlpatterns = [
    path('login/', sign_views.ManagerLoginView.as_view(), name='login'),
    path('logout/', sign_views.ManagerLogoutView.as_view(), name='logout'),
    
    path('head/email/change/<str:uidb64>/', sign_views.HeadEmailChangeView.as_view(), name='head_change_email'),
    path('head/password/change/<str:uidb64>/', sign_views.HeadPasswordChangeView.as_view(), name='head_change_password'),
    
    path('head/', include('head.urls')),
    path('table/', include('table.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)