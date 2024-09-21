from django.urls import path,include
from . import views

app_name = "manager"

urlpatterns = [
    # 教师模块
    path("index/",views.manager_index,name="index"),
    path("teacher/<int:uid>/info/",views.teacher_info),
    path("teacher/add/",views.teacher_add),
    path("teacher/<int:uid>/edit/",views.teacher_edit),
    path("teacher/delete/",views.teacher_delete),
    
    # 登录模块
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("image/code/", views.image_code, name="image_code"),
    
    # 学生模块
    path("student/index/", views.manager_student_index, name="学生信息主页"),
    path("student/<int:uid>/info/", views.student_info),
    path("student/add/", views.student_add),
    path("student/delete/", views.student_delete),
    path("student/<int:uid>/edit/", views.student_edit),
    
    
]