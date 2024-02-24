from django.db import models
from django.utils import timezone

from sign.models import AuthCompany, AuthShop

import os
import uuid

def template_image_path(self, filename):
    return "uploads/template/image/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

def template_video_path(self, filename):
    return "uploads/template/video/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

def template_video_thumbnail_path(self, filename):
    return "uploads/template/video/thumbnail/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

class HeadTemplateText(models.Model):

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    name = models.CharField(max_length=255,null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_text'

class CompanyTemplateText(models.Model):

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_text")
    name = models.CharField(max_length=255,null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_text'

class ShopTemplateText(models.Model):

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text")
    name = models.CharField(max_length=255,null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_text'

class HeadTemplateTextItem(models.Model):
    message_type_choice = (
        (1, 'text'),
        (2, 'image'),
        (3, 'video'),
        (4, 'template'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(HeadTemplateText, on_delete=models.CASCADE, related_name="head_template_text_item")
    number = models.IntegerField(default=0)
    message_type = models.IntegerField(choices=message_type_choice, default=0)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_text_item'

class CompanyTemplateTextItem(models.Model):
    message_type_choice = (
        (1, 'text'),
        (2, 'image'),
        (3, 'video'),
        (4, 'template'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(CompanyTemplateText, on_delete=models.CASCADE, related_name="company_template_text_item")
    number = models.IntegerField(default=0)
    message_type = models.IntegerField(choices=message_type_choice, default=0)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_text_item'

class ShopTemplateTextItem(models.Model):
    message_type_choice = (
        (1, 'text'),
        (2, 'image'),
        (3, 'video'),
        (4, 'template'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(ShopTemplateText, on_delete=models.CASCADE, related_name="shop_template_text_item")
    number = models.IntegerField(default=0)
    message_type = models.IntegerField(choices=message_type_choice, default=0)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_text_item'



class HeadTemplateGreeting(models.Model):
    message_type_choice = (
        (1, 'text'),
        (2, 'image'),
        (3, 'video'),
        (4, 'template'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    number = models.IntegerField(default=0)
    message_type = models.IntegerField(choices=message_type_choice, default=0)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_greeting'

class CompanyTemplateGreeting(models.Model):
    message_type_choice = (
        (1, 'text'),
        (2, 'image'),
        (3, 'video'),
        (4, 'template'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_greeting")
    number = models.IntegerField(default=0)
    message_type = models.IntegerField(choices=message_type_choice, default=0)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_greeting'

class ShopTemplateGreeting(models.Model):
    message_type_choice = (
        (1, 'text'),
        (2, 'image'),
        (3, 'video'),
        (4, 'template'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_greeting")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_greeting")
    number = models.IntegerField(default=0)
    message_type = models.IntegerField(choices=message_type_choice, default=0)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_greeting'