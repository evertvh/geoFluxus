# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 22:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0035_auto_20171015_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='sink',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activity',
            name='source',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activitygroup',
            name='sink',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='activitygroup',
            name='source',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='actor',
            name='sink',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='actor',
            name='source',
            field=models.BooleanField(default=False),
        ),
    ]
