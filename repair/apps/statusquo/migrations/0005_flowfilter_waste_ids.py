# Generated by Django 2.2.6 on 2019-10-30 16:56

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('statusquo', '0004_flowfilter_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowfilter',
            name='waste_ids',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
