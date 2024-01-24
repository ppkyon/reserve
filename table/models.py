from django.db import models
from django.utils import timezone

from sign.models import AuthCompany, AuthShop, AuthUser

class TableSearch(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    url = models.CharField(max_length=255, null=False, blank=False)
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="table_search")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="table_search")
    manager = models.ForeignKey(AuthUser, on_delete=models.PROTECT, related_name="table_search")
    text = models.CharField(max_length=255, null=False, blank=False)
    item = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'table_search'

class TableNumber(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    url = models.CharField(max_length=255, null=False, blank=False)
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="table_number")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="table_number")
    manager = models.ForeignKey(AuthUser, on_delete=models.PROTECT, related_name="table_number")
    number = models.IntegerField(null=False, blank=False, default=0)
    item = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'table_number'

class TableSort(models.Model):
    sort_choice = (
        (0, 'なし'),
        (1, 'asc'),
        (2, 'desc'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    url = models.CharField(max_length=255, null=False, blank=False)
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="table_sort")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="table_sort")
    manager = models.ForeignKey(AuthUser, on_delete=models.PROTECT, related_name="table_sort")
    target = models.CharField(max_length=255, null=False, blank=False)
    sort = models.IntegerField(choices=sort_choice, default=0)
    item = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'table_sort'