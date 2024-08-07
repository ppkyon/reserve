# Generated by Django 4.0 on 2024-07-20 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='talkmessage',
            name='sticker_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='talkmessage',
            name='message_type',
            field=models.IntegerField(choices=[(0, 'text'), (1, 'image'), (2, 'video'), (3, 'audio'), (4, 'location'), (5, 'rich_message'), (6, 'rich_video'), (7, 'card_type'), (8, 'button'), (9, 'sticker')], default=0),
        ),
    ]
