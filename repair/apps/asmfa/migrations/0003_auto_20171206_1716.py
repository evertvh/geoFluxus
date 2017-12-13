# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-06 16:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0002_auto_20171205_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity2activity',
            name='description',
            field=models.TextField(blank=True, max_length=510, null=True),
        ),
        migrations.AddField(
            model_name='actor2actor',
            name='description',
            field=models.TextField(blank=True, max_length=510, null=True),
        ),
        migrations.AddField(
            model_name='group2group',
            name='description',
            field=models.TextField(blank=True, max_length=510, null=True),
        ),
        migrations.AlterField(
            model_name='administrativelocation',
            name='actor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='administrative_location', to='asmfa.Actor'),
        ),
        migrations.AlterField(
            model_name='operationallocation',
            name='actor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operational_locations', to='asmfa.Actor'),
        ),
        migrations.AlterField(
            model_name='productfraction',
            name='fraction',
            field=models.FloatField(default=1),
        ),
    ]