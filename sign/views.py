from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.template.loader import get_template
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View

from sign.mixins import HeadLoginMixin

from sign.forms import ManagerLoginForm

from sign.models import AuthLogin, ManagerProfile, EmailChangeToken, PasswordChangeToken

import environ
import datetime
import uuid

env = environ.Env()
env.read_env('.env')

class ManagerLoginView(LoginView):
    title = 'ログイン'
    form_class = ManagerLoginForm
    template_name = 'sign/login.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            if request.user.head_flg:
                return redirect('/head/shop/')
            elif request.user.company_flg:
                return redirect('/head/shop/')
            elif request.user.status <= 1:
                return redirect('/setting/')
            else:
                return redirect('/dashboard/')
        else:
            return render(self.request, self.template_name, {'title': self.title})
    
    def get_success_url(self):
        if self.request.user.head_flg:
            # return self.get_redirect_url() or resolve_url('head:shop:index')
            return self.get_redirect_url() or resolve_url('head:setting:index')
        elif self.request.user.company_flg:
            if AuthLogin.objects.filter(user=self.request.user).exists():
                auth_login = AuthLogin.objects.filter(user=self.request.user).first()
                auth_login.company = self.request.user.company
                auth_login.shop = self.request.user.shop
                auth_login.save()
            else:
                AuthLogin.objects.create(
                    id = str(uuid.uuid4()),
                    user = self.request.user,
                    company = self.request.user.company,
                )
            if self.request.user.status <= 1:
                return self.get_redirect_url() or resolve_url('setting:index')
            else:
                return self.get_redirect_url() or resolve_url('dashboard:index')
        else:
            if AuthLogin.objects.filter(user=self.request.user).exists():
                auth_login = AuthLogin.objects.filter(user=self.request.user).first()
                auth_login.shop = self.request.user.shop
                auth_login.save()
            else:
                AuthLogin.objects.create(
                    id = str(uuid.uuid4()),
                    user = self.request.user,
                    company = self.request.user.company,
                    shop = self.request.user.shop,
                )
            if self.request.user.status <= 1:
                return self.get_redirect_url() or resolve_url('setting:index')
            else:
                return self.get_redirect_url() or resolve_url('dashboard:index')

    def form_invalid(self, form):
        for error_message in form.errors.as_data():
            messages.add_message( self.request, messages.ERROR, form.errors.as_data()[error_message][0].message )
        return render(self.request, self.template_name, {'title': self.title, 'form': form})

class ManagerLogoutView(LogoutView):
    next_page = '/login'



class HeadEmailChangeView(HeadLoginMixin, View):
    template_name = 'sign/head/change_email.html'
    title = 'メールアドレス変更'

    def get(self, request, **kwargs):
        user = None
        try:
            token = force_str(urlsafe_base64_decode(kwargs.get("uidb64")))
            temp_user = get_object_or_404(EmailChangeToken, token=token)
            user = temp_user.manager
        except:
            user = None
        
        EmailChangeToken.objects.filter(token=token).delete()
        if user == None:
            return render(self.request, self.template_name, {'title': self.title, 'user': user, 'status': 1})
        elif datetime.datetime.now() > temp_user.expiration_date:
            return render(self.request, self.template_name, {'title': self.title, 'user': user, 'status': 2})
        else:
            user.email = temp_user.email
            user.save()

            if env('ENCODING') == 'True':
                site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")
            else:
                site_name = env('SITE_NAME')
            subject = '【' + site_name + '】メールアドレス変更完了メール'
            template = get_template('head/setting/email/change_email_complete.txt')
            site = get_current_site(request)
            context = {
                'protocol': 'https' if request.is_secure() else 'http',
                'domain': site.domain,
                'user': user,
                'site_name': site_name,
            }
            send_mail(subject, template.render(context), settings.EMAIL_HOST_USER, [user.email])
            
            return render(self.request, self.template_name, {'title': self.title, 'user': user, 'status': 0})



class HeadPasswordChangeView(HeadLoginMixin, View):
    template_name = 'sign/head/change_password.html'
    title = 'パスワード変更'

    def get(self, request, **kwargs):
        user = None
        try:
            token = force_str(urlsafe_base64_decode(kwargs.get("uidb64")))
            temp_user = get_object_or_404(PasswordChangeToken, token=token)
            user = temp_user.manager
        except:
            user = None

        PasswordChangeToken.objects.filter(token=token).delete()
        if user == None:
            return render(self.request, self.template_name, {'title': self.title, 'status': 1})
        elif datetime.datetime.now() > temp_user.expiration_date:
            return render(self.request, self.template_name, {'title': self.title, 'status': 2})
        else:
            if ManagerProfile.objects.filter(manager=user).exists():
                profile = ManagerProfile.objects.filter(manager=user).first()
                if profile.family_name and profile.first_name:
                    user.status = 3
                else:
                    user.status = 2
            else:
                user.status = 2
            user.password = temp_user.password
            user.save()

            if env('ENCODING') == 'True':
                site_name = env('SITE_NAME').encode("shift-jis").decode("utf-8", errors="ignore")
            else:
                site_name = env('SITE_NAME')
            subject = '【' + site_name + '】パスワード変更完了メール'
            template = get_template('head/setting/email/change_password_complete.txt')
            site = get_current_site(request)
            context = {
                'protocol': 'https' if request.is_secure() else 'http',
                'domain': site.domain,
                'user': user,
                'site_name': site_name,
            }
            send_mail(subject, template.render(context), settings.EMAIL_HOST_USER, [user.email])

        return render(self.request, self.template_name, {'title': self.title, 'status': 0})