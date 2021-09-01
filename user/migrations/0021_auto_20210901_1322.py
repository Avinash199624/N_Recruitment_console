# Generated by Django 3.1.7 on 2021-09-01 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_remove_userprofile_religion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_religion',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='religion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_religion', to='user.religionmaster'),
        ),
    ]
