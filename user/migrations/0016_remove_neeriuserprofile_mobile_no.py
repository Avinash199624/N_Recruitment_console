# Generated by Django 3.1.7 on 2021-05-10 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_userauthentication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='neeriuserprofile',
            name='mobile_no',
        ),
    ]