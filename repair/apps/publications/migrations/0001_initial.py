# Generated by Django 2.2.6 on 2019-11-05 11:42

from django.db import migrations, models
import django.db.models.deletion
import repair.apps.login.models.bases


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publications_bootstrap', '0006_auto_20191009_1434'),
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationInCasestudy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casestudy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications_bootstrap.Publication')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'unique_together': {('publication', 'casestudy')},
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
    ]
