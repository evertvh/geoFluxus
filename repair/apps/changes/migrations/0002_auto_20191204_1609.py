# Generated by Django 2.2.7 on 2019-12-04 16:09

from django.db import migrations, models
import django.db.models.deletion
import repair.apps.utils.protect_cascade


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('changes', '0001_initial'),
        ('asmfa', '0003_auto_20191204_1609'),
        ('login', '0001_initial'),
        ('studyarea', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='coordinating_stakeholder',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='studyarea.Stakeholder'),
        ),
        migrations.AddField(
            model_name='strategy',
            name='keyflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asmfa.KeyflowInCasestudy'),
        ),
        migrations.AddField(
            model_name='strategy',
            name='solutions',
            field=models.ManyToManyField(through='changes.SolutionInStrategy', to='changes.Solution'),
        ),
        migrations.AddField(
            model_name='strategy',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.UserInCasestudy'),
        ),
        migrations.AddField(
            model_name='solutionpart',
            name='flow_changes',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='reference_flow_change', to='changes.FlowReference'),
        ),
        migrations.AddField(
            model_name='solutionpart',
            name='flow_reference',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='reference_solution_part', to='changes.FlowReference'),
        ),
        migrations.AddField(
            model_name='solutionpart',
            name='question',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='changes.ImplementationQuestion'),
        ),
        migrations.AddField(
            model_name='solutionpart',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solution_parts', to='changes.Solution'),
        ),
        migrations.AddField(
            model_name='solutioninstrategy',
            name='participants',
            field=models.ManyToManyField(to='studyarea.Stakeholder'),
        ),
        migrations.AddField(
            model_name='solutioninstrategy',
            name='solution',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='changes.Solution'),
        ),
        migrations.AddField(
            model_name='solutioninstrategy',
            name='strategy',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='solutioninstrategy', to='changes.Strategy'),
        ),
        migrations.AddField(
            model_name='solutioncategory',
            name='keyflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asmfa.KeyflowInCasestudy'),
        ),
        migrations.AddField(
            model_name='solution',
            name='solution_category',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='changes.SolutionCategory'),
        ),
        migrations.AddField(
            model_name='possibleimplementationarea',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='possible_implementation_area', to='changes.Solution'),
        ),
        migrations.AddField(
            model_name='implementationquestion',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='changes.Solution'),
        ),
        migrations.AddField(
            model_name='implementationquantity',
            name='implementation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='implementation_quantity', to='changes.SolutionInStrategy'),
        ),
        migrations.AddField(
            model_name='implementationquantity',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='changes.ImplementationQuestion'),
        ),
        migrations.AddField(
            model_name='implementationarea',
            name='implementation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='implementation_area', to='changes.SolutionInStrategy'),
        ),
        migrations.AddField(
            model_name='implementationarea',
            name='possible_implementation_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='changes.PossibleImplementationArea'),
        ),
        migrations.AddField(
            model_name='flowreference',
            name='destination_activity',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='reference_destination', to='asmfa.Activity'),
        ),
        migrations.AddField(
            model_name='flowreference',
            name='destination_area',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='possible_destination_area', to='changes.PossibleImplementationArea'),
        ),
        migrations.AddField(
            model_name='flowreference',
            name='material',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='asmfa.Material'),
        ),
        migrations.AddField(
            model_name='flowreference',
            name='origin_activity',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='reference_origin', to='asmfa.Activity'),
        ),
        migrations.AddField(
            model_name='flowreference',
            name='origin_area',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='possible_origin_area', to='changes.PossibleImplementationArea'),
        ),
        migrations.AddField(
            model_name='flowreference',
            name='process',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='asmfa.Process'),
        ),
        migrations.AddField(
            model_name='affectedflow',
            name='destination_activity',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='affected_destinations', to='asmfa.Activity'),
        ),
        migrations.AddField(
            model_name='affectedflow',
            name='material',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='affected_materials', to='asmfa.Material'),
        ),
        migrations.AddField(
            model_name='affectedflow',
            name='origin_activity',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='affected_origins', to='asmfa.Activity'),
        ),
        migrations.AddField(
            model_name='affectedflow',
            name='process',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='affected_processes', to='asmfa.Process'),
        ),
        migrations.AddField(
            model_name='affectedflow',
            name='solution_part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affected_flows', to='changes.SolutionPart'),
        ),
    ]