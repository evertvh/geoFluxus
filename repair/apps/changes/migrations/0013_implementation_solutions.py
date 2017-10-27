# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0012_auto_20171007_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='implementation',
            name='solutions',
            field=models.ManyToManyField(through='changes.SolutionInImplementation', to='changes.Solution'),
        ),
    ]
