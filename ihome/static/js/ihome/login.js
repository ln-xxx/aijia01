function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    console.log('进入登陆验证....');
    $("#mobile").focus(function () {
        $("#mobile-err").hide();
    });
    $("#password").focus(function () {
        $("#password-err").hide();
    });
//处理表单添加提交事件
    $('.form-login').submit(function (e) {
        e.preventDefault(); //阻止表单默认的提交行为
//1. 找数据
        mobile = $('#mobile').val();
        passwd = $('#password').val();
        console.log('手机' + mobile + '密码:' + passwd);
//2. 前端校验
        var reg_mobile = /^1[3456789]\d{9}$/;
//reg_mobile.test(reg_mobile)==false
        if (!mobile) {
            $('#mobile-err span').html('请输入正确手机号');
            $('#mobile-err').show();
            return;
        }
//密码强度
        var reg_pwd = /^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*?]).*$/;
        if (!passwd) {
            $('#password-err span').html('密码最少6位，包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符')
            $('#password-err').show();
            return;
        }
        // alert('做ajax');
//3. 做ajax
        $.ajax({
            url: '/api/v1.0/login',
            type: 'POST',
            data: {'mobile': mobile, 'password': passwd},
            dataType: 'json',
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (res) {
                console.log(res);
                if (res.errno == '0') {
                    location.href = 'index.html' //js跳转
                } else {
                    console.log('错误');
                    console.log(res);
                    $('#password-err span').html(res.errmsg);
                    $('#password-err').show()
                }
            }
        })
    })
})


