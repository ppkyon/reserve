from django.core.management import call_command
from django.db import migrations

def load_fixture(apps, schema_editor):
    call_command('loaddata', 'fixture/json/country.json', app_label='country')
    call_command('loaddata', 'fixture/json/first_manager.json', app_label='first_manager')
    call_command('loaddata', 'fixture/json/prefecture.json', app_label='prefecture')
    call_command('loaddata', 'fixture/json/work_parent.json', app_label='work_parent')
    call_command('loaddata', 'fixture/json/work_child.json', app_label='work_child')

class Migration(migrations.Migration):

    dependencies = [
        ('fixture', '0001_initial'),
        ('sign', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]