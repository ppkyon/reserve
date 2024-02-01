from django.urls import path

from account import views, action

app_name = 'account'

urlpatterns = [
    path('company/', views.CompanyView.as_view(), name='company'),
    path('company/check/', views.CompanyCheckView.as_view(), name='company_check'),
    path('company/end/', views.CompanyEndView.as_view(), name='company_end'),
    
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('shop/check/', views.ShopCheckView.as_view(), name='shop_check'),
    path('shop/end/', views.ShopEndView.as_view(), name='shop_end'),

    path('email/check/', action.check_email, name='check_email'),
]
