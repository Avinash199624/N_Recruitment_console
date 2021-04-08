# Generated by Django 3.1.7 on 2021-04-08 13:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('temp_type', models.CharField(blank=True, max_length=100, null=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
            ],
        ),
        migrations.CreateModel(
            name='TemplateMaster',
            fields=[
                ('template_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('template_name', models.CharField(blank=True, max_length=100, null=True)),
                ('subject', models.CharField(blank=True, max_length=200, null=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='template_type', to='communication_template.templatetype')),
            ],
        ),
        migrations.AddConstraint(
            model_name='templatemaster',
            constraint=models.UniqueConstraint(condition=models.Q(is_active=True), fields=('type', 'is_active'), name='unique_level_per_type'),
        ),
    ]
