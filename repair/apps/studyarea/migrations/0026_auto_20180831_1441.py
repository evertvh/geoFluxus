# Generated by Django 2.0 on 2018-08-31 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studyarea', '0025_auto_20180829_1319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='_parent_area',
            new_name='parent_area',
        ),
    ]
