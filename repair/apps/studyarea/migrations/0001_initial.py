# Generated by Django 2.2.6 on 2019-11-10 08:51

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import repair.apps.login.models.bases
import repair.apps.utils.protect_cascade


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wms_client', '0013_auto_20190508_1210'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminLevels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('level', models.IntegerField()),
                ('casestudy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'unique_together': {('casestudy', 'level'), ('casestudy', 'name')},
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='StakeholderCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('casestudy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True, null=True)),
                ('stakeholder_category', models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='studyarea.StakeholderCategory')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LayerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('order', models.IntegerField(default=1)),
                ('tag', models.CharField(blank=True, default='', max_length=20)),
                ('casestudy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('included', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=1)),
                ('category', models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='studyarea.LayerCategory')),
                ('style', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wms_client.LayerStyle')),
                ('wms_layer', models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='wms_client.WMSLayer')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ChartCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('casestudy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='charts')),
                ('chart_category', models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='studyarea.ChartCategory')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('code', models.TextField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('inhabitants', models.BigIntegerField(default=0)),
                ('adminlevel', models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='studyarea.AdminLevels')),
                ('parent_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studyarea.Area')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
    ]
