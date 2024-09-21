from django.urls import path
from . import views

app_name = "student"

urlpatterns = [
    path("info/",views.student_info),
    path("logout/",views.logout),
    path("<int:uid>/edit/",views.student_edit),
]