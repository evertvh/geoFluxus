# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-19 20:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studyarea', '0008_area_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='level',
            new_name='adminlevel',
        ),
        migrations.RemoveField(
            model_name='area',
            name='casestudy',
        ),
    ]
