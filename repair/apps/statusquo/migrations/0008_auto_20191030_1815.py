# Generated by Django 2.2.6 on 2019-10-30 18:15

from django.db import migrations
import enumfields.fields
import repair.apps.statusquo.models.filters


class Migration(migrations.Migration):

    dependencies = [
        ('statusquo', '0007_auto_20191030_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowfilter',
            name='role',
            field=enumfields.fields.EnumIntegerField(default=1, enum=repair.apps.statusquo.models.filters.Role),
        ),
    ]
