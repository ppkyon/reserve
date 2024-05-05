from django.db import models
from django.utils import timezone

from question.models import ShopQuestion
from setting.models import ShopOffline, ShopOnline
from sign.models import AuthUser, AuthShop

class ReserveBasic(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_basic")
    start = models.IntegerField(default=0)
    deadline = models.IntegerField(default=0)
    on_time = models.IntegerField(default=0)
    any_day = models.IntegerField(default=0)
    any_time = models.IntegerField(default=0)
    method = models.IntegerField(default=0)
    unit = models.IntegerField(default=0)
    business_mon_day = models.BooleanField(default=False)
    business_tue_day = models.BooleanField(default=False)
    business_wed_day = models.BooleanField(default=False)
    business_thu_day = models.BooleanField(default=False)
    business_fri_day = models.BooleanField(default=False)
    business_sat_day = models.BooleanField(default=False)
    business_sun_day = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_basic'

class ReserveOfflinePlace(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_place")
    name = models.CharField(max_length=255, null=True)
    outline = models.TextField(max_length=1000, blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_offline_place'

class ReserveOnlinePlace(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_place")
    name = models.CharField(max_length=255, null=True)
    outline = models.TextField(max_length=1000, blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_online_place'

class ReserveOfflineCourse(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_course")
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=255, null=True)
    outline = models.TextField(max_length=1000, blank=True, null=True)
    start = models.IntegerField(default=0)
    deadline = models.IntegerField(default=0)
    on_time = models.IntegerField(default=0)
    any_day = models.IntegerField(default=0)
    any_time = models.IntegerField(default=0)
    method = models.IntegerField(default=0)
    business_mon_day = models.BooleanField(default=False)
    business_tue_day = models.BooleanField(default=False)
    business_wed_day = models.BooleanField(default=False)
    business_thu_day = models.BooleanField(default=False)
    business_fri_day = models.BooleanField(default=False)
    business_sat_day = models.BooleanField(default=False)
    business_sun_day = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_offline_course'

class ReserveOnlineCourse(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_course")
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=255, null=True)
    outline = models.TextField(max_length=1000, blank=True, null=True)
    start = models.IntegerField(default=0)
    deadline = models.IntegerField(default=0)
    on_time = models.IntegerField(default=0)
    any_day = models.IntegerField(default=0)
    any_time = models.IntegerField(default=0)
    method = models.IntegerField(default=0)
    business_mon_day = models.BooleanField(default=False)
    business_tue_day = models.BooleanField(default=False)
    business_wed_day = models.BooleanField(default=False)
    business_thu_day = models.BooleanField(default=False)
    business_fri_day = models.BooleanField(default=False)
    business_sat_day = models.BooleanField(default=False)
    business_sun_day = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_online_course'

class ReserveOfflineSetting(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    offline = models.ForeignKey(ShopOffline, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_setting")
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    outline = models.TextField(max_length=1000, blank=True, null=True)
    note = models.CharField(max_length=255, null=True)
    time = models.IntegerField(default=0)
    people = models.IntegerField(default=0)
    facility = models.IntegerField(default=0)
    question = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_setting")
    advance = models.CharField(max_length=255, null=True)
    course_flg = models.BooleanField(default=False)
    display_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_offline_setting'

class ReserveOnlineSetting(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    online = models.ForeignKey(ShopOnline, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_setting")
    number = models.IntegerField(default=0)
    title = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    outline = models.TextField(max_length=1000, blank=True, null=True)
    note = models.CharField(max_length=255, null=True)
    time = models.IntegerField(default=0)
    people = models.IntegerField(default=0)
    facility = models.IntegerField(default=0)
    question = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_setting")
    advance = models.CharField(max_length=255, null=True)
    course_flg = models.BooleanField(default=False)
    display_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_online_setting'

class ReserveOnlineMeeting(models.Model):
    platform_choice = (
        (1, 'LINEミーティング'),
        (2, 'Zoom'),
        (9, 'その他'),
    )
    status_choice = (
        (0, '使用可能'),
        (1, '期限切れ'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    online = models.ForeignKey(ReserveOnlineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_meeting")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True)
    url = models.URLField(max_length=255, null=False, blank=False)
    platform = models.IntegerField(choices=platform_choice, default=0)
    platform_text = models.CharField(max_length=255, null=True)
    start_date =  models.DateTimeField(blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=status_choice, default=0)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_online_meeting'

class ReserveOfflineFacility(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    offline = models.ForeignKey(ShopOffline, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_facility")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True)
    count = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_offline_facility'

class ReserveOnlineFacility(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    online = models.ForeignKey(ShopOnline, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_facility")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True)
    count = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_online_facility'

class ReserveOfflineManagerMenu(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_manager_menu")
    offline = models.ForeignKey(ReserveOfflineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_manager_menu")
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="reserve_offline_manager_menu")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_offline_manager_menu'

class ReserveOnlineManagerMenu(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_manager_menu")
    online = models.ForeignKey(ReserveOnlineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_manager_menu")
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="reserve_online_manager_menu")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_online_manager_menu'

class ReserveOfflineFacilityMenu(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_facility_menu")
    offline = models.ForeignKey(ReserveOfflineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_facility_menu")
    facility = models.ForeignKey(ReserveOfflineFacility, on_delete=models.CASCADE, related_name="reserve_offline_facility_menu")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_offline_facility_menu'

class ReserveOnlineFacilityMenu(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_facility_menu")
    online = models.ForeignKey(ReserveOnlineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_facility_menu")
    facility = models.ForeignKey(ReserveOfflineFacility, on_delete=models.CASCADE, related_name="reserve_online_facility_menu")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_online_facility_menu'

class ReserveOfflineFlowMenu(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_flow_menu")
    offline = models.ForeignKey(ReserveOfflineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_offline_flow_menu")
    flow = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_offline_flow_menu'

class ReserveOnlineFlowMenu(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_flow_menu")
    online = models.ForeignKey(ReserveOnlineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_online_flow_menu")
    flow = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_online_flow_menu'



class ReserveStartDate(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_start_date")
    offline = models.ForeignKey(ReserveOfflineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_start_date")
    online = models.ForeignKey(ReserveOnlineSetting, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_start_date")
    offline_course = models.ForeignKey(ReserveOfflineCourse, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_start_date")
    online_course = models.ForeignKey(ReserveOnlineCourse, on_delete=models.CASCADE, blank=True, null=True, related_name="reserve_start_date")
    first_date = models.DateTimeField(blank=False, null=True)
    second_date = models.DateTimeField(blank=False, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'reserve_start_date'