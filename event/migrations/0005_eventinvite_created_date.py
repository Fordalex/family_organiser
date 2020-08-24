# Generated by Django 3.0.7 on 2020-08-24 01:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_event_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventinvite',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
