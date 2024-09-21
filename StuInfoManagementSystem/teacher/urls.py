from django.urls import path,include
from . import views

app_name = "teacher"

urlpatterns = [
    path("index/",views.teacher_index),
    path("info/",views.teacher_info),
    
    path("student/<int:uid>/info/", views.student_info),
    path("student/add/", views.student_add),
    path("student/delete/", views.student_delete),
    path("student/<int:uid>/edit/", views.student_edit),
]