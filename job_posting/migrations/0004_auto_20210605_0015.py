# Generated by Django 3.1.7 on 2021-06-05 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_posting', '0003_auto_20210529_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobposting',
            old_name='description',
            new_name='ad_approval_id',
        ),
        migrations.AddField(
            model_name='jobposting',
            name='post_ad_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobposting',
            name='pre_ad_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
