# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 18:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0007_solutionratiooneunit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='implementation',
            old_name='case_study_id',
            new_name='case_study',
        ),
        migrations.RenameField(
            model_name='solution',
            old_name='case_study_id',
            new_name='case_study',
        ),
        migrations.RenameField(
            model_name='solutioncategory',
            old_name='case_study_id',
            new_name='case_study',
        ),
        migrations.RenameField(
            model_name='stakeholder',
            old_name='stakeholder_category_id',
            new_name='stakeholder_category',
        ),
        migrations.RenameField(
            model_name='stakeholdercategory',
            old_name='case_study_id',
            new_name='case_study',
        ),
        migrations.RenameField(
            model_name='strategy',
            old_name='case_study_id',
            new_name='case_study',
        ),
        migrations.RenameField(
            model_name='userap12',
            old_name='case_study_id',
            new_name='case_study',
        ),
        migrations.RenameField(
            model_name='userap34',
            old_name='case_study_id',
            new_name='case_study',
        ),
        migrations.AlterUniqueTogether(
            name='implementation',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='solutioncategory',
            unique_together=set([('case_study', 'user_ap12_id', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='stakeholder',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='stakeholdercategory',
            unique_together=set([('case_study', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='strategy',
            unique_together=set([('case_study', 'user_id', 'name')]),
        ),
        migrations.RemoveField(
            model_name='stakeholder',
            name='case_study_id',
        ),
    ]
