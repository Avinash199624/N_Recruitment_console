# Generated by Django 3.1.7 on 2021-09-01 11:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20210831_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReligionMaster',
            fields=[
                ('created_by', models.CharField(blank=True, help_text='username', max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, help_text='username', max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
                ('religion_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('religion_name', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='religion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_religion', to='user.religionmaster'),
        ),
    ]
