# Generated by Django 2.2.1 on 2019-08-06 09:44

from django.db import migrations
import enumfields.fields
import repair.apps.changes.models.solutions


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0043_auto_20190805_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutionpart',
            name='scheme',
            field=enumfields.fields.EnumIntegerField(default=0, enum=repair.apps.changes.models.solutions.Scheme),
        ),
    ]
