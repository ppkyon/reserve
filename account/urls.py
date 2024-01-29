from django.urls import path

from account import views, action

app_name = 'account'

urlpatterns = [
    path('company/', views.CompanyView.as_view(), name='company'),
    path('company/check/', views.CompanyCheckView.as_view(), name='company_check'),
    path('company/end/', views.CompanyEndView.as_view(), name='company_end'),

    path('email/check/', action.check_email, name='check_email'),
]
