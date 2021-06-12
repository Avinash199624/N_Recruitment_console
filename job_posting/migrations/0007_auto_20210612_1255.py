# Generated by Django 3.1.7 on 2021-06-12 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_delete_documentmaster'),
        ('job_posting', '0006_remove_jobposting_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='positionqualificationmapping',
            name='documents_required',
            field=models.ManyToManyField(blank=True, related_name='position_qualification_required_documents', to='document.NewDocumentMaster'),
        ),
        migrations.AddField(
            model_name='positionqualificationmapping',
            name='information_required',
            field=models.ManyToManyField(blank=True, related_name='position_required_info', to='document.InformationMaster'),
        ),
        migrations.AddField(
            model_name='positionqualificationmapping',
            name='position_display_name',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='positionqualificationmapping',
            name='qualification_job_history',
            field=models.ManyToManyField(blank=True, related_name='position_qualification_job_history', to='job_posting.QualificationJobHistoryMaster'),
        ),
        migrations.AlterField(
            model_name='jobposting',
            name='status',
            field=models.CharField(blank=True, choices=[('scheduled', 'Scheduled'), ('published', 'Published'), ('suspended', 'Suspended'), ('cancelled', 'Cancelled'), ('closed', 'Closed'), ('Archived', 'Archived')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='positionqualificationmapping',
            name='qualification',
            field=models.ManyToManyField(blank=True, related_name='position_qualification', to='job_posting.QualificationMaster'),
        ),
    ]
