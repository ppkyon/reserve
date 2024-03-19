from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from sign import views as sign_views

urlpatterns = [
    path('login/', sign_views.ManagerLoginView.as_view(), name='login'),
    path('logout/', sign_views.ManagerLogoutView.as_view(), name='logout'),
    path('simple/login/', sign_views.SimpleLoginView.as_view(), name='simple'),
    
    path('head/email/change/<str:uidb64>/', sign_views.HeadEmailChangeView.as_view(), name='head_change_email'),
    path('head/password/change/<str:uidb64>/', sign_views.HeadPasswordChangeView.as_view(), name='head_change_password'),
    
    path('company/email/change/<str:uidb64>/', sign_views.CompanyEmailChangeView.as_view(), name='company_change_email'),
    path('company/password/change/<str:uidb64>/', sign_views.CompanyPasswordChangeView.as_view(), name='company_change_password'),
    
    path('email/change/<str:uidb64>/', sign_views.ShopEmailChangeView.as_view(), name='shop_change_email'),
    path('password/change/<str:uidb64>/', sign_views.ShopPasswordChangeView.as_view(), name='shop_change_password'),
    
    path('', include('dashboard.urls')),
    path('account/', include('account.urls')),
    path('company/', include('company.urls')),
    path('fixture/', include('fixture.urls')),
    path('flow/', include('flow.urls')),
    path('head/', include('head.urls')),
    path('question/', include('question.urls')),
    path('richmenu/', include('richmenu.urls')),
    path('setting/', include('setting.urls')),
    path('table/', include('table.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)