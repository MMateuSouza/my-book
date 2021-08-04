from django.contrib.auth.models import Group
from django.db import migrations

GROUPS = ['Administrador', 'Consumidor', 'Narrador']


def create_initial_groups(apps, schema_editor):
    for name in GROUPS:
        Group(name=name).save()


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunPython(create_initial_groups),
    ]
