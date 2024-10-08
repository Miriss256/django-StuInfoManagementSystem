# Generated by Django 5.0.6 on 2024-07-30 15:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0009_manager_usertype_student_usertype_teacher_usertype"),
    ]

    operations = [
        migrations.AlterField(
            model_name="manager",
            name="usertype",
            field=models.SmallIntegerField(default=1, verbose_name="类型"),
        ),
        migrations.AlterField(
            model_name="student",
            name="usertype",
            field=models.SmallIntegerField(default=3, verbose_name="类型"),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="usertype",
            field=models.SmallIntegerField(default=2, verbose_name="类型"),
        ),
    ]
