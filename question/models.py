from django.db import models
from django.utils import timezone

from sign.models import AuthCompany, AuthShop

class HeadQuestion(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    title = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    color = models.CharField(max_length=1,null=True)
    count = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_question'

class HeadQuestionItem(models.Model):
    type_choice = (
        (1, '氏名'),
        (2, 'フリガナ'),
        (3, '年齢'),
        (4, '性別'),
        (5, '電話番号'),
        (6, 'メールアドレス'),
        (7, '生年月日'),
        (8, '住所'),
        (9, 'プロフィール写真'),
        (10, '画像'),
        (11, '動画'),
        (51, '予約形式'),
        (52, '予約日程'),
        (53, '予約可能日'),
        (54, '予約日程再調整'),
        (99, '設問'),
    )
    choice_type_choice = (
        (1, 'フリーテキスト'),
        (2, 'ラジオボタン'),
        (3, 'チェックボックス'),
        (4, 'プルダウン'),
        (5, '日付'),
        (6, '時間'),
        (7, '日時'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    question = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, related_name="head_question_item")
    number = models.IntegerField(default=0)
    type = models.IntegerField(choices=type_choice, default=0)
    title = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    choice_type = models.IntegerField(choices=choice_type_choice, default=0)
    choice_count = models.IntegerField(blank=True, null=True)
    required_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'head_question_item'

class HeadQuestionItemChoice(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    question_item = models.ForeignKey(HeadQuestionItem, on_delete=models.CASCADE, related_name="head_question_item_choice")
    number = models.IntegerField(default=0)
    text = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'head_question_item_choice'



class CompanyQuestion(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    head = models.ForeignKey(HeadQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="company_question")
    company = models.ForeignKey(AuthCompany, on_delete=models.CASCADE, blank=True, null=True, related_name="company_question")
    title = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    color = models.CharField(max_length=1,null=True)
    count = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_question'

class CompanyQuestionItem(models.Model):
    type_choice = (
        (1, '氏名'),
        (2, 'フリガナ'),
        (3, '年齢'),
        (4, '性別'),
        (5, '電話番号'),
        (6, 'メールアドレス'),
        (7, '生年月日'),
        (8, '住所'),
        (9, 'プロフィール写真'),
        (10, '画像'),
        (11, '動画'),
        (51, '予約形式'),
        (52, '予約日程'),
        (53, '予約可能日'),
        (54, '予約日程再調整'),
        (99, '設問'),
    )
    choice_type_choice = (
        (1, 'フリーテキスト'),
        (2, 'ラジオボタン'),
        (3, 'チェックボックス'),
        (4, 'プルダウン'),
        (5, '日付'),
        (6, '時間'),
        (7, '日時'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    question = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, related_name="company_question_item")
    number = models.IntegerField(default=0)
    type = models.IntegerField(choices=type_choice, default=0)
    title = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    choice_type = models.IntegerField(choices=choice_type_choice, default=0)
    choice_count = models.IntegerField(blank=True, null=True)
    required_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'company_question_item'

class CompanyQuestionItemChoice(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    question_item = models.ForeignKey(CompanyQuestionItem, on_delete=models.CASCADE, related_name="company_question_item_choice")
    number = models.IntegerField(default=0)
    text = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'company_question_item_choice'



class ShopQuestion(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    display_id = models.BigIntegerField()
    company = models.ForeignKey(CompanyQuestion, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_question")
    shop = models.ForeignKey(AuthShop, on_delete=models.CASCADE, blank=True, null=True, related_name="shop_question")
    title = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    color = models.CharField(max_length=1,null=True)
    favorite_flg = models.BooleanField(default=False)
    count = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255,null=True)
    use_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_question'

class ShopQuestionItem(models.Model):
    type_choice = (
        (1, '氏名'),
        (2, 'フリガナ'),
        (3, '年齢'),
        (4, '性別'),
        (5, '電話番号'),
        (6, 'メールアドレス'),
        (7, '生年月日'),
        (8, '住所'),
        (9, 'プロフィール写真'),
        (10, '画像'),
        (11, '動画'),
        (51, '予約形式'),
        (52, '予約日程'),
        (53, '予約可能日'),
        (54, '予約日程再調整'),
        (99, '設問'),
    )
    choice_type_choice = (
        (1, 'フリーテキスト'),
        (2, 'ラジオボタン'),
        (3, 'チェックボックス'),
        (4, 'プルダウン'),
        (5, '日付'),
        (6, '時間'),
        (7, '日時'),
    )

    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    question = models.ForeignKey(ShopQuestion, on_delete=models.CASCADE, related_name="shop_question_item")
    number = models.IntegerField(default=0)
    type = models.IntegerField(choices=type_choice, default=0)
    title = models.CharField(max_length=255,null=True)
    description = models.CharField(max_length=255,null=True)
    choice_type = models.IntegerField(choices=choice_type_choice, default=0)
    choice_count = models.IntegerField(blank=True, null=True)
    required_flg = models.BooleanField(default=False)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'shop_question_item'

class ShopQuestionItemChoice(models.Model):
    id = models.CharField(primary_key=True, max_length=255, null=False, blank=False, unique=True)
    question_item = models.ForeignKey(ShopQuestionItem, on_delete=models.CASCADE, related_name="shop_question_item_choice")
    number = models.IntegerField(default=0)
    text = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(blank=False, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'shop_question_item_choice'