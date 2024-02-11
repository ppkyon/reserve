from django.db import models
from django.utils import timezone

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from fixture.models import Country, Prefecture, WorkParent, WorkChild

import os
import uuid

def account_image_path(self, filename):
    return "uploads/account/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

def head_image_path(self, filename):
    return "uploads/head/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

def manager_image_path(self, filename):
    return "uploads/manager/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]
    
def logo_image_path(self, filename):
    return "uploads/logo/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

def manager_profile_image_path(self, filename):
    return "uploads/profile/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

class AuthCompany(models.Model):
    status_choice = (
        (0, '停止中'),
        (1, '仮登録'),
        (2, '未認証'),
        (3, 'アクティブ'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    status = models.IntegerField(choices=status_choice, default=0)
    delete_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'auth_company'

class AuthShop(models.Model):
    status_choice = (
        (0, '停止中'),
        (1, '仮登録'),
        (2, '未認証'),
        (3, 'アクティブ'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="auth_shop")
    status = models.IntegerField(choices=status_choice, default=0)
    delete_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'auth_shop'

class AuthUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class AuthUser(AbstractBaseUser, PermissionsMixin):
    authority_choice = (
        (0, '一般'),
        (1, '閲覧者'),
        (2, '編集者'),
        (3, '管理者'),
    )
    status_choice = (
        (0, '停止中'),
        (1, '仮登録'),
        (2, '未認証'),
        (3, 'アクティブ'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="auth_user")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="auth_user")
    email = models.EmailField(blank=False, unique=True)
    authority = models.IntegerField(choices=authority_choice, default=0)
    status = models.IntegerField(choices=status_choice, default=0)
    author = models.CharField(max_length=255,null=True)
    head_flg = models.BooleanField(default=False)
    company_flg = models.BooleanField(default=False)
    delete_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = AuthUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_user'

class CompanyProfile(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_profile")
    head_family_name = models.CharField(max_length=255, null=True)
    head_first_name = models.CharField(max_length=255, null=True)
    head_family_name_kana = models.CharField(max_length=255, null=True)
    head_first_name_kana = models.CharField(max_length=255, null=True)
    head_phone_number = models.CharField(max_length=255, null=True)
    head_email = models.EmailField(blank=True, null=True)
    head_image = models.ImageField(upload_to=head_image_path, blank=True, null=True)
    manager_family_name = models.CharField(max_length=255, null=True)
    manager_first_name = models.CharField(max_length=255, null=True)
    manager_family_name_kana = models.CharField(max_length=255, null=True)
    manager_first_name_kana = models.CharField(max_length=255, null=True)
    manager_department = models.CharField(max_length=255, null=True)
    manager_phone_number = models.CharField(max_length=255, null=True)
    manager_email = models.EmailField(blank=True, null=True)
    manager_image = models.ImageField(upload_to=manager_image_path, blank=True, null=True)
    company_name = models.CharField(max_length=255, null=True)
    company_postcode = models.IntegerField(blank=True, null=True)
    company_prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, blank=True, null=True, related_name="company_profile")
    company_address = models.CharField(max_length=255, null=True)
    company_url = models.CharField(max_length=255, null=True)
    company_phone_number = models.CharField(max_length=255, null=True)
    company_work_parent = models.ForeignKey(WorkParent, on_delete=models.CASCADE, blank=True, null=True, related_name="company_profile")
    company_work_child = models.ForeignKey(WorkChild, on_delete=models.CASCADE, blank=True, null=True, related_name="company_profile")
    company_logo_image = models.ImageField(upload_to=logo_image_path, blank=True, null=True)
    memo = models.TextField(max_length=1000, blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_profile'

class ShopProfile(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_profile")
    account_name = models.CharField(max_length=255, null=True)
    account_image = models.ImageField(upload_to=account_image_path, blank=True, null=True)
    account_country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name="company_profile")
    head_family_name = models.CharField(max_length=255, null=True)
    head_first_name = models.CharField(max_length=255, null=True)
    head_family_name_kana = models.CharField(max_length=255, null=True)
    head_first_name_kana = models.CharField(max_length=255, null=True)
    head_phone_number = models.CharField(max_length=255, null=True)
    head_email = models.EmailField(blank=True, null=True)
    head_image = models.ImageField(upload_to=head_image_path, blank=True, null=True)
    manager_family_name = models.CharField(max_length=255, null=True)
    manager_first_name = models.CharField(max_length=255, null=True)
    manager_family_name_kana = models.CharField(max_length=255, null=True)
    manager_first_name_kana = models.CharField(max_length=255, null=True)
    manager_department = models.CharField(max_length=255, null=True)
    manager_phone_number = models.CharField(max_length=255, null=True)
    manager_email = models.EmailField(blank=True, null=True)
    manager_image = models.ImageField(upload_to=manager_image_path, blank=True, null=True)
    shop_name = models.CharField(max_length=255, null=True)
    shop_postcode = models.IntegerField(blank=True, null=True)
    shop_prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_profile")
    shop_address = models.CharField(max_length=255, null=True)
    shop_url = models.CharField(max_length=255, null=True)
    shop_phone_number = models.CharField(max_length=255, null=True)
    shop_logo_image = models.ImageField(upload_to=logo_image_path, blank=True, null=True)
    memo = models.TextField(max_length=1000, blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_profile'
        
class ShopLine(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_line")
    channel_id = models.CharField(max_length=255,null=True)
    channel_secret = models.CharField(max_length=255,null=True)
    channel_access_token = models.CharField(max_length=255,null=True)
    bot_id = models.CharField(max_length=255,null=True)
    liff_id = models.CharField(max_length=255,null=True)
    analytics_id = models.CharField(max_length=255,null=True)
    qrcode_id = models.CharField(max_length=255,null=True)
    reserve_id = models.CharField(max_length=255,null=True)
    follow_url = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_line'

class ManagerProfile(models.Model):
    sex_choice = (
        (1, '男性'),
        (2, '女性'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    manager = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name="manager_profile")
    family_name = models.CharField(max_length=255,null=True)
    first_name = models.CharField(max_length=255,null=True)
    family_name_kana = models.CharField(max_length=255,null=True)
    first_name_kana = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to=manager_profile_image_path, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    sex = models.IntegerField(choices=sex_choice, default=0)
    phone_number = models.CharField(max_length=255,null=True)
    department = models.CharField(max_length=255,null=True)
    job = models.CharField(max_length=255,null=True)
    work = models.CharField(max_length=255,null=True)
    color = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'manager_profile'



class EmailChangeToken(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    manager = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name="email_change_token")
    email = models.EmailField(null=True, blank=True)
    token = models.CharField(max_length=255, unique=True)
    expiration_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'email_change_token'

class PasswordChangeToken(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    manager = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name="password_change_token")
    password = models.EmailField(null=True, blank=True)
    token = models.CharField(max_length=255, unique=True)
    expiration_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'password_change_token'



class AuthLogin(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="auth_login")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="auth_login")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="auth_login")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'auth_login'