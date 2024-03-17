from django.core.management import call_command
from django.db import migrations

def load_fixture(apps, schema_editor):
    call_command('loaddata', 'fixture/json/first_manager.json', app_label='first_manager')

class Migration(migrations.Migration):

    dependencies = [
        ('fixture', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]