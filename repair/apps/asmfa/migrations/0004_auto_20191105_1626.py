# Generated by Django 2.2.6 on 2019-11-05 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0003_auto_20191105_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flowchain',
            name='amount',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=3),
        ),
    ]
