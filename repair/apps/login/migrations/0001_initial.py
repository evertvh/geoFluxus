# Generated by Django 2.2.6 on 2019-11-10 08:51

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import repair.apps.login.models.bases


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseStudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('focusarea', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('description', models.TextField(blank=True, null=True)),
                ('show_on_welcome_map', models.BooleanField(default=True)),
                ('target_year', models.IntegerField(default=2020)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'setupmode', 'dataentry', 'conclusions'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.TextField(blank=True, default='')),
                ('session', models.TextField(blank=True, default='')),
                ('can_change_password', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UserInCasestudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.TextField(blank=True, default='')),
                ('gets_evaluated', models.BooleanField(default=False)),
                ('alias', models.TextField(blank=True, default='')),
                ('casestudy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.Profile')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'unique_together': {('user', 'casestudy')},
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='profile',
            name='casestudies',
            field=models.ManyToManyField(through='login.UserInCasestudy', to='login.CaseStudy'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
