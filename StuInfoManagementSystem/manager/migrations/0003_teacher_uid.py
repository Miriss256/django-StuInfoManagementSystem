# Generated by Django 5.0.6 on 2024-07-28 08:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0002_alter_student_phone_number_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="uid",
            field=models.IntegerField(default=11001, verbose_name="教师ID"),
        ),
    ]
