# Generated by Django 4.0 on 2024-02-25 13:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import template.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sign', '0002_managerprofile_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyTemplateText',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255, null=True)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_template_text', to='sign.authcompany')),
            ],
            options={
                'db_table': 'company_template_text',
            },
        ),
        migrations.CreateModel(
            name='HeadTemplateGreeting',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('number', models.IntegerField(default=0)),
                ('message_type', models.IntegerField(choices=[(1, 'text'), (2, 'image'), (3, 'video'), (4, 'template')], default=0)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=template.models.template_image_path)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=template.models.template_video_path)),
                ('video_width', models.IntegerField(blank=True, null=True)),
                ('video_height', models.IntegerField(blank=True, null=True)),
                ('video_thumbnail', models.FileField(blank=True, null=True, upload_to=template.models.template_video_thumbnail_path)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'head_template_greeting',
            },
        ),
        migrations.CreateModel(
            name='HeadTemplateText',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255, null=True)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'head_template_text',
            },
        ),
        migrations.CreateModel(
            name='HeadTemplateVideo',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=template.models.template_video_path)),
                ('video_width', models.IntegerField(blank=True, null=True)),
                ('video_height', models.IntegerField(blank=True, null=True)),
                ('video_time', models.IntegerField(blank=True, null=True)),
                ('video_size', models.IntegerField(blank=True, null=True)),
                ('video_thumbnail', models.FileField(blank=True, null=True, upload_to=template.models.template_video_thumbnail_path)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'head_template_video',
            },
        ),
        migrations.CreateModel(
            name='ShopTemplateText',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255, null=True)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_template_text', to='sign.authcompany')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_template_text', to='sign.authshop')),
            ],
            options={
                'db_table': 'shop_template_text',
            },
        ),
        migrations.CreateModel(
            name='ShopTemplateVideo',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=template.models.template_video_path)),
                ('video_width', models.IntegerField(blank=True, null=True)),
                ('video_height', models.IntegerField(blank=True, null=True)),
                ('video_time', models.IntegerField(blank=True, null=True)),
                ('video_size', models.IntegerField(blank=True, null=True)),
                ('video_thumbnail', models.FileField(blank=True, null=True, upload_to=template.models.template_video_thumbnail_path)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_template_video', to='sign.authcompany')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_template_video', to='sign.authshop')),
            ],
            options={
                'db_table': 'shop_template_video',
            },
        ),
        migrations.CreateModel(
            name='ShopTemplateTextItem',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('number', models.IntegerField(default=0)),
                ('message_type', models.IntegerField(choices=[(1, 'text'), (2, 'image'), (3, 'video'), (4, 'template')], default=0)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=template.models.template_image_path)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=template.models.template_video_path)),
                ('video_width', models.IntegerField(blank=True, null=True)),
                ('video_height', models.IntegerField(blank=True, null=True)),
                ('video_thumbnail', models.FileField(blank=True, null=True, upload_to=template.models.template_video_thumbnail_path)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_template_text_item', to='template.shoptemplatetext')),
            ],
            options={
                'db_table': 'shop_template_text_item',
            },
        ),
        migrations.CreateModel(
            name='ShopTemplateGreeting',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('number', models.IntegerField(default=0)),
                ('message_type', models.IntegerField(choices=[(1, 'text'), (2, 'image'), (3, 'video'), (4, 'template')], default=0)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=template.models.template_image_path)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=template.models.template_video_path)),
                ('video_width', models.IntegerField(blank=True, null=True)),
                ('video_height', models.IntegerField(blank=True, null=True)),
                ('video_thumbnail', models.FileField(blank=True, null=True, upload_to=template.models.template_video_thumbnail_path)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_template_greeting', to='sign.authcompany')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shop_template_greeting', to='sign.authshop')),
            ],
            options={
                'db_table': 'shop_template_greeting',
            },
        ),
        migrations.CreateModel(
            name='HeadTemplateTextItem',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('number', models.IntegerField(default=0)),
                ('message_type', models.IntegerField(choices=[(1, 'text'), (2, 'image'), (3, 'video'), (4, 'template')], default=0)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=template.models.template_image_path)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=template.models.template_video_path)),
                ('video_width', models.IntegerField(blank=True, null=True)),
                ('video_height', models.IntegerField(blank=True, null=True)),
                ('video_thumbnail', models.FileField(blank=True, null=True, upload_to=template.models.template_video_thumbnail_path)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_template_text_item', to='template.headtemplatetext')),
            ],
            options={
                'db_table': 'head_template_text_item',
            },
        ),
        migrations.CreateModel(
            name='CompanyTemplateVideo',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=255, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=template.models.template_video_path)),
                ('video_width', models.IntegerField(blank=True, null=True)),
                ('video_height', models.IntegerField(blank=True, null=True)),
                ('video_time', models.IntegerField(blank=True, null=True)),
                ('video_size', models.IntegerField(blank=True, null=True)),
                ('video_thumbnail', models.FileField(blank=True, null=True, upload_to=template.models.template_video_thumbnail_path)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_template_video', to='sign.authcompany')),
            ],
            options={
                'db_table': 'company_template_video',
            },
        ),
        migrations.CreateModel(
            name='CompanyTemplateTextItem',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('number', models.IntegerField(default=0)),
                ('message_type', models.IntegerField(choices=[(1, 'text'), (2, 'image'), (3, 'video'), (4, 'template')], default=0)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=template.models.template_image_path)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=template.models.template_video_path)),
                ('video_width', models.IntegerField(blank=True, null=True)),
                ('video_height', models.IntegerField(blank=True, null=True)),
                ('video_thumbnail', models.FileField(blank=True, null=True, upload_to=template.models.template_video_thumbnail_path)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_template_text_item', to='template.companytemplatetext')),
            ],
            options={
                'db_table': 'company_template_text_item',
            },
        ),
        migrations.CreateModel(
            name='CompanyTemplateGreeting',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('display_id', models.BigIntegerField()),
                ('number', models.IntegerField(default=0)),
                ('message_type', models.IntegerField(choices=[(1, 'text'), (2, 'image'), (3, 'video'), (4, 'template')], default=0)),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=template.models.template_image_path)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('video', models.FileField(blank=True, null=True, upload_to=template.models.template_video_path)),
                ('video_width', models.IntegerField(blank=True, null=True)),
                ('video_height', models.IntegerField(blank=True, null=True)),
                ('video_thumbnail', models.FileField(blank=True, null=True, upload_to=template.models.template_video_thumbnail_path)),
                ('author', models.CharField(max_length=255, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_template_greeting', to='sign.authcompany')),
            ],
            options={
                'db_table': 'company_template_greeting',
            },
        ),
    ]
