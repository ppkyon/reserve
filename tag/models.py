from django.db import models
from django.utils import timezone

from sign.models import AuthCompany, AuthShop

class HeadTagGenre(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    name = models.CharField(max_length=255,null=True)
    count = models.IntegerField(blank=True, null=True)
    favorite_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_tag_genre'

class HeadTag(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    genre = models.ForeignKey(HeadTagGenre, on_delete=models.CASCADE, related_name="head_tag")
    name = models.CharField(max_length=255,null=True)
    favorite_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_tag'



class CompanyTagGenre(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="tag_genre")
    name = models.CharField(max_length=255,null=True)
    count = models.IntegerField(blank=True, null=True)
    favorite_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_tag_genre'

class CompanyTag(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    genre = models.ForeignKey(HeadTagGenre, on_delete=models.CASCADE, related_name="company_tag")
    name = models.CharField(max_length=255,null=True)
    favorite_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_tag'



class TagGenre(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="tag_genre")
    name = models.CharField(max_length=255,null=True)
    count = models.IntegerField(blank=True, null=True)
    favorite_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'tag_genre'

class Tag(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    genre = models.ForeignKey(TagGenre, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True)
    favorite_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'tag'
