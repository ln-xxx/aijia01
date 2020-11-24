function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function sendSMSCode() {
    // 点击发送短信验证码后被执行的函数
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    $.get("/api/v1.0/sms_conde/" + mobile)
}  // resp是后端返回的响应值，因为后端返回的是json字符串，

function generateImageCode() {
    //生成图片验证码的后端地址，设置到页面中，让浏览器请求验证码图片
    //1.生成图片验证码的编号
    //指定图片url
    var url = "/api/v1.0/img_conde"
    $(".image-code img").attr("src", url)
}

$(document).ready(function () {
    console.log('进入注册验证.');
    // $("#mobile").focus(function () {
    //     $("#mobile-err").hide();
    // });
    // $("#password").focus(function () {
    //     $("#password-err").hide();
    // });
//处理表单添加提交事件
    $('.form-register').submit(function (e) {
        e.preventDefault(); //阻止表单默认的提交行为
//1. 找数据
        mobile = $('#mobile').val();
        password = $('#password').val();
        password2 = $('#password2').val();
        console.log('手机' + mobile + '密码:' + password + '密码2:' + password2);


// //2. 前端校验
//         var reg_mobile = /^1[3456789]\d{9}$/;
// //reg_mobile.test(reg_mobile)==false
//         if (!mobile) {
//             $('#mobile-err span').html('请输入正确手机号');
//             $('#mobile-err').show();
//             return;
//         }
// //密码强度
//         var reg_pwd = /^.*(?=.{6,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*?]).*$/;
//         if (!passwd) {
//             $('#password-err span').html('密码最少6位，包括至少1个大写字母，1个小写字母，1个数字，1个特殊字符')
//             $('#password-err').show();
//             return;
//         }
//         // alert('做ajax');
//3. 做ajax
        $.ajax({
            url: '/api/v1.0/register',
            type: 'POST',
            data: {'mobile': mobile, 'password': password, 'password2': password2},
            dataType: 'json',
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (res) {
                console.log(res);
                if (res.errno == '0') {
                    location.href = 'login.html' //js跳转
                } else {
                    console.log('错误');
                    // console.log(res);
                    // $('#password-err span').html(res.errmsg);
                    // $('#password-err').show()
                }
            }
        })
    })
})


