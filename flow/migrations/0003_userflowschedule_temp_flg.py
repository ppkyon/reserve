# Generated by Django 4.0 on 2024-05-16 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userflowschedule',
            name='temp_flg',
            field=models.BooleanField(default=False),
        ),
    ]
