# Generated by Django 3.1.7 on 2021-05-05 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_user_mobile_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='passport_number',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
