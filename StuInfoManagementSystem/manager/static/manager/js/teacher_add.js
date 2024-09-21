$(function () {
    binBtnAddEvent();
    binBtnSaveEvent();
    binBtnDeleteEvent();
    binBtnConfirmDeleteEvent();
    binBtnEditEvent();
    binBtnCloseEvent();
})

function binBtnAddEvent() {
    $("#btnAdd").click(function () {
        EditID = undefined;

        // 新建对话框
        $("#myModalLabel").text("添加教师");
        $('#myModal').modal('show');
        $("#formAdd").reset();
    })
}


function binBtnSaveEvent() {
    $("#btnSave").click(function () {
        // 清除错误信息
        $(".error-msg").empty();
        // 后台发送请求

        if (EditID) {
            doEdit();
        } else {
            doAdd();
        }

        function doEdit() {
            $.ajax({
                url: "/manager/order/edit/" + "?oid=" + EditID,  // 请求页面
                type: "post",
                data: $("#formAdd").serialize(),
                dataType: "JSON",
                success: function (res) {
                    if (res.status) {
                        alert("操作成功");
                        $("#formAdd")[0].reset();  //清空表单
                        $('#myModal').modal('hide');  // 关闭模态框
                        location.reload();  //刷新页面
                    } else {
                        if (res.tips) {
                            alert(res.tips)
                        } else {
                            $.each(res.error, function (name, errorList) {
                                $("#id_" + name).next().text(errorList[0]);  // 输出错误信息并显示
                            });
                        }
                    }
                }
            })
        }

        function doAdd() {
            $.ajax({
                url: "/manager/teacher/add/",  // 请求页面
                type: "post",
                data: $("#formAdd").serialize(),
                dataType: "JSON",
                success: function (res) {
                    if (res.status) {
                        alert("操作成功");
                        $("#formAdd")[0].reset();  //清空表单
                        $('#myModal').modal('hide');  // 关闭模态框
                        location.reload();  //刷新页面
                    } else {
                        console.log(res.error);
                        $.each(res.error, function (name, errorList) {
                            $("#id_" + name).next().text(errorList[0]);  // 输出错误信息并显示
                        });
                    }
                }
            })
        }
    })
}

let DELETE_ID;

function binBtnDeleteEvent() {
    $(".btn-delete").click(function () {
        $('#deleteModal').modal('show');

        DELETE_ID = $(this).attr("data-uid");
    });
}

function binBtnConfirmDeleteEvent() {
    $("#btnConfirmDelete").click(function () {
        $.ajax({
            url: "/manager/order/delete/",
            type: "GET",
            data: {
                oid: DELETE_ID
            },
            dataType: "JSON",
            success: function (res) {
                if (res.status) {
                    alert("删除成功")
                    location.reload();  //刷新页面
                } else {
                    // 删除失败
                    alert(res.error)
                }
            }
        })
    })
}

let EditID;

function binBtnEditEvent() {
    $(".btn-edit").click(function () {
        $("#formAdd")[0].reset();
        EditID = $(this).attr("data-uid");
        $.ajax({
            url: "/manager/order/detail/",
            type: "get",
            data: {
                oid: EditID
            },
            dataType: "JSON",
            success: function (res) {
                if (res.status) {
                    $.each(res.data, function (name, value) {
                        $("#id_" + name).val(value);
                    });
                    $("#myModalLabel").text("编辑订单");
                    $('#myModal').modal('show');
                } else {
                    alert(res.error)
                }
            }
        })
    })
}

function binBtnCloseEvent() {
    $(".btn-close").click(function () {
        $("#formAdd")[0].reset();
        EditID = undefined;
    })
}




