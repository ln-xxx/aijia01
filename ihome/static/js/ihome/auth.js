
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    console.log('进入登陆验证....');
//处理表单添加提交事件
    $('#form-auth').submit(function (e) {
        e.preventDefault(); //阻止表单默认的提交行为
//1. 找数据
        realname = $('#real-name').val();
        idcard = $('#id-card').val();
        console.log('姓名' + realname + '身份证:' + idcard);
// //3. 做ajax
        $.ajax({
            url: '/api/v1.0/auth',
            type: 'POST',
            data: {'real_name': realname, 'id_card': idcard},
            dataType: 'json',
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (res) {
                console.log(res);
                if (res.errno == '0') {
                    alert('完成')
                    // location.href = 'index.html' //js跳转
                    // location.href = 'auth.html' //js跳转
                } else {
                    alert('错误')
                    // console.log('错误');
                    // console.log(res);
                    // $('#password-err span').html(res.errmsg);
                    // $('#password-err').show()
                }
            }
        })
    })
})


