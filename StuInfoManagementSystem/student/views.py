from django.shortcuts import render
from teacher.views import *


def student_info(request):
    """学生详情"""
    id = request.session["info"]["id"]
    obj = models.student.objects.get(id=id)  # 返回查询信息
    return render(request, "student/student_info.html", {"obj": obj})

def student_edit(request, uid):
    """学生信息修改"""
    row_object = models.student.objects.filter(
        studentid=uid
    ).first()  # 获取请求的数据的值
    if request.method == "GET":  # 默认响应页面
        form = StudentAddForm(instance=row_object)
        return render(request, "student/student_edit.html", {"form": form})
    form = StudentAddForm(data=request.POST, files=request.FILES, instance=row_object)
    if form.is_valid():  # 如果数据合法就保存
        form.save()  # 更新数据
        return redirect("/student/info/")  # 返回列表页面
    return render(
        request, "student/student_edit.html", {"form": form}
    )  # 提交数据不合法返回默认页面

def logout(request):
    """用户注销"""
    request.session.clear()

    return redirect("/manager/login/")
