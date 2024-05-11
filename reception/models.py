from django.db import models
from django.utils import timezone

from reserve.models import ReserveOfflineSetting, ReserveOnlineSetting
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthUser, AuthShop

class ReceptionData(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_data")
    auto_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reception_data'

class ReceptionOfflinePlace(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    offline = models.ForeignKey(ShopOffline, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_offline_place")
    number = models.IntegerField(default=1)
    reception_date = models.DateTimeField(blank=False, null=True)
    reception_from = models.TimeField(blank=True, null=True)
    reception_to = models.TimeField(blank=True, null=True)
    reception_count = models.IntegerField(default=0)
    reception_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'reception_offline_place'

class ReceptionOnlinePlace(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    online = models.ForeignKey(ShopOnline, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_online_place")
    number = models.IntegerField(default=1)
    reception_date = models.DateTimeField(blank=False, null=True)
    reception_from = models.TimeField(blank=True, null=True)
    reception_to = models.TimeField(blank=True, null=True)
    reception_count = models.IntegerField(default=0)
    reception_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'reception_online_place'

class ReceptionOfflineManager(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    offline = models.ForeignKey(ShopOffline, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_offline_manager")
    number = models.IntegerField(default=1)
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="reception_offline_manager")
    reception_date = models.DateTimeField(blank=False, null=True)
    reception_from = models.TimeField(blank=True, null=True)
    reception_to = models.TimeField(blank=True, null=True)
    reception_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'reception_offline_manager'

class ReceptionOnlineManager(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    online = models.ForeignKey(ShopOnline, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_online_manager")
    number = models.IntegerField(default=1)
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="reception_online_manager")
    reception_date = models.DateTimeField(blank=False, null=True)
    reception_from = models.TimeField(blank=True, null=True)
    reception_to = models.TimeField(blank=True, null=True)
    reception_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'reception_online_manager'

class ReceptionOfflineManagerSetting(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    offline = models.ForeignKey(ReserveOfflineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_offline_manager_setting")
    manager = models.ForeignKey(ReceptionOfflineManager, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_offline_manager_setting")
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reception_offline_manager_setting'

class ReceptionOnlineManagerSetting(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    online = models.ForeignKey(ReserveOnlineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_online_manager_setting")
    manager = models.ForeignKey(ReceptionOnlineManager, on_delete=models.CASCADE, blank=True, null=True, related_name="reception_online_manager_setting")
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reception_online_manager_setting'