# Generated by Django 3.1.7 on 2021-04-01 14:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentMaster',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('doc_type', models.CharField(blank=True, max_length=50, null=True)),
                ('doc_name', models.CharField(blank=True, max_length=50, null=True)),
                ('file_size', models.IntegerField(blank=True, help_text='Document file size in MB', null=True)),
            ],
        ),
    ]
