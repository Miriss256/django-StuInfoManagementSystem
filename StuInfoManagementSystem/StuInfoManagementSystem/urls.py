"""StuInfoManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

# 启用media
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT},name='media'),
    
    path("admin/", admin.site.urls),
    
    path("student/",include("student.urls")),  # 学生模块
    
    path("teacher/",include("teacher.urls")),  # 教师模块
    
    path("manager/",include("manager.urls")),  # 管理员模块
    
]
