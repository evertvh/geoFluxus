# Generated by Django 2.2.7 on 2019-12-05 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statusquo', '0002_auto_20191204_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowfilter',
            name='composite',
            field=models.TextField(null=True),
        ),
    ]
