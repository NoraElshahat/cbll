# Generated by Django 3.1.5 on 2021-03-28 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0004_cbluser_img")]

    operations = [
        migrations.AlterField(
            model_name="cbluser",
            name="img",
            field=models.ImageField(
                blank=True, upload_to="storage/users/", verbose_name="user picture"
            ),
        )
    ]
