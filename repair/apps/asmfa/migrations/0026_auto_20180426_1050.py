# Generated by Django 2.0 on 2018-04-26 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0025_auto_20180327_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrativelocation',
            name='country',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='operationallocation',
            name='country',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
