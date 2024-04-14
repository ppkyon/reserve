from django.db import models
from django.utils import timezone

from question.models import ShopQuestion
from reserve.models import (
    ReserveOnlineSetting, ReserveOfflineSetting, ReserveOnlineMeeting, ReserveOfflineCourse, ReserveOnlineCourse, ReserveOfflineFacility, ReserveOnlineFacility
)
from richmenu.models import HeadRichMenu, CompanyRichMenu, ShopRichMenu
from sign.models import AuthUser, AuthCompany, AuthShop
from template.models import (
    HeadTemplateText, HeadTemplateVideo, HeadTemplateRichMessage, HeadTemplateRichVideo, HeadTemplateCardType,
    CompanyTemplateText, CompanyTemplateVideo, CompanyTemplateRichMessage, CompanyTemplateRichVideo, CompanyTemplateCardType,
    ShopTemplateText, ShopTemplateVideo, ShopTemplateRichMessage, ShopTemplateRichVideo, ShopTemplateCardType
)
from user.models import LineUser

class HeadFlow(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    name = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    valid = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow'

class CompanyFlow(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    parent = models.ForeignKey(HeadFlow, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow")
    name = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    valid = models.BooleanField(default=False)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow'

class ShopFlow(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    parent = models.ForeignKey(CompanyFlow, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow")
    name = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    period_from = models.DateTimeField(blank=True, null=True)
    period_to = models.DateTimeField(blank=True, null=True)
    favorite_flg = models.BooleanField(default=False)
    delete_flg = models.BooleanField(default=False)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow'

class HeadFlowTab(models.Model):
    member_choice = (
        (0, 'no'),
        (1, 'yes'),
        (2, 'any'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlow, on_delete=models.CASCADE, null=True, related_name="head_flow_tab")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    value = models.CharField(max_length=255,null=True)
    member = models.IntegerField(choices=member_choice, default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_tab'

class CompanyFlowTab(models.Model):
    member_choice = (
        (0, 'no'),
        (1, 'yes'),
        (2, 'any'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlow, on_delete=models.CASCADE, null=True, related_name="company_flow_tab")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    value = models.CharField(max_length=255,null=True)
    member = models.IntegerField(choices=member_choice, default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_tab'

class ShopFlowTab(models.Model):
    member_choice = (
        (0, 'no'),
        (1, 'yes'),
        (2, 'any'),
    )
    
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlow, on_delete=models.CASCADE, null=True, related_name="shop_flow_tab")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    value = models.CharField(max_length=255,null=True)
    member = models.IntegerField(choices=member_choice, default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_tab'

class HeadFlowItem(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'template_greeting'),
        (2, 'template_message'),
        (3, 'template_video'), 
        (4, 'template_rich_message'),
        (5, 'template_rich_video'),
        (6, 'template_card_type'),
        (7, 'rich_menu'),
        (8, 'action'),
        (9, 'step'),
        (10, 'wait'),
        (11, 'end'),
        (51, 'manual'),
        (52, 'timer'),
        (53, 'condition'),
        (54, 'schedule'),
        (55, 'result'),
    )
    
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow_tab = models.ForeignKey(HeadFlowTab, on_delete=models.CASCADE, related_name="head_flow_item")
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    type = models.IntegerField(choices=type_choice, default=0)
    name = models.CharField(max_length=255,null=True)
    analytics = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_item'

class CompanyFlowItem(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'template_greeting'),
        (2, 'template_message'),
        (3, 'template_video'), 
        (4, 'template_rich_message'),
        (5, 'template_rich_video'),
        (6, 'template_card_type'),
        (7, 'rich_menu'),
        (8, 'action'),
        (9, 'step'),
        (10, 'wait'),
        (11, 'end'),
        (51, 'manual'),
        (52, 'timer'),
        (53, 'condition'),
        (54, 'schedule'),
        (55, 'result'),
    )
    
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow_tab = models.ForeignKey(CompanyFlowTab, on_delete=models.CASCADE, related_name="company_flow_item")
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    type = models.IntegerField(choices=type_choice, default=0)
    name = models.CharField(max_length=255,null=True)
    analytics = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_item'

class ShopFlowItem(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'template_greeting'),
        (2, 'template_message'),
        (3, 'template_video'), 
        (4, 'template_rich_message'),
        (5, 'template_rich_video'),
        (6, 'template_card_type'),
        (7, 'rich_menu'),
        (8, 'action'),
        (9, 'step'),
        (10, 'wait'),
        (11, 'end'),
        (51, 'manual'),
        (52, 'timer'),
        (53, 'condition'),
        (54, 'schedule'),
        (55, 'result'),
    )
    
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow_tab = models.ForeignKey(ShopFlowTab, on_delete=models.CASCADE, related_name="shop_flow_item")
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    number = models.IntegerField(default=0)
    type = models.IntegerField(choices=type_choice, default=0)
    name = models.CharField(max_length=255,null=True)
    analytics = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_item'



class HeadFlowTemplate(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_template")
    template_text = models.ForeignKey(HeadTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_template")
    template_video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_template")
    template_richmessage = models.ForeignKey(HeadTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_template")
    template_richvideo = models.ForeignKey(HeadTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_template")
    template_cardtype = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_template")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_template'

class CompanyFlowTemplate(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_template")
    template_text = models.ForeignKey(CompanyTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template")
    template_video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template")
    template_richmessage = models.ForeignKey(CompanyTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template")
    template_richvideo = models.ForeignKey(CompanyTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template")
    template_cardtype = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_template'

class ShopFlowTemplate(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_template")
    template_text = models.ForeignKey(ShopTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template")
    template_video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template")
    template_richmessage = models.ForeignKey(ShopTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template")
    template_richvideo = models.ForeignKey(ShopTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template")
    template_cardtype = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_template'

class HeadFlowRichMenu(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_rich_menu")
    rich_menu = models.ForeignKey(HeadRichMenu, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_rich_menu")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_rich_menu'

class CompanyFlowRichMenu(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_rich_menu")
    rich_menu = models.ForeignKey(CompanyRichMenu, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_rich_menu")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_rich_menu'

class ShopFlowRichMenu(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_rich_menu")
    rich_menu = models.ForeignKey(ShopRichMenu, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_rich_menu")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_rich_menu'

class HeadFlowAction(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_action")
    action = models.ForeignKey(HeadFlowTab, on_delete=models.CASCADE, related_name="head_flow_action")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_action'

class CompanyFlowAction(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_action")
    action = models.ForeignKey(CompanyFlowTab, on_delete=models.CASCADE, related_name="company_flow_action")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_action'

class ShopFlowAction(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_action")
    action = models.ForeignKey(ShopFlowTab, on_delete=models.CASCADE, related_name="shop_flow_action")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_action'

class HeadFlowStep(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_step")
    tab = models.ForeignKey(HeadFlowTab, on_delete=models.CASCADE, related_name="head_flow_step")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_step'

class CompanyFlowStep(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_step")
    tab = models.ForeignKey(CompanyFlowTab, on_delete=models.CASCADE, related_name="company_flow_step")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_step'

class ShopFlowStep(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_step")
    tab = models.ForeignKey(ShopFlowTab, on_delete=models.CASCADE, related_name="shop_flow_step")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_step'

class HeadFlowTemplateReminder(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_template_reminder")
    template_text = models.ForeignKey(HeadTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_template_reminder")
    template_video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_template_reminder")
    template_richmessage = models.ForeignKey(HeadTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_template_reminder")
    template_richvideo = models.ForeignKey(HeadTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_template_reminder")
    template_cardtype = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_templaet_reminder")
    date = models.IntegerField(default=0)
    repeat_flg = models.BooleanField(default=False)
    repeat_date = models.IntegerField(default=0)
    repeat_count_flg = models.BooleanField(default=False)
    repeat_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_template_reminder'

class CompanyFlowTemplateReminder(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_template_reminder")
    template_text = models.ForeignKey(CompanyTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template_reminder")
    template_video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template_reminder")
    template_richmessage = models.ForeignKey(CompanyTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template_reminder")
    template_richvideo = models.ForeignKey(CompanyTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template_reminder")
    template_cardtype = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_template_reminder")
    date = models.IntegerField(default=0)
    repeat_flg = models.BooleanField(default=False)
    repeat_date = models.IntegerField(default=0)
    repeat_count_flg = models.BooleanField(default=False)
    repeat_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_template_reminder'

class ShopFlowTemplateReminder(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_template_reminder")
    template_text = models.ForeignKey(ShopTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template_reminder")
    template_video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template_reminder")
    template_richmessage = models.ForeignKey(ShopTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template_reminder")
    template_richvideo = models.ForeignKey(ShopTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template_reminder")
    template_cardtype = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_template_reminder")
    date = models.IntegerField(default=0)
    repeat_flg = models.BooleanField(default=False)
    repeat_date = models.IntegerField(default=0)
    repeat_count_flg = models.BooleanField(default=False)
    repeat_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_template_reminder'

class HeadFlowActionReminder(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_action_reminder")
    template_text = models.ForeignKey(HeadTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_reminder")
    template_video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_reminder")
    template_richmessage = models.ForeignKey(HeadTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_reminder")
    template_richvideo = models.ForeignKey(HeadTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_reminder")
    template_cardtype = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_reminder")
    date = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_action_reminder'

class CompanyFlowActionReminder(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_action_reminder")
    template_text = models.ForeignKey(CompanyTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_reminder")
    template_video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_reminder")
    template_richmessage = models.ForeignKey(CompanyTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_reminder")
    template_richvideo = models.ForeignKey(CompanyTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_reminder")
    template_cardtype = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_reminder")
    date = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_action_reminder'

class ShopFlowActionReminder(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_action_reminder")
    template_text = models.ForeignKey(ShopTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_reminder")
    template_video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_reminder")
    template_richmessage = models.ForeignKey(ShopTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_reminder")
    template_richvideo = models.ForeignKey(ShopTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_reminder")
    template_cardtype = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_reminder")
    date = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_action_reminder'

class HeadFlowActionMessage(models.Model):
    type_choice = (
        (0, '即時'),
        (1, '日時'),
        (2, '経過時間'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_action_message")
    template_text = models.ForeignKey(HeadTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_message")
    template_video = models.ForeignKey(HeadTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_message")
    template_richmessage = models.ForeignKey(HeadTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_message")
    template_richvideo = models.ForeignKey(HeadTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_message")
    template_cardtype = models.ForeignKey(HeadTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="head_flow_action_message")
    type = models.IntegerField(choices=type_choice, default=0)
    date = models.IntegerField(default=0)
    time = models.TimeField(blank=False, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_action_message'

class CompanyFlowActionMessage(models.Model):
    type_choice = (
        (0, '即時'),
        (1, '日時'),
        (2, '経過時間'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_action_message")
    template_text = models.ForeignKey(CompanyTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_message")
    template_video = models.ForeignKey(CompanyTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_message")
    template_richmessage = models.ForeignKey(CompanyTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_message")
    template_richvideo = models.ForeignKey(CompanyTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_message")
    template_cardtype = models.ForeignKey(CompanyTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="company_flow_action_message")
    type = models.IntegerField(choices=type_choice, default=0)
    date = models.IntegerField(default=0)
    time = models.TimeField(blank=False, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_action_message'

class ShopFlowActionMessage(models.Model):
    type_choice = (
        (0, '即時'),
        (1, '日時'),
        (2, '経過時間'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_action_message")
    template_text = models.ForeignKey(ShopTemplateText, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_message")
    template_video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_message")
    template_richmessage = models.ForeignKey(ShopTemplateRichMessage, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_message")
    template_richvideo = models.ForeignKey(ShopTemplateRichVideo, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_message")
    template_cardtype = models.ForeignKey(ShopTemplateCardType, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_flow_action_message")
    type = models.IntegerField(choices=type_choice, default=0)
    date = models.IntegerField(default=0)
    time = models.TimeField(blank=False, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_action_message'



class HeadFlowTimer(models.Model):
    type_choice = (
        (0, '即時'),
        (1, '日時'),
        (2, '経過時間'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_timer")
    type = models.IntegerField(choices=type_choice, default=0)
    date = models.IntegerField(default=0)
    time = models.TimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_timer'

class CompanyFlowTimer(models.Model):
    type_choice = (
        (0, '即時'),
        (1, '日時'),
        (2, '経過時間'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_timer")
    type = models.IntegerField(choices=type_choice, default=0)
    date = models.IntegerField(default=0)
    time = models.TimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_timer'

class ShopFlowTimer(models.Model):
    type_choice = (
        (0, '即時'),
        (1, '日時'),
        (2, '経過時間'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_timer")
    type = models.IntegerField(choices=type_choice, default=0)
    date = models.IntegerField(default=0)
    time = models.TimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_timer'

class HeadFlowCondition(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_condition")
    number = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_condition'

class CompanyFlowCondition(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_condition")
    number = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_condition'

class ShopFlowCondition(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_condition")
    number = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_condition'
        
class HeadFlowConditionItem(models.Model):
    type_choice = (
        (1, '提出'),
        (2, '年齢'),
        (3, '性別'),
        (4, '条件'),
        (5, '形式'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    condition = models.ForeignKey(HeadFlowCondition, on_delete=models.CASCADE, related_name="head_flow_condition_item")
    number = models.IntegerField(default=0)
    type = models.IntegerField(choices=type_choice, default=0)
    text1 = models.IntegerField(default=0)
    text2 = models.IntegerField(default=0)
    radio = models.IntegerField(default=0)
    check1 = models.BooleanField(default=False)
    check2 = models.BooleanField(default=False)
    check3 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_condition_item'
        
class CompanyFlowConditionItem(models.Model):
    type_choice = (
        (1, '提出'),
        (2, '年齢'),
        (3, '性別'),
        (4, '条件'),
        (5, '形式'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    condition = models.ForeignKey(CompanyFlowCondition, on_delete=models.CASCADE, related_name="company_flow_condition_item")
    number = models.IntegerField(default=0)
    type = models.IntegerField(choices=type_choice, default=0)
    text1 = models.IntegerField(default=0)
    text2 = models.IntegerField(default=0)
    radio = models.IntegerField(default=0)
    check1 = models.BooleanField(default=False)
    check2 = models.BooleanField(default=False)
    check3 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_condition_item'
        
class ShopFlowConditionItem(models.Model):
    type_choice = (
        (1, '提出'),
        (2, '年齢'),
        (3, '性別'),
        (4, '条件'),
        (5, '形式'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    condition = models.ForeignKey(ShopFlowCondition, on_delete=models.CASCADE, related_name="shop_flow_condition_item")
    number = models.IntegerField(default=0)
    type = models.IntegerField(choices=type_choice, default=0)
    text1 = models.IntegerField(default=0)
    text2 = models.IntegerField(default=0)
    radio = models.IntegerField(default=0)
    check1 = models.BooleanField(default=False)
    check2 = models.BooleanField(default=False)
    check3 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_condition_item'

class HeadFlowSchedule(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_schedule")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_schedule'

class CompanyFlowSchedule(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_schedule")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_schedule'

class ShopFlowSchedule(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_schedule")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_schedule'

class HeadFlowResult(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(HeadFlowItem, on_delete=models.CASCADE, related_name="head_flow_result")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_flow_result'

class CompanyFlowResult(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(CompanyFlowItem, on_delete=models.CASCADE, related_name="company_flow_result")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_flow_result'

class ShopFlowResult(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    flow = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, related_name="shop_flow_result")
    number = models.IntegerField(default=0)
    name = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_flow_result'



class UserFlow(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name="user_flow")
    number = models.IntegerField(default=0)
    flow = models.ForeignKey(ShopFlow, on_delete=models.CASCADE, related_name="user_flow")
    flow_tab = models.ForeignKey(ShopFlowTab, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow")
    flow_item = models.ForeignKey(ShopFlowItem, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow")
    name = models.CharField(max_length=255,null=True)
    image = models.ForeignKey(ShopTemplateRichMessage, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    video = models.ForeignKey(ShopTemplateVideo, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    richmenu = models.ForeignKey(ShopRichMenu, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    end_flg = models.BooleanField(default=False)
    checked_at = models.DateTimeField(blank=False, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_flow'

class UserFlowSchedule(models.Model):
    join_choice = (
        (0, '未定'),
        (1, '参加'),
        (2, '不参加'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    flow = models.ForeignKey(UserFlow, on_delete=models.CASCADE, blank=True, null=True, related_name="user_flow_schedule")
    number = models.IntegerField(default=0)
    date = models.DateTimeField(blank=False, null=True)
    time = models.TimeField(blank=False, null=True)
    join = models.IntegerField(choices=join_choice, default=0)
    online = models.ForeignKey(ReserveOnlineSetting, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    offline = models.ForeignKey(ReserveOfflineSetting, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    online_course = models.ForeignKey(ReserveOnlineCourse, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    offline_course = models.ForeignKey(ReserveOfflineCourse, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    online_facility = models.ForeignKey(ReserveOnlineFacility, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    offline_facility = models.ForeignKey(ReserveOfflineFacility, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    question = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    meeting = models.ForeignKey(ReserveOnlineMeeting, on_delete=models.CASCADE, blank=False, null=True, related_name="user_flow_history")
    memo = models.TextField(max_length=1000, blank=True, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_flow_schedule'

class UserFlowTimer(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name="user_flow_timer")
    action_date = models.DateTimeField(blank=False, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'user_flow_timer'