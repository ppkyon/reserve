from django.db import models
from django.utils import timezone

from question.models import HeadQuestion, CompanyQuestion, ShopQuestion
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



class HeadTemplateVideo(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    name = models.CharField(max_length=255,null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_time = models.IntegerField(blank=True, null=True)
    video_size = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_video'

class CompanyTemplateVideo(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_video")
    name = models.CharField(max_length=255,null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_time = models.IntegerField(blank=True, null=True)
    video_size = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_video'

class ShopTemplateVideo(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_video")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_video")
    name = models.CharField(max_length=255,null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_time = models.IntegerField(blank=True, null=True)
    video_size = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_video'



class HeadTemplateRichMessage(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    type = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image240 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image300 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image460 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image700 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image1040 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_rich_message'

class CompanyTemplateRichMessage(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_rich_message")
    type = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image240 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image300 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image460 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image700 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image1040 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_rich_message'

class ShopTemplateRichMessage(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_rich_message")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_rich_message")
    type = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image240 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image300 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image460 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image700 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image1040 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_rich_message'

class HeadTemplateRichMessageItem(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'reserve'),
        (5, 'company'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(HeadTemplateRichMessage, on_delete=models.CASCADE, related_name="head_template_rich_message_item")
    number = models.CharField(max_length=1,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_rich_message_item")
    question = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_rich_message_item")
    label = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_rich_message_item'

class CompanyTemplateRichMessageItem(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'reserve'),
        (5, 'company'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(CompanyTemplateRichMessage, on_delete=models.CASCADE, related_name="company_template_rich_message_item")
    number = models.CharField(max_length=1,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_rich_message_item")
    question = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_rich_message_item")
    label = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_rich_message_item'

class ShopTemplateRichMessageItem(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'reserve'),
        (5, 'company'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(ShopTemplateRichMessage, on_delete=models.CASCADE, related_name="shop_template_rich_message_item")
    number = models.CharField(max_length=1,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_rich_message_item")
    question = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_rich_message_item")
    label = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_rich_message_item'



class HeadTemplateRichVideo(models.Model):
    text_choice = (
        (0, 'detail'),
        (1, 'install'),
        (2, 'buy'),
        (3, 'reserve'),
        (4, 'app'),
        (5, 'request'),
        (6, 'join'),
        (7, 'vote'),
        (8, 'search'),
        (9, 'contact'),
        (10, 'claim'),
        (11, 'video'),
        (12, 'custom'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    video = models.ImageField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_time = models.IntegerField(blank=True, null=True)
    video_size = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail240 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail300 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail460 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail700 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail1040 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    display_flg = models.BooleanField(default=False)
    url = models.CharField(max_length=255,null=True)
    text = models.IntegerField(choices=text_choice, default=0, blank=True, null=True)
    custom = models.CharField(max_length=255,null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_rich_video'

class CompanyTemplateRichVideo(models.Model):
    text_choice = (
        (0, 'detail'),
        (1, 'install'),
        (2, 'buy'),
        (3, 'reserve'),
        (4, 'app'),
        (5, 'request'),
        (6, 'join'),
        (7, 'vote'),
        (8, 'search'),
        (9, 'contact'),
        (10, 'claim'),
        (11, 'video'),
        (12, 'custom'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_rich_video")
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    video = models.ImageField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_time = models.IntegerField(blank=True, null=True)
    video_size = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail240 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail300 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail460 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail700 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail1040 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    display_flg = models.BooleanField(default=False)
    url = models.CharField(max_length=255,null=True)
    text = models.IntegerField(choices=text_choice, default=0, blank=True, null=True)
    custom = models.CharField(max_length=255,null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_rich_video'

class ShopTemplateRichVideo(models.Model):
    text_choice = (
        (0, 'detail'),
        (1, 'install'),
        (2, 'buy'),
        (3, 'reserve'),
        (4, 'app'),
        (5, 'request'),
        (6, 'join'),
        (7, 'vote'),
        (8, 'search'),
        (9, 'contact'),
        (10, 'claim'),
        (11, 'video'),
        (12, 'custom'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_rich_video")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_rich_video")
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    video = models.ImageField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_time = models.IntegerField(blank=True, null=True)
    video_size = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail240 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail300 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail460 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail700 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    video_thumbnail1040 = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    display_flg = models.BooleanField(default=False)
    url = models.CharField(max_length=255,null=True)
    text = models.IntegerField(choices=text_choice, default=0, blank=True, null=True)
    custom = models.CharField(max_length=255,null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_rich_video'



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