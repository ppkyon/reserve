# Generated by Django 4.0 on 2024-05-04 01:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAlert',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('number', models.IntegerField(default=0)),
                ('text', models.TextField(blank=True, max_length=1000, null=True)),
                ('status', models.IntegerField(choices=[(1, 'info'), (2, 'notice'), (3, 'error')], default=0)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_alert', to='user.lineuser')),
            ],
            options={
                'db_table': 'user_alert',
            },
        ),
    ]
