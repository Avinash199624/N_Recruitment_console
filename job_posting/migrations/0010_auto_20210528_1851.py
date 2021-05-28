# Generated by Django 3.1.7 on 2021-05-28 18:51

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0007_auto_20210527_1549'),
        ('job_posting', '0009_appealmaster'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewPositionMaster',
            fields=[
                ('created_by', models.CharField(blank=True, help_text='username', max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, help_text='username', max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
                ('position_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position_name', models.CharField(blank=True, max_length=300, null=True)),
                ('position_display_name', models.CharField(blank=True, max_length=300, null=True)),
                ('min_age', models.PositiveIntegerField(blank=True, null=True)),
                ('max_age', models.PositiveIntegerField(blank=True, null=True)),
                ('documents_required', models.ManyToManyField(blank=True, related_name='required_documents', to='document.NewDocumentMaster')),
                ('information_required', models.ManyToManyField(blank=True, related_name='required_info', to='document.InformationMaster')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QualificationJobHistoryMaster',
            fields=[
                ('created_by', models.CharField(blank=True, help_text='username', max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, help_text='username', max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
                ('qualification_job_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('qualification', models.CharField(blank=True, max_length=300, null=True)),
                ('short_code', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=300, null=True), blank=True, null=True, size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='qualificationmaster',
            name='qualification_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='TemporaryPositionMaster',
            fields=[
                ('created_by', models.CharField(blank=True, help_text='username', max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, help_text='username', max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
                ('temp_position_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('allowance', models.CharField(blank=True, choices=[('hra', 'HRA'), ('consolidated', 'CONSOLIDATED')], max_length=30, null=True)),
                ('salary', models.FloatField(blank=True, null=True)),
                ('temp_position_master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='temp_positon', to='job_posting.newpositionmaster')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PermanentPositionMaster',
            fields=[
                ('created_by', models.CharField(blank=True, help_text='username', max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, help_text='username', max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
                ('perm_position_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('grade', models.CharField(blank=True, choices=[('i', 'I'), ('ii', 'II'), ('iii', 'III'), ('iv', 'IV'), ('v', 'V')], max_length=30, null=True)),
                ('level', models.CharField(blank=True, choices=[('i', 'I'), ('ii', 'II'), ('iii', 'III'), ('iv', 'IV')], max_length=30, null=True)),
                ('perm_position_master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='perm_positon', to='job_posting.newpositionmaster')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newpositionmaster',
            name='qualification',
            field=models.ManyToManyField(blank=True, related_name='qualification_master_position', to='job_posting.QualificationMaster'),
        ),
        migrations.AddField(
            model_name='newpositionmaster',
            name='qualification_job_history',
            field=models.ManyToManyField(blank=True, related_name='qualification_job_history', to='job_posting.QualificationJobHistoryMaster'),
        ),
        migrations.AlterField(
            model_name='jobpostingrequirement',
            name='manpower_positions',
            field=models.ManyToManyField(blank=True, related_name='job_positions', through='job_posting.JobPostingRequirementPositions', to='job_posting.TemporaryPositionMaster'),
        ),
        migrations.AlterField(
            model_name='jobpostingrequirementpositions',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='positions_position', to='job_posting.temporarypositionmaster'),
        ),
    ]
