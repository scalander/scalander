# Generated by Django 4.0 on 2022-10-20 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_app', '0004_remove_meeting_lock_in_duration_meeting_lock_in_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingtimeproposal',
            name='end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='meetingtimeproposal',
            name='start',
            field=models.DateTimeField(),
        ),
    ]