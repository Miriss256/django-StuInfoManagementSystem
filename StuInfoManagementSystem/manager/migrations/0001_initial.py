# Generated by Django 5.0.6 on 2024-07-27 10:14

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="manager",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="用户名")),
                ("password", models.CharField(max_length=64, verbose_name="密码")),
            ],
        ),
        migrations.CreateModel(
            name="student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="姓名")),
                ("age", models.IntegerField(verbose_name="年龄")),
                (
                    "gender",
                    models.SmallIntegerField(
                        choices=[(1, "男"), (2, "女")], default=1, verbose_name="性别"
                    ),
                ),
                ("password", models.CharField(max_length=64, verbose_name="密码")),
                ("grade", models.IntegerField(verbose_name="年级")),
                ("classes", models.CharField(max_length=32, verbose_name="班级")),
                ("major", models.CharField(max_length=32, verbose_name="专业")),
                ("studentid", models.IntegerField(verbose_name="学号")),
                ("faculty", models.CharField(max_length=32, verbose_name="院系")),
                ("address", models.CharField(max_length=128, verbose_name="住址")),
                ("phone_number", models.IntegerField(verbose_name="手机号")),
            ],
        ),
        migrations.CreateModel(
            name="teacher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, verbose_name="姓名")),
                ("age", models.IntegerField(verbose_name="年龄")),
                (
                    "gender",
                    models.SmallIntegerField(
                        choices=[(1, "男"), (2, "女")], default=1, verbose_name="性别"
                    ),
                ),
                ("create_time", models.DateField(verbose_name="入职时间")),
                (
                    "salary",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10, verbose_name="工资"
                    ),
                ),
                ("password", models.CharField(max_length=64, verbose_name="密码")),
                (
                    "department",
                    models.SmallIntegerField(
                        choices=[
                            (1, "教育部"),
                            (2, "数学部"),
                            (3, "英语部"),
                            (4, "化学部"),
                            (5, "生物部"),
                            (6, "人文部"),
                            (7, "语文部"),
                        ],
                        default=1,
                        verbose_name="部门",
                    ),
                ),
                ("faculty", models.CharField(max_length=32, verbose_name="院系")),
                (
                    "level",
                    models.SmallIntegerField(
                        choices=[(1, "普通"), (2, "优秀"), (3, "特级")],
                        default=1,
                        verbose_name="级别",
                    ),
                ),
                ("phone_number", models.IntegerField(verbose_name="手机号")),
            ],
        ),
    ]
