# Generated by Django 2.0 on 2019-03-25 15:54

from django.db import migrations, models
import repair.apps.utils.protect_cascade


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0040_auto_20190214_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fractionflow',
            name='origin',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='f_outputs', to='asmfa.Actor'),
        ),
    ]
