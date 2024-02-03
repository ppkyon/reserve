from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from sign.models import AuthCompany, AuthShop, AuthLogin

import uuid

class HeadLoginMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.status == 0 or not request.user.head_flg or request.user.delete_flg:
            return redirect('/logout')
        return super().dispatch(request, *args, **kwargs)

class CompanyLoginMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.status == 0 or ( not request.user.head_flg and not request.user.company_flg ) or request.user.delete_flg:
            return redirect('/logout')
        
        if request.GET.get("login_id"):
            if AuthLogin.objects.filter(user=request.user).exists():
                auth_login = AuthLogin.objects.filter(user=request.user).first()
                auth_login.company = AuthCompany.objects.filter(display_id=request.GET.get("login_id")).first()
                auth_login.save()
            else:
                auth_login = AuthLogin.objects.create(
                    id = str(uuid.uuid4()),
                    user = request.user,
                    company = AuthCompany.objects.filter(display_id=request.GET.get("login_id")).first(),
                )
        
        auth_login = AuthLogin.objects.filter(user=request.user).first()
        if auth_login:
            request.company = auth_login.company

        return super().dispatch(request, *args, **kwargs)

class ShopLoginMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.status == 0 or request.user.delete_flg:
            return redirect('/logout')
        
        if request.GET.get("login_id"):
            shop = AuthShop.objects.filter(display_id=request.GET.get("login_id")).first()
            if AuthLogin.objects.filter(user=request.user).exists():
                auth_login = AuthLogin.objects.filter(user=request.user).first()
                auth_login.company = shop.company
                auth_login.shop = shop
                auth_login.save()
            else:
                auth_login = AuthLogin.objects.create(
                    id = str(uuid.uuid4()),
                    user = request.user,
                    company = shop.company,
                    shop = shop,
                )
        
        auth_login = AuthLogin.objects.filter(user=request.user).first()
        if auth_login:
            request.company = auth_login.company
            request.shop = auth_login.shop

        return super().dispatch(request, *args, **kwargs)