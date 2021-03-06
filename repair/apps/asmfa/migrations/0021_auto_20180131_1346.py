# Generated by Django 2.0 on 2018-01-31 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0020_auto_20180130_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nace', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'default_permissions': ('add', 'change', 'delete', 'view')},
        ),
        migrations.AlterModelOptions(
            name='waste',
            options={'default_permissions': ('add', 'change', 'delete', 'view')},
        ),
        migrations.RemoveField(
            model_name='activity2activity',
            name='fractions',
        ),
        migrations.RemoveField(
            model_name='actor2actor',
            name='fractions',
        ),
        migrations.RemoveField(
            model_name='group2group',
            name='fractions',
        ),
        migrations.RemoveField(
            model_name='product',
            name='id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='nace',
        ),
        migrations.RemoveField(
            model_name='productfraction',
            name='default',
        ),
        migrations.RemoveField(
            model_name='productfraction',
            name='keyflow',
        ),
        migrations.RemoveField(
            model_name='productfraction',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productfraction',
            name='waste',
        ),
        migrations.RemoveField(
            model_name='waste',
            name='id',
        ),
        migrations.RemoveField(
            model_name='waste',
            name='nace',
        ),
        migrations.AddField(
            model_name='activity2activity',
            name='composition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='activity2activity', to='asmfa.Composition'),
        ),
        migrations.AddField(
            model_name='actor2actor',
            name='composition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actor2actor', to='asmfa.Composition'),
        ),
        migrations.AddField(
            model_name='group2group',
            name='composition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group2group', to='asmfa.Composition'),
        ),
        migrations.AddField(
            model_name='product',
            name='composition_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='asmfa.Composition'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productfraction',
            name='composition',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fractions', to='asmfa.Composition'),
        ),
        migrations.AddField(
            model_name='waste',
            name='composition_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='asmfa.Composition'),
            preserve_default=False,
        ),
    ]
