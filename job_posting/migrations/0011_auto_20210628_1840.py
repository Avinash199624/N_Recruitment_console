# Generated by Django 3.1.7 on 2021-06-28 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_posting', '0010_auto_20210623_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permanentpositionmaster',
            name='grade',
            field=models.CharField(blank=True, choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='permanentpositionmaster',
            name='level',
            field=models.CharField(blank=True, choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='positionqualificationmapping',
            name='grade',
            field=models.CharField(blank=True, choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('V', 'V')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='positionqualificationmapping',
            name='level',
            field=models.CharField(blank=True, choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV')], max_length=30, null=True),
        ),
    ]
