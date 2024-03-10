from django.db import models
from django.utils import timezone

from question.models import HeadQuestion, CompanyQuestion, ShopQuestion
from sign.models import AuthCompany, AuthShop
from template.models import HeadTemplateVideo, CompanyTemplateVideo, ShopTemplateVideo

import os
import uuid

def richmenu_image_path(self, filename):
    return "uploads/richmenu/image/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

class HeadRichMenu(models.Model):
    type_choice = (
        (0, 'default'),
        (1, 'another'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    name = models.CharField(max_length=255,null=True)
    menu_type = models.IntegerField(choices=type_choice, default=0)
    menu_flg = models.BooleanField(default=False)
    menu_text = models.CharField(max_length=255,null=True)
    type = models.IntegerField(default=0)
    image = models.ImageField(upload_to=richmenu_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_rich_menu'

class CompanyRichMenu(models.Model):
    type_choice = (
        (0, 'default'),
        (1, 'another'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    parent = models.ForeignKey(HeadRichMenu, on_delete=models.CASCADE, blank=True, null=True, related_name="company_rich_menu")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_rich_menu")
    name = models.CharField(max_length=255,null=True)
    menu_type = models.IntegerField(choices=type_choice, default=0)
    menu_flg = models.BooleanField(default=False)
    menu_text = models.CharField(max_length=255,null=True)
    type = models.IntegerField(default=0)
    image = models.ImageField(upload_to=richmenu_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_rich_menu'

class ShopRichMenu(models.Model):
    type_choice = (
        (0, 'default'),
        (1, 'another'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    parent = models.ForeignKey(CompanyRichMenu, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_rich_menu")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_rich_menu")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_rich_menu")
    name = models.CharField(max_length=255,null=True)
    menu_type = models.IntegerField(choices=type_choice, default=0)
    menu_flg = models.BooleanField(default=False)
    menu_text = models.CharField(max_length=255,null=True)
    type = models.IntegerField(default=0)
    image = models.ImageField(upload_to=richmenu_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_rich_menu'

class HeadRichMenuItem(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    rich_menu = models.ForeignKey(HeadRichMenu, on_delete=models.CASCADE, related_name="head_rich_menu_item")
    number = models.CharField(max_length=1,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_rich_menu_item")
    question = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="head_rich_menu_item")
    label = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_rich_menu_item'

class CompanyRichMenuItem(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    rich_menu = models.ForeignKey(CompanyRichMenu, on_delete=models.CASCADE, related_name="company_rich_menu_item")
    number = models.CharField(max_length=1,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_rich_menu_item")
    question = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_rich_menu_item")
    label = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_rich_menu_item'

class ShopRichMenuItem(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    rich_menu = models.ForeignKey(ShopRichMenu, on_delete=models.CASCADE, related_name="shop_rich_menu_item")
    number = models.CharField(max_length=1,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_rich_menu_item")
    question = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_rich_menu_item")
    label = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_rich_menu_item'