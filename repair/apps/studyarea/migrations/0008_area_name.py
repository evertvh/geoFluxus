# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-15 01:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyarea', '0007_auto_20180115_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
    ]