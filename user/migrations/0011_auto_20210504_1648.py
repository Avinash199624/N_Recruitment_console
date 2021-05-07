# Generated by Django 3.1.7 on 2021-05-04 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_user_mobile_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.CharField(blank=True, help_text='username', max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, help_text='username', max_length=25, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False, help_text='Used for Soft Delete')),
                ('bond_title', models.CharField(blank=True, max_length=100, null=True)),
                ('bond_details', models.TextField(blank=True, null=True)),
                ('organisation_name', models.CharField(blank=True, max_length=200, null=True)),
                ('bond_start_date', models.DateField(blank=True, null=True)),
                ('bond_end_date', models.DateField(blank=True, null=True)),
                ('notice_period_min', models.IntegerField(blank=True, help_text='notice_period_min_in_days', null=True)),
                ('notice_period_max', models.IntegerField(blank=True, help_text='notice_period_max_in_days', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='OtherInfo',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='other_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_info', to='user.otherinformation'),
        ),
    ]