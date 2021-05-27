# Generated by Django 3.1.5 on 2021-03-28 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("visit", "0002_auto_20210301_1219")]

    operations = [
        migrations.AlterField(
            model_name="visit",
            name="img_one",
            field=models.ImageField(
                blank=True,
                default="",
                upload_to="storage/visits/",
                verbose_name="Other image",
            ),
        ),
        migrations.AlterField(
            model_name="visit",
            name="img_two",
            field=models.ImageField(
                blank=True,
                default="",
                upload_to="storage/visits/",
                verbose_name="Other image",
            ),
        ),
        migrations.AlterField(
            model_name="visit",
            name="main_img",
            field=models.ImageField(
                blank=True,
                default="",
                upload_to="storage/visits/",
                verbose_name="Main image",
            ),
        ),
    ]