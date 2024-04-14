from django.db import models
from django.utils import timezone

from sign.models import AuthShop

import os
import uuid

def user_profile_image_path(self, filename):
    return "uploads/user/profile/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

class LineUser(models.Model):
    status_choice = (
        (0, 'なし'),
        (1, 'フォロー'),
        (2, 'アンフォロー'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, related_name="line_user")
    line_user_id = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, null=True)
    display_image = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(choices=status_choice, default=0)
    member_flg = models.BooleanField(default=False)
    delete_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'line_user'

class UserProfile(models.Model):
    sex_choice = (
        (1, '男性'),
        (2, '女性'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    atelle_id = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name="user_profile")
    email = models.EmailField(blank=False)
    name = models.CharField(max_length=255,null=True)
    name_kana = models.CharField(max_length=255,null=True)
    age = models.IntegerField(blank=True, null=True)
    sex = models.IntegerField(choices=sex_choice, default=0)
    phone_number = models.CharField(max_length=255,null=True)
    birth = models.DateTimeField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True)
    background = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)
    memo = models.TextField(max_length=1000, blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_profile'
