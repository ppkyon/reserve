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
    parent = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_video")
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
    parent = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_video")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_video")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_video")
    name = models.CharField(max_length=255,null=True)
    video = models.FileField(upload_to=template_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_time = models.IntegerField(blank=True, null=True)
    video_size = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=template_video_thumbnail_path, blank=True, null=True)
    favorite_flg = models.BooleanField(default=False)
    use_flg = models.BooleanField(default=False)
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
    parent = models.ForeignKey(HeadTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_rich_message")
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
    parent = models.ForeignKey(CompanyTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_rich_message")
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
    favorite_flg = models.BooleanField(default=False)
    use_flg = models.BooleanField(default=False)
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
        (5, 'history'),
        (6, 'company'),
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
        (5, 'history'),
        (6, 'company'),
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
        (5, 'history'),
        (6, 'company'),
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
    parent = models.ForeignKey(HeadTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_rich_video")
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
    parent = models.ForeignKey(CompanyTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_rich_video")
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
    favorite_flg = models.BooleanField(default=False)
    use_flg = models.BooleanField(default=False)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_rich_video'



class HeadTemplateCardType(models.Model):
    type_choice = (
        (1, 'location'),
        (2, 'person'),
        (3, 'image'),
        (4, 'announce'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    count = models.IntegerField(default=0)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_card_type'

class CompanyTemplateCardType(models.Model):
    type_choice = (
        (1, 'location'),
        (2, 'person'),
        (3, 'image'),
        (4, 'announce'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    parent = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type")
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    count = models.IntegerField(default=0)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_card_type'

class ShopTemplateCardType(models.Model):
    type_choice = (
        (1, 'location'),
        (2, 'person'),
        (3, 'image'),
        (4, 'announce'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    parent = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type")
    name = models.CharField(max_length=255,null=True)
    title = models.CharField(max_length=255,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    count = models.IntegerField(default=0)
    favorite_flg = models.BooleanField(default=False)
    use_flg = models.BooleanField(default=False)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_card_type'

class HeadTemplateCardTypeAnnounce(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, related_name="head_template_card_type_announce")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    image_count = models.CharField(max_length=1,null=True)
    image_1 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_flg = models.BooleanField(default=False)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    description = models.CharField(max_length=255,null=True)
    description_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_card_type_announce'

class CompanyTemplateCardTypeAnnounce(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, related_name="company_template_card_type_announce")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    image_count = models.CharField(max_length=1,null=True)
    image_1 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_flg = models.BooleanField(default=False)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    description = models.CharField(max_length=255,null=True)
    description_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_card_type_announce'

class ShopTemplateCardTypeAnnounce(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, related_name="shop_template_card_type_announce")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    image_count = models.CharField(max_length=1,null=True)
    image_1 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_flg = models.BooleanField(default=False)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    description = models.CharField(max_length=255,null=True)
    description_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_card_type_announce'

class HeadTemplateCardTypeAnnounceText(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(HeadTemplateCardTypeAnnounce, on_delete=models.CASCADE, related_name="head_template_card_type_announce_text")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    text = models.CharField(max_length=255,null=True)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_card_type_announce_text'

class CompanyTemplateCardTypeAnnounceText(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(CompanyTemplateCardTypeAnnounce, on_delete=models.CASCADE, related_name="company_template_card_type_announce_text")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    text = models.CharField(max_length=255,null=True)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_card_type_announce_text'

class ShopTemplateCardTypeAnnounceText(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(ShopTemplateCardTypeAnnounce, on_delete=models.CASCADE, related_name="shop_template_card_type_announce_text")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    text = models.CharField(max_length=255,null=True)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_card_type_announce_text'

class HeadTemplateCardTypeAnnounceAction(models.Model):
    type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )
    button_type_choice = (
        (1, 'action'),
        (2, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(HeadTemplateCardTypeAnnounce, on_delete=models.CASCADE, related_name="head_template_card_type_announce_action")
    number = models.CharField(max_length=1,null=True)
    label = models.CharField(max_length=255,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_announce_action")
    question = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_announce_action")
    text = models.CharField(max_length=255,null=True)
    button_type = models.IntegerField(choices=button_type_choice, default=0)
    button_color = models.IntegerField(default=0)
    button_background_color = models.IntegerField(default=0)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_card_type_announce_action'

class CompanyTemplateCardTypeAnnounceAction(models.Model):
    type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )
    button_type_choice = (
        (1, 'action'),
        (2, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(CompanyTemplateCardTypeAnnounce, on_delete=models.CASCADE, related_name="company_template_card_type_announce_action")
    number = models.CharField(max_length=1,null=True)
    label = models.CharField(max_length=255,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_announce_action")
    question = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_announce_action")
    text = models.CharField(max_length=255,null=True)
    button_type = models.IntegerField(choices=button_type_choice, default=0)
    button_color = models.IntegerField(default=0)
    button_background_color = models.IntegerField(default=0)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_card_type_announce_action'

class ShopTemplateCardTypeAnnounceAction(models.Model):
    type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )
    button_type_choice = (
        (1, 'action'),
        (2, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(ShopTemplateCardTypeAnnounce, on_delete=models.CASCADE, related_name="shop_template_card_type_announce_action")
    number = models.CharField(max_length=1,null=True)
    label = models.CharField(max_length=255,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_announce_action")
    question = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_announce_action")
    text = models.CharField(max_length=255,null=True)
    button_type = models.IntegerField(choices=button_type_choice, default=0)
    button_color = models.IntegerField(default=0)
    button_background_color = models.IntegerField(default=0)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_card_type_announce_action'

class HeadTemplateCardTypeLocation(models.Model):
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )
    plus_type_choice = (
        (1, 'time'),
        (2, 'price'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, related_name="head_template_card_type_location")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    image_count = models.CharField(max_length=1,null=True)
    image_1 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    place = models.CharField(max_length=255,null=True)
    place_flg = models.BooleanField(default=False)
    plus = models.CharField(max_length=255,null=True)
    plus_type = models.IntegerField(choices=action_type_choice, default=0)
    plus_flg = models.BooleanField(default=False)
    action_label_1 = models.CharField(max_length=255,null=True)
    action_type_1 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_1 = models.CharField(max_length=255,null=True)
    action_video_1 = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_location_1")
    action_question_1 = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_location_1")
    action_text_1 = models.CharField(max_length=255,null=True)
    action_flg_1 = models.BooleanField(default=False)
    action_label_2 = models.CharField(max_length=255,null=True)
    action_type_2 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_2 = models.CharField(max_length=255,null=True)
    action_video_2 = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_location_2")
    action_question_2 = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_location_2")
    action_text_2 = models.CharField(max_length=255,null=True)
    action_flg_2 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_card_type_location'

class CompanyTemplateCardTypeLocation(models.Model):
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )
    plus_type_choice = (
        (1, 'time'),
        (2, 'price'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, related_name="company_template_card_type_location")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    image_count = models.CharField(max_length=1,null=True)
    image_1 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    place = models.CharField(max_length=255,null=True)
    place_flg = models.BooleanField(default=False)
    plus = models.CharField(max_length=255,null=True)
    plus_type = models.IntegerField(choices=action_type_choice, default=0)
    plus_flg = models.BooleanField(default=False)
    action_label_1 = models.CharField(max_length=255,null=True)
    action_type_1 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_1 = models.CharField(max_length=255,null=True)
    action_video_1 = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_location_1")
    action_question_1 = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_location_1")
    action_text_1 = models.CharField(max_length=255,null=True)
    action_flg_1 = models.BooleanField(default=False)
    action_label_2 = models.CharField(max_length=255,null=True)
    action_type_2 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_2 = models.CharField(max_length=255,null=True)
    action_video_2 = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_location_2")
    action_question_2 = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_location_2")
    action_text_2 = models.CharField(max_length=255,null=True)
    action_flg_2 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_card_type_location'

class ShopTemplateCardTypeLocation(models.Model):
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )
    plus_type_choice = (
        (1, 'time'),
        (2, 'price'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, related_name="shop_template_card_type_location")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    image_count = models.CharField(max_length=1,null=True)
    image_1 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    place = models.CharField(max_length=255,null=True)
    place_flg = models.BooleanField(default=False)
    plus = models.CharField(max_length=255,null=True)
    plus_type = models.IntegerField(choices=action_type_choice, default=0)
    plus_flg = models.BooleanField(default=False)
    action_label_1 = models.CharField(max_length=255,null=True)
    action_type_1 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_1 = models.CharField(max_length=255,null=True)
    action_video_1 = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_location_1")
    action_question_1 = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_location_1")
    action_text_1 = models.CharField(max_length=255,null=True)
    action_flg_1 = models.BooleanField(default=False)
    action_label_2 = models.CharField(max_length=255,null=True)
    action_type_2 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_2 = models.CharField(max_length=255,null=True)
    action_video_2 = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_location_2")
    action_question_2 = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_location_2")
    action_text_2 = models.CharField(max_length=255,null=True)
    action_flg_2 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_card_type_location'

class HeadTemplateCardTypePerson(models.Model):
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, related_name="head_template_card_type_person")
    number = models.CharField(max_length=1,null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    name = models.CharField(max_length=255,null=True)
    tag_1 = models.CharField(max_length=255,null=True)
    tag_color_1 = models.CharField(max_length=1,null=True)
    tag_flg_1 = models.BooleanField(default=False)
    tag_2 = models.CharField(max_length=255,null=True)
    tag_color_2 = models.CharField(max_length=1,null=True)
    tag_flg_2 = models.BooleanField(default=False)
    tag_3 = models.CharField(max_length=255,null=True)
    tag_color_3 = models.CharField(max_length=1,null=True)
    tag_flg_3 = models.BooleanField(default=False)
    description = models.CharField(max_length=255,null=True)
    description_flg = models.BooleanField(default=False)
    action_label_1 = models.CharField(max_length=255,null=True)
    action_type_1 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_1 = models.CharField(max_length=255,null=True)
    action_video_1 = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_person_1")
    action_question_1 = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_person_1")
    action_text_1 = models.CharField(max_length=255,null=True)
    action_flg_1 = models.BooleanField(default=False)
    action_label_2 = models.CharField(max_length=255,null=True)
    action_type_2 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_2 = models.CharField(max_length=255,null=True)
    action_video_2 = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_person_2")
    action_question_2 = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_person_2")
    action_text_2 = models.CharField(max_length=255,null=True)
    action_flg_2 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_card_type_person'

class CompanyTemplateCardTypePerson(models.Model):
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, related_name="company_template_card_type_person")
    number = models.CharField(max_length=1,null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    name = models.CharField(max_length=255,null=True)
    tag_1 = models.CharField(max_length=255,null=True)
    tag_color_1 = models.CharField(max_length=1,null=True)
    tag_flg_1 = models.BooleanField(default=False)
    tag_2 = models.CharField(max_length=255,null=True)
    tag_color_2 = models.CharField(max_length=1,null=True)
    tag_flg_2 = models.BooleanField(default=False)
    tag_3 = models.CharField(max_length=255,null=True)
    tag_color_3 = models.CharField(max_length=1,null=True)
    tag_flg_3 = models.BooleanField(default=False)
    description = models.CharField(max_length=255,null=True)
    description_flg = models.BooleanField(default=False)
    action_label_1 = models.CharField(max_length=255,null=True)
    action_type_1 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_1 = models.CharField(max_length=255,null=True)
    action_video_1 = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_person_1")
    action_question_1 = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_person_1")
    action_text_1 = models.CharField(max_length=255,null=True)
    action_flg_1 = models.BooleanField(default=False)
    action_label_2 = models.CharField(max_length=255,null=True)
    action_type_2 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_2 = models.CharField(max_length=255,null=True)
    action_video_2 = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_person_2")
    action_question_2 = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_person_2")
    action_text_2 = models.CharField(max_length=255,null=True)
    action_flg_2 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_card_type_person'

class ShopTemplateCardTypePerson(models.Model):
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, related_name="shop_template_card_type_person")
    number = models.CharField(max_length=1,null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    name = models.CharField(max_length=255,null=True)
    tag_1 = models.CharField(max_length=255,null=True)
    tag_color_1 = models.CharField(max_length=1,null=True)
    tag_flg_1 = models.BooleanField(default=False)
    tag_2 = models.CharField(max_length=255,null=True)
    tag_color_2 = models.CharField(max_length=1,null=True)
    tag_flg_2 = models.BooleanField(default=False)
    tag_3 = models.CharField(max_length=255,null=True)
    tag_color_3 = models.CharField(max_length=1,null=True)
    tag_flg_3 = models.BooleanField(default=False)
    description = models.CharField(max_length=255,null=True)
    description_flg = models.BooleanField(default=False)
    action_label_1 = models.CharField(max_length=255,null=True)
    action_type_1 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_1 = models.CharField(max_length=255,null=True)
    action_video_1 = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_person_1")
    action_question_1 = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_person_1")
    action_text_1 = models.CharField(max_length=255,null=True)
    action_flg_1 = models.BooleanField(default=False)
    action_label_2 = models.CharField(max_length=255,null=True)
    action_type_2 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_2 = models.CharField(max_length=255,null=True)
    action_video_2 = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_person_2")
    action_question_2 = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_person_2")
    action_text_2 = models.CharField(max_length=255,null=True)
    action_flg_2 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_card_type_person'

class HeadTemplateCardTypeImage(models.Model):
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, related_name="head_template_card_type_image")
    number = models.CharField(max_length=1,null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    action_label = models.CharField(max_length=255,null=True)
    action_type = models.IntegerField(choices=action_type_choice, default=0)
    action_url = models.CharField(max_length=255,null=True)
    action_video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_image")
    action_question = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_image")
    action_text = models.CharField(max_length=255,null=True)
    action_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_card_type_image'

class CompanyTemplateCardTypeImage(models.Model):
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, related_name="company_template_card_type_image")
    number = models.CharField(max_length=1,null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    action_label = models.CharField(max_length=255,null=True)
    action_type = models.IntegerField(choices=action_type_choice, default=0)
    action_url = models.CharField(max_length=255,null=True)
    action_video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_image")
    action_question = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_image")
    action_text = models.CharField(max_length=255,null=True)
    action_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_card_type_image'

class ShopTemplateCardTypeImage(models.Model):
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, related_name="shop_template_card_type_image")
    number = models.CharField(max_length=1,null=True)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    action_label = models.CharField(max_length=255,null=True)
    action_type = models.IntegerField(choices=action_type_choice, default=0)
    action_url = models.CharField(max_length=255,null=True)
    action_video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_image")
    action_question = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_image")
    action_text = models.CharField(max_length=255,null=True)
    action_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_card_type_image'

class HeadTemplateCardTypeMore(models.Model):
    template_type_choice = (
        (1, 'simple'),
        (2, 'image'),
    )
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, related_name="head_template_card_type_more")
    type = models.IntegerField(choices=template_type_choice, default=0)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    action_label = models.CharField(max_length=255,null=True)
    action_type = models.IntegerField(choices=action_type_choice, default=0)
    action_url = models.CharField(max_length=255,null=True)
    action_video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_more")
    action_question = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_card_type_more")
    action_text = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_template_card_type_more'

class CompanyTemplateCardTypeMore(models.Model):
    template_type_choice = (
        (1, 'simple'),
        (2, 'image'),
    )
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, related_name="company_template_card_type_more")
    type = models.IntegerField(choices=template_type_choice, default=0)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    action_label = models.CharField(max_length=255,null=True)
    action_type = models.IntegerField(choices=action_type_choice, default=0)
    action_url = models.CharField(max_length=255,null=True)
    action_video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_more")
    action_question = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_card_type_more")
    action_text = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_template_card_type_more'

class ShopTemplateCardTypeMore(models.Model):
    template_type_choice = (
        (1, 'simple'),
        (2, 'image'),
    )
    action_type_choice = (
        (1, 'link'),
        (2, 'video'),
        (3, 'question'),
        (4, 'reserve'),
        (5, 'history'),
        (6, 'online'),
        (7, 'company'),
        (8, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    template = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, related_name="shop_template_card_type_more")
    type = models.IntegerField(choices=template_type_choice, default=0)
    image = models.ImageField(upload_to=template_image_path, blank=True, null=True)
    action_label = models.CharField(max_length=255,null=True)
    action_type = models.IntegerField(choices=action_type_choice, default=0)
    action_url = models.CharField(max_length=255,null=True)
    action_video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_more")
    action_question = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_card_type_more")
    action_text = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_card_type_more'





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
    parent = models.ForeignKey(HeadTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_text")
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
    parent = models.ForeignKey(CompanyTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text")
    name = models.CharField(max_length=255,null=True)
    favorite_flg = models.BooleanField(default=False)
    use_flg = models.BooleanField(default=False)
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
    template_text = models.ForeignKey(HeadTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_text_item_relate")
    template_video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_text_item_relate")
    template_richmessage = models.ForeignKey(HeadTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_text_item_relate")
    template_richvideo = models.ForeignKey(HeadTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_text_item_relate")
    template_cardtype = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_text_item_relate")
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
    template_text = models.ForeignKey(CompanyTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_text_item_relate")
    template_video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_text_item_relate")
    template_richmessage = models.ForeignKey(CompanyTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_text_item_relate")
    template_richvideo = models.ForeignKey(CompanyTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_text_item_relate")
    template_cardtype = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_text_item_relate")
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
    template_text = models.ForeignKey(ShopTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text_item_relate")
    template_video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text_item_relate")
    template_richmessage = models.ForeignKey(ShopTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text_item_relate")
    template_richvideo = models.ForeignKey(ShopTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text_item_relate")
    template_cardtype = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_text_item_relate")
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
    template_text = models.ForeignKey(HeadTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_greeting")
    template_video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_greeting")
    template_richmessage = models.ForeignKey(HeadTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_greeting")
    template_richvideo = models.ForeignKey(HeadTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_greeting")
    template_cardtype = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="head_template_greeting")
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
    template_text = models.ForeignKey(CompanyTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_greeting")
    template_video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_greeting")
    template_richmessage = models.ForeignKey(CompanyTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_greeting")
    template_richvideo = models.ForeignKey(CompanyTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_greeting")
    template_cardtype = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="company_template_greeting")
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
    template_text = models.ForeignKey(ShopTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_greeting")
    template_video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_greeting")
    template_richmessage = models.ForeignKey(ShopTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_greeting")
    template_richvideo = models.ForeignKey(ShopTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_greeting")
    template_cardtype = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_template_greeting")
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_template_greeting'