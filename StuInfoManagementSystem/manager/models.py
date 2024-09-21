from django.db import models
from django.core.validators import RegexValidator


class manager(models.Model):
    """管理员表"""
    name = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)
    usertype = models.SmallIntegerField(verbose_name="类型",default=1)
    
    def __str__(self):
        return self.name

MOBILE_REGEX = RegexValidator(
    regex=r"^1[3-9]\d{9}$", message="手机号格式错误", code="invalid_mobile"
)
class teacher(models.Model):
    """教师表"""
    uid = models.IntegerField(verbose_name="教师ID")
    name = models.CharField(verbose_name="姓名",max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    GENDER_CHOICES = (
        (1,"男"),
        (2,"女")
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=GENDER_CHOICES,default=1)
    create_time = models.DateField(verbose_name="入职时间")
    salary = models.DecimalField(
        verbose_name="工资", max_digits=10, decimal_places=2, default=0
    )
    password = models.CharField(verbose_name="密码",max_length=64)
    DEPARTMENTS_CHOICES = (
        (1,"教育部"),
        (2,"数学部"),
        (3,"英语部"),
        (4,"化学部"),
        (5,"生物部"),
        (6,"人文部"),
        (7,"语文部"),
        )
    department = models.SmallIntegerField(verbose_name="部门",choices=DEPARTMENTS_CHOICES,default=1)
    faculty = models.CharField(verbose_name="院系",max_length=32)
    LEVEL_CHOICES = (
        (1,"普通教师"),
        (2,"优秀教师"),
        (3,"特级教师"),
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=LEVEL_CHOICES,default=1)
    phone_number = models.CharField(
        max_length=11, validators=[MOBILE_REGEX], unique=True, verbose_name="手机号"
    )
    usertype = models.SmallIntegerField(verbose_name="类型",default=2)
    
    def __str__(self):
        return self.name


class student(models.Model):  
    """学生表"""
    name = models.CharField(verbose_name="姓名",max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    GENDER_CHOICES = (
        (1,"男"),
        (2,"女")
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=GENDER_CHOICES,default=1)
    password = models.CharField(verbose_name="密码",max_length=64)
    grade = models.IntegerField(verbose_name="年级")
    classes = models.CharField(verbose_name="班级",max_length=32)
    major = models.CharField(verbose_name="专业",max_length=32)
    studentid = models.IntegerField(verbose_name="学号")
    faculty = models.CharField(verbose_name="院系",max_length=32)
    address = models.CharField(verbose_name="住址",max_length=128)
    phone_number = models.CharField(
        max_length=11, validators=[MOBILE_REGEX], unique=True, verbose_name="手机号"
    )
    img = models.FileField(verbose_name="头像", max_length=128,upload_to="StudentTx")
    usertype = models.SmallIntegerField(verbose_name="类型",default=3)
    
    def __str__(self):
        return self.name
