# Generated by Django 5.0.6 on 2024-07-30 08:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0006_alter_teacher_uid"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="img",
            field=models.FileField(
                default="", max_length=128, upload_to="StudentTx", verbose_name="头像"
            ),
        ),
    ]
