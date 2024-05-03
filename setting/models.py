from django.db import models
from django.utils import timezone

from sign.models import AuthUser, AuthShop

class ShopOffline(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_offline")
    title = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255,null=True)
    note = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'shop_offline'

class ShopOnline(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_online")
    title = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    outline = models.CharField(max_length=255,null=True)
    note = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'shop_online'

class ShopOfflineTime(models.Model):
    week_choice = (
        (1, '月'),
        (2, '火'),
        (3, '水'),
        (4, '木'),
        (5, '金'),
        (6, '土'),
        (7, '日'),
        (8, '祝'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    offline = models.ForeignKey(ShopOffline, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_offline_time")
    week = models.IntegerField(choices=week_choice, default=0)
    number = models.IntegerField(default=1)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'shop_offline_time'

class ShopOnlineTime(models.Model):
    week_choice = (
        (1, '月'),
        (2, '火'),
        (3, '水'),
        (4, '木'),
        (5, '金'),
        (6, '土'),
        (7, '日'),
        (8, '祝'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    online = models.ForeignKey(ShopOnline, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_online_time")
    week = models.IntegerField(choices=week_choice, default=0)
    number = models.IntegerField(default=1)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'shop_online_time'



class ManagerOffline(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="manager_offline")
    offline = models.ForeignKey(ShopOffline, on_delete=models.CASCADE, blank=True, null=True, related_name="manager_offline")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'manager_offline'

class ManagerOnline(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="manager_online")
    online = models.ForeignKey(ShopOnline, on_delete=models.CASCADE, blank=True, null=True, related_name="manager_online")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'manager_online'

class ManagerOfflineTime(models.Model):
    week_choice = (
        (1, '月'),
        (2, '火'),
        (3, '水'),
        (4, '木'),
        (5, '金'),
        (6, '土'),
        (7, '日'),
        (8, '祝'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    offline = models.ForeignKey(ManagerOffline, on_delete=models.CASCADE, blank=True, null=True, related_name="manager_offline_time")
    week = models.IntegerField(choices=week_choice, default=0)
    number = models.IntegerField(default=1)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    holiday_flg = models.BooleanField(default=False)
    calendar_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'manager_offline_time'

class ManagerOnlineTime(models.Model):
    week_choice = (
        (1, '月'),
        (2, '火'),
        (3, '水'),
        (4, '木'),
        (5, '金'),
        (6, '土'),
        (7, '日'),
        (8, '祝'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    online = models.ForeignKey(ManagerOnline, on_delete=models.CASCADE, blank=True, null=True, related_name="manager_online_time")
    week = models.IntegerField(choices=week_choice, default=0)
    number = models.IntegerField(default=1)
    time_from = models.TimeField(blank=True, null=True)
    time_to = models.TimeField(blank=True, null=True)
    holiday_flg = models.BooleanField(default=False)
    calendar_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'manager_online_time'



class SettingAlert(models.Model):
    status_choice = (
        (1, 'info'),
        (2, 'notice'),
        (3, 'error'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="setting_alert")
    text = models.TextField(max_length=1000, blank=True, null=True)
    status = models.IntegerField(choices=status_choice, default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'setting_alert'