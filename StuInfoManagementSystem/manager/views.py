from . import models
from io import BytesIO
from .utils.encrypt import md5
from .utils.image_code import check_code
from django import forms
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts import HttpResponse, render, redirect


def manager_index(request):
    """教师列表"""
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["uid__contains"] = search_data

    obj_list = models.teacher.objects.filter(**data_dict).order_by(
        "-level"
    )  # 返回数据库信息
    return render(request, "manager/manager_index.html", {"obj_list": obj_list})


def teacher_info(request, uid):
    """教师详情"""
    obj = models.teacher.objects.get(uid=uid)  # 返回查询信息
    return render(request, "manager/manager_teacher_info.html", {"obj": obj})


widgets = {
    "password": forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "请输入密码"}
    )
}  # 定制密码所需类型和样式类


class TeacherAddForm(forms.ModelForm):
    """教师信息管理模块"""

    confirm_password = forms.CharField(
        label="确认密码", widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.teacher
        fields = [
            "name",
            "gender",
            "age",
            "faculty",
            "uid",
            "level",
            "create_time",
            "salary",
            "password",
            "confirm_password",
            "phone_number",
        ]  # 获取所需数据
        widgets = widgets

    def __init__(
        self, *args, **kwargs
    ):  # 覆写方法并用 for 循环为每个数据添加默认参数和所需的样式类
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "password":  # 跳过密码型
                continue
            if name == "img":
                continue
            field.widget.attrs = {
                "class": "form-control",
                "placeholder": "请输入" + field.label,
            }

    def clean_password(self):  # 用md5加密密码
        password = self.cleaned_data.get("password")
        md5_password = md5(password)

        exists = models.teacher.objects.filter(
            id=self.instance.pk, password=md5_password
        ).exists()
        if exists:
            raise ValidationError("不能与之前密码相同！")

        return md5_password

    def clean_confirm_password(self):  # 利用钩子方法验证密码
        pwd = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if confirm_password != pwd:
            raise ValidationError("密码不一致，请重新输入！")
        return confirm_password


def teacher_add(request):
    """教师添加"""
    if request.method == "GET":  # 设置默认响应页面
        form = TeacherAddForm()
        return render(request, "manager/manager_teacher_add.html", {"form": form})

    form = TeacherAddForm(data=request.POST)  # 获取web端提交的数据
    if form.is_valid():  # 如果数据合法就保存
        form.save()
        return redirect("/manager/index/")

    return render(
        request, "manager/manager_teacher_add.html", {"form": form}
    )  # 提交数据不合法返回默认页面


def teacher_edit(request, uid):
    """教师信息修改"""
    row_object = models.teacher.objects.filter(uid=uid).first()  # 获取请求的数据的值
    if request.method == "GET":  # 默认响应页面
        form = TeacherAddForm(instance=row_object)
        return render(request, "manager/manager_teacher_edit.html", {"form": form})
    form = TeacherAddForm(data=request.POST, instance=row_object)
    if form.is_valid():  # 如果数据合法就保存
        form.save()  # 更新数据
        return redirect("/manager/index/")  # 返回列表页面
    return render(
        request, "manager/manager_teacher_edit.html", {"form": form}
    )  # 提交数据不合法返回默认页面


def teacher_delete(request):
    """删除教师"""
    uid = request.GET.get("uid")
    print(uid)
    if not models.teacher.objects.filter(uid=uid).exists():
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})

    models.teacher.objects.filter(uid=uid).delete()
    return JsonResponse({"status": True})


class LoginForm(forms.Form):
    """登录表单"""

    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入用户名"}
        ),
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "请输入密码"},
            render_value=True,
        ),
        required=True,
    )
    user_choose = ((1, "管理员"), (2, "教师"), (3, "学生"))
    usertype = forms.ChoiceField(
        choices=user_choose,
        label="登录角色",
        widget=forms.Select(
            attrs={"class": "form-control"},
        ),
        required=True,
    )
    image_code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "请输入验证码"}
        ),
        required=True,
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")

        return md5(password)


def login(request):
    """用户登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "manager/login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():

        user_image_code = form.cleaned_data.pop("image_code")
        image_code = request.session.get("image_code", "")

        if user_image_code.upper() != image_code.upper():  # 校验验证码
            form.add_error("image_code", "验证码错误！")
            return render(request, "manager/login.html", {"form": form})

        print(form.cleaned_data)
        if form.cleaned_data["usertype"] == "1":
            admin_object = models.manager.objects.filter(**form.cleaned_data).first()
        elif form.cleaned_data["usertype"] == "2":
            admin_object = models.teacher.objects.filter(**form.cleaned_data).first()
        elif form.cleaned_data["usertype"] == "3":
            admin_object = models.student.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "manager/login.html", {"form": form})

        request.session["info"] = {
            "id": admin_object.id,
            "username": admin_object.name,
        }
        request.session.set_expiry(60 * 60 * 24 * 7)  # 登录数据存七天，即七天免登录
        if form.cleaned_data["usertype"] == "1":
            return redirect("/manager/index")
        if form.cleaned_data["usertype"] == "2":
            return redirect("/teacher/index")
        if form.cleaned_data["usertype"] == "3":
            return redirect("/student/info")

    return render(request, "manager/login.html", {"form": form})


def logout(request):
    """用户注销"""
    request.session.clear()

    return redirect("/manager/login/")


def image_code(request):
    """生成图片验证码"""

    img, code_string = check_code()

    request.session["image_code"] = code_string  # 将验证码写入session中
    request.session.set_expiry(60)  # 给session设置60秒超时

    stream = BytesIO()
    img.save(stream, "png")
    return HttpResponse(stream.getvalue())


def manager_student_index(request):
    """学生列表"""
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["studentid__contains"] = search_data

    obj_list = models.student.objects.filter(**data_dict).order_by(
        "-grade"
    )  # 返回数据库信息
    return render(request, "manager/manager_student_index.html", {"obj_list": obj_list})


def student_info(request, uid):
    """学生详情"""
    obj = models.student.objects.get(studentid=uid)  # 返回查询信息
    return render(request, "manager/manager_student_info.html", {"obj": obj})


widgets = {
    "password": forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "请输入密码"}
    )
}  # 定制密码所需类型和样式类


class StudentAddForm(forms.ModelForm):
    """学生信息管理模块"""

    confirm_password = forms.CharField(
        label="确认密码", widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.student
        # exclude = ["id"]
        fields = [
            "name",
            "studentid",
            "gender",
            "age",
            "grade",
            "classes",
            "faculty",
            "major",
            "address",
            "password",
            "phone_number",
            "confirm_password",
            "img",
        ]  # 获取所需数据
        widgets = widgets

    def __init__(
        self, *args, **kwargs
    ):  # 覆写方法并用 for 循环为每个数据添加默认参数和所需的样式类
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "password":  # 跳过密码型
                continue
            if name == "img":
                continue
            field.widget.attrs = {
                "class": "form-control",
                "placeholder": "请输入" + field.label,
            }

    def clean_password(self):  # 用md5加密密码
        password = self.cleaned_data.get("password")
        md5_password = md5(password)

        exists = models.student.objects.filter(
            id=self.instance.pk, password=md5_password
        ).exists()
        if exists:
            raise ValidationError("不能与之前密码相同！")

        return md5_password

    def clean_confirm_password(self):  # 利用钩子方法验证密码
        pwd = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if confirm_password != pwd:
            raise ValidationError("密码不一致，请重新输入！")
        return confirm_password


def student_add(request):
    """学生添加"""
    if request.method == "GET":  # 设置默认响应页面
        form = StudentAddForm()
        return render(request, "manager/manager_student_add.html", {"form": form})

    form = StudentAddForm(data=request.POST, files=request.FILES)  # 获取web端提交的数据
    if form.is_valid():  # 如果数据合法就保存
        form.save()
        return redirect("/manager/student/index/")

    return render(
        request, "manager/manager_student_add.html", {"form": form}
    )  # 提交数据不合法返回默认页面


def student_edit(request, uid):
    """学生信息修改"""
    row_object = models.student.objects.filter(
        studentid=uid
    ).first()  # 获取请求的数据的值
    if request.method == "GET":  # 默认响应页面
        form = StudentAddForm(instance=row_object)
        return render(request, "manager/manager_student_edit.html", {"form": form})
    form = StudentAddForm(data=request.POST, files=request.FILES, instance=row_object)
    if form.is_valid():  # 如果数据合法就保存
        form.save()  # 更新数据
        return redirect("/manager/student/index/")  # 返回列表页面
    return render(
        request, "manager/manager_student_edit.html", {"form": form}
    )  # 提交数据不合法返回默认页面


def student_delete(request):
    """删除学生"""
    uid = request.GET.get("uid")
    print(uid)
    if not models.student.objects.filter(studentid=uid).exists():
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})

    models.student.objects.filter(studentid=uid).delete()
    return JsonResponse({"status": True})
