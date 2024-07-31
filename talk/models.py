from django.db import models
from django.utils import timezone

from sign.models import AuthUser
from user.models import LineUser

import os
import uuid

def talk_image_path(self, filename):
    return "uploads/talk/image/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

def talk_video_path(self, filename):
    return "uploads/talk/video/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

def talk_video_thumbnail_path(self, filename):
    return "uploads/talk/video/thumbnail/" + str(uuid.uuid4()).replace('-', '') + os.path.splitext(filename)[-1]

class TalkMessage(models.Model):
    message_type_choice = (
        (0, 'text'),
        (1, 'image'),
        (2, 'video'),
        (3, 'audio'),
        (4, 'location'),
        (5, 'rich_message'),
        (6, 'rich_video'),
        (7, 'card_type'),
        (8, 'button'),
        (9, 'sticker'),
    )
    account_type_choice = (
        (0, 'user'),
        (1, 'manager'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name="talk_message")
    line_user_id = models.CharField(max_length=255, null=False, blank=False)
    line_message_id = models.CharField(max_length=255, blank=True, null=True)
    reply_token = models.CharField(max_length=255, blank=True, null=True)
    message_type = models.IntegerField(choices=message_type_choice, default=0)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    video = models.FileField(upload_to=talk_video_path, blank=True, null=True)
    video_width = models.IntegerField(blank=True, null=True)
    video_height = models.IntegerField(blank=True, null=True)
    video_thumbnail = models.FileField(upload_to=talk_video_thumbnail_path, blank=True, null=True)
    template_id = models.CharField(max_length=255, blank=True, null=True)
    sticker_id = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.IntegerField(choices=account_type_choice, default=0)
    author = models.CharField(max_length=255,null=True)
    send_date = models.DateTimeField(blank=False, null=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message'

class TalkMessageEmoji(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    message = models.ForeignKey(TalkMessage, on_delete=models.CASCADE, related_name="talk_message_emoji")
    number = models.IntegerField(default=0)
    index = models.IntegerField(default=0)
    product_id = models.CharField(max_length=255, null=True)
    emoji_id = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message_emoji'

class TalkMessageCardType(models.Model):
    type_choice = (
        (0, 'product'),
        (1, 'location'),
        (2, 'person'),
        (3, 'image'),
        (4, 'announce'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    message = models.ForeignKey(TalkMessage, on_delete=models.CASCADE, related_name="talk_message_card_type")
    type = models.IntegerField(choices=type_choice, default=0)
    count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message_card_type'

class TalkMessageCardTypeAnnounce(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(TalkMessageCardType, on_delete=models.CASCADE, related_name="talk_message_card_type_announce")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    image_count = models.CharField(max_length=1,null=True)
    image_1 = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
    image_flg = models.BooleanField(default=False)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    description = models.CharField(max_length=255,null=True)
    description_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message_card_type_announce'

class TalkMessageCardTypeAnnounceText(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type_announce = models.ForeignKey(TalkMessageCardTypeAnnounce, on_delete=models.CASCADE, related_name="talk_message_card_type_announce_text")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    text = models.CharField(max_length=255,null=True)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message_card_type_announce_text'

class TalkMessageCardTypeAnnounceAction(models.Model):
    type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'company'),
        (5, 'text'),
        (5, 'online'),
    )
    button_type_choice = (
        (0, 'action'),
        (1, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type_announce = models.ForeignKey(TalkMessageCardTypeAnnounce, on_delete=models.CASCADE, related_name="talk_message_card_type_announce_action")
    number = models.CharField(max_length=1,null=True)
    label = models.CharField(max_length=255,null=True)
    type = models.IntegerField(choices=type_choice, default=0)
    url = models.CharField(max_length=255,null=True)
    text = models.CharField(max_length=255,null=True)
    button_type = models.IntegerField(choices=button_type_choice, default=0)
    button_color = models.IntegerField(default=0)
    button_background_color = models.IntegerField(default=0)
    flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message_card_type_announce_action'

class TalkMessageCardTypeLocation(models.Model):
    action_type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'company'),
        (5, 'text'),
    )
    plus_type_choice = (
        (0, 'none'),
        (1, 'time'),
        (2, 'price'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(TalkMessageCardType, on_delete=models.CASCADE, related_name="talk_message_card_type_product")
    number = models.CharField(max_length=1,null=True)
    title = models.CharField(max_length=255,null=True)
    image_count = models.CharField(max_length=1,null=True)
    image_1 = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
    image_2 = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
    image_3 = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
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
    action_text_1 = models.CharField(max_length=255,null=True)
    action_flg_1 = models.BooleanField(default=False)
    action_label_2 = models.CharField(max_length=255,null=True)
    action_type_2 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_2 = models.CharField(max_length=255,null=True)
    action_text_2 = models.CharField(max_length=255,null=True)
    action_flg_2 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message_card_type_location'

class TalkMessageCardTypePerson(models.Model):
    action_type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'company'),
        (5, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(TalkMessageCardType, on_delete=models.CASCADE, related_name="talk_message_card_type_person")
    number = models.CharField(max_length=1,null=True)
    image = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
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
    action_text_1 = models.CharField(max_length=255,null=True)
    action_flg_1 = models.BooleanField(default=False)
    action_label_2 = models.CharField(max_length=255,null=True)
    action_type_2 = models.IntegerField(choices=action_type_choice, default=0)
    action_url_2 = models.CharField(max_length=255,null=True)
    action_text_2 = models.CharField(max_length=255,null=True)
    action_flg_2 = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message_card_type_person'

class TalkMessageCardTypeImage(models.Model):
    action_type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'company'),
        (5, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(TalkMessageCardType, on_delete=models.CASCADE, related_name="talk_message_card_type_image")
    number = models.CharField(max_length=1,null=True)
    image = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
    label = models.CharField(max_length=255,null=True)
    label_color = models.CharField(max_length=1,null=True)
    label_flg = models.BooleanField(default=False)
    action_label = models.CharField(max_length=255,null=True)
    action_type = models.IntegerField(choices=action_type_choice, default=0)
    action_url = models.CharField(max_length=255,null=True)
    action_text = models.CharField(max_length=255,null=True)
    action_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message_card_type_image'

class TalkMessageCardTypeMore(models.Model):
    template_type_choice = (
        (0, 'none'),
        (1, 'simple'),
        (2, 'image'),
    )
    action_type_choice = (
        (0, 'none'),
        (1, 'link'),
        (2, 'video'),
        (3, 'questionform'),
        (4, 'company'),
        (5, 'text'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    card_type = models.ForeignKey(TalkMessageCardType, on_delete=models.CASCADE, related_name="talk_message_card_type_more")
    template = models.IntegerField(choices=template_type_choice, default=0)
    image = models.ImageField(upload_to=talk_image_path, blank=True, null=True)
    action_label = models.CharField(max_length=255,null=True)
    action_type = models.IntegerField(choices=action_type_choice, default=0)
    action_url = models.CharField(max_length=255,null=True)
    action_text = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_message_card_type_more'



class TalkManager(models.Model):

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    user = models.OneToOneField(LineUser, on_delete=models.CASCADE, related_name="talk_manager")
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="talk_manager")
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'talk_manager'

class TalkStatus(models.Model):
    status_choice = (
        (0, '対応なし'),
        (1, '要対応'),
        (2, '対応済み'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    user = models.OneToOneField(LineUser, on_delete=models.CASCADE, related_name="talk_status")
    status = models.IntegerField(choices=status_choice, default=0)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_status'

class TalkPin(models.Model):

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name="talk_pin")
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="talk_pin")
    pin_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_pin'

class TalkRead(models.Model):

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    user = models.ForeignKey(LineUser, on_delete=models.CASCADE, related_name="talk_read")
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="talk_read")
    read_count = models.IntegerField(default=0)
    read_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_read'

class TalkUpdate(models.Model):

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    manager = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="talk_update")
    update_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'talk_update'