# Generated by Django 3.1.7 on 2021-06-25 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20210619_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='userauthentication',
            name='account_lock_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userauthentication',
            name='wrong_login_attempt',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
