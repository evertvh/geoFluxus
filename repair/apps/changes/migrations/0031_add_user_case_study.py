# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0030_auto_20171008_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='casestudy',
            field=models.IntegerField(default=5),
        ),
    ]
