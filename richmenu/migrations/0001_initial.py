# Generated by Django 4.0 on 2024-03-26 22:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import richmenu.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('template', '0001_initial'),
        ('user', '0001_initial'),
        ('sign', '0001_initial'),
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyRichMenu',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255, null=True)),
                ('menu_type', models.IntegerField(choices=[(0, 'default'), (1, 'another')], default=0)),
                ('menu_flg', models.BooleanField(default=False)),
                ('menu_text', models.CharField(max_length=255, null=True)),
                ('type', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to=richmenu.models.richmenu_image_path)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_rich_menu', to='sign.authcompany')),
            ],
            options={
                'db_table': 'company_rich_menu',
            },
        ),
        migrations.CreateModel(
            name='HeadRichMenu',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255, null=True)),
                ('menu_type', models.IntegerField(choices=[(0, 'default'), (1, 'another')], default=0)),
                ('menu_flg', models.BooleanField(default=False)),
                ('menu_text', models.CharField(max_length=255, null=True)),
                ('type', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to=richmenu.models.richmenu_image_path)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'head_rich_menu',
            },
        ),
        migrations.CreateModel(
            name='ShopRichMenu',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('rich_menu_id', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('menu_type', models.IntegerField(choices=[(0, 'default'), (1, 'another')], default=0)),
                ('menu_flg', models.BooleanField(default=False)),
                ('menu_text', models.CharField(max_length=255, null=True)),
                ('type', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to=richmenu.models.richmenu_image_path)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('favorite_flg', models.BooleanField(default=False)),
                ('use_flg', models.BooleanField(default=False)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_rich_menu', to='sign.authcompany')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_rich_menu', to='richmenu.companyrichmenu')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_rich_menu', to='sign.authshop')),
            ],
            options={
                'db_table': 'shop_rich_menu',
            },
        ),
        migrations.CreateModel(
            name='ShopRichMenuItem',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('number', models.CharField(max_length=1, null=True)),
                ('type', models.IntegerField(choices=[(0, 'none'), (1, 'link'), (2, 'video'), (3, 'questionform'), (4, 'reserve'), (5, 'history'), (6, 'online'), (7, 'company'), (8, 'text')], default=0)),
                ('url', models.CharField(max_length=255, null=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_rich_menu_item', to='question.shopquestion')),
                ('rich_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_rich_menu_item', to='richmenu.shoprichmenu')),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_rich_menu_item', to='template.shoptemplatevideo')),
            ],
            options={
                'db_table': 'shop_rich_menu_item',
            },
        ),
        migrations.CreateModel(
            name='UserRichMenuClick',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('count', models.IntegerField(default=0)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('rich_menu_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_rich_menu_click', to='richmenu.shoprichmenuitem')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_rich_menu_click', to='user.lineuser')),
            ],
            options={
                'db_table': 'user_rich_menu_click',
            },
        ),
        migrations.CreateModel(
            name='UserRichMenu',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('rich_menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_rich_menu', to='richmenu.shoprichmenu')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_rich_menu', to='user.lineuser')),
            ],
            options={
                'db_table': 'user_rich_menu',
            },
        ),
        migrations.CreateModel(
            name='HeadRichMenuItem',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('number', models.CharField(max_length=1, null=True)),
                ('type', models.IntegerField(choices=[(0, 'none'), (1, 'link'), (2, 'video'), (3, 'questionform'), (4, 'reserve'), (5, 'history'), (6, 'online'), (7, 'company'), (8, 'text')], default=0)),
                ('url', models.CharField(max_length=255, null=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_rich_menu_item', to='question.headquestion')),
                ('rich_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_rich_menu_item', to='richmenu.headrichmenu')),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_rich_menu_item', to='template.headtemplatevideo')),
            ],
            options={
                'db_table': 'head_rich_menu_item',
            },
        ),
        migrations.CreateModel(
            name='CompanyRichMenuItem',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('number', models.CharField(max_length=1, null=True)),
                ('type', models.IntegerField(choices=[(0, 'none'), (1, 'link'), (2, 'video'), (3, 'questionform'), (4, 'reserve'), (5, 'history'), (6, 'online'), (7, 'company'), (8, 'text')], default=0)),
                ('url', models.CharField(max_length=255, null=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_rich_menu_item', to='question.companyquestion')),
                ('rich_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_rich_menu_item', to='richmenu.companyrichmenu')),
                ('video', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_rich_menu_item', to='template.companytemplatevideo')),
            ],
            options={
                'db_table': 'company_rich_menu_item',
            },
        ),
        migrations.AddField(
            model_name='companyrichmenu',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_rich_menu', to='richmenu.headrichmenu'),
        ),
    ]
