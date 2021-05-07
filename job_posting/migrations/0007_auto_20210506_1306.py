# Generated by Django 3.1.7 on 2021-05-06 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_posting', '0006_auto_20210503_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobpostingrequirementpositions',
            name='total_cost',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobpostingrequirementpositions',
            name='job_posting_requirement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manpower_position', to='job_posting.jobpostingrequirement'),
        ),
        migrations.AlterField(
            model_name='jobpostingrequirementpositions',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='positions_position', to='job_posting.positionmaster'),
        ),
    ]
