from django.contrib.auth.models import Group
from django.db import migrations

GROUPS = ['Administrador', 'Ouvinte', 'Narrador']


def create_initial_groups(apps, schema_editor):
    for name in GROUPS:
        Group(name=name).save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_groups),
    ]
