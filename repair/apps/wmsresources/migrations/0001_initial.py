# Generated by Django 2.2.6 on 2019-10-15 14:16

from django.db import migrations, models
import django.db.models.deletion
import repair.apps.login.models.bases


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wms_client', '0013_auto_20190508_1210'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WMSResourceInCasestudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casestudy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
                ('wmsresource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wms_client.WMSResource')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'unique_together': {('wmsresource', 'casestudy')},
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
    ]
