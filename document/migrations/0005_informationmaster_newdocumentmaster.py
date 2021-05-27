# Generated by Django 3.1.7 on 2021-05-24 19:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0004_auto_20210501_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformationMaster',
            fields=[
                ('created_by', models.CharField(blank=True, help_text='username', max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, help_text='username', max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
                ('info_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('info_name', models.CharField(blank=True, max_length=50, null=True)),
                ('info_type', models.CharField(blank=True, choices=[('caste', 'CASTE'), ('personal', 'PERSONAL'), ('qualification', 'QUALIFICATION'), ('experience', 'EXPERIENCE'), ('published papers', 'PUBLISHED_PAPERS'), ('others', 'OTHERS')], max_length=30, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NewDocumentMaster',
            fields=[
                ('created_by', models.CharField(blank=True, help_text='username', max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, help_text='username', max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
                ('doc_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('doc_name', models.CharField(blank=True, max_length=50, null=True)),
                ('doc_type', models.CharField(blank=True, choices=[('caste', 'CASTE'), ('personal', 'PERSONAL'), ('qualification', 'QUALIFICATION'), ('experience', 'EXPERIENCE'), ('published papers', 'PUBLISHED_PAPERS'), ('others', 'OTHERS')], max_length=30, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]