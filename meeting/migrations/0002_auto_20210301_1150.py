# Generated by Django 3.1.5 on 2021-03-01 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("meeting", "0001_initial"),
        ("visit", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="meetingattendace",
            name="user",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="meeting",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="visit.visitsites"
            ),
        ),
    ]