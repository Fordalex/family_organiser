# Generated by Django 3.0.7 on 2020-07-06 01:43

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('status', '0008_auto_20200706_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_users', to=settings.AUTH_USER_MODEL),
        ),
    ]