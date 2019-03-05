/**
 * Created by hynev on 2017/11/25.
 */

$(function () {
    $("#get-captcha-btn").click(function (event) {
        event.preventDefault();

        var emailE = $("input[name=email]");
        var captchaE = $("input[name=captcha]");

        var email = emailE.val();

        if (!email) {
            myalert.alertInfoToast('请输入邮箱！');
            return;
        }

        csrf_ajax.get({
            'url': '/cms/captcha/',
            'data': {
                'email': email,
            },
            'success': function (data) {
                // code==200
                // code != 200
                var message = data['message'];
                if (data['code'] === 200) {
                    myalert.alertSuccessToast(message);
                    emailE.val(email);
                    captchaE.val("");
                } else {
                    myalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                myalert.alertNetworkError();
            }
        })

    });
    $("#submit").click(function (event) {
        // event.preventDefault
        // 是阻止按钮默认的提交表单的事件
        event.preventDefault();

        var emailE = $("input[name=email]");
        var captchaE = $("input[name=captcha]");

        var email = emailE.val();
        var captcha = captchaE.val();

        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken
        csrf_ajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha,
            },
            'success': function (data) {
                // code==200
                // code != 200
                var message = data['message'];
                if (data['code'] == 200) {
                    myalert.alertSuccessToast(message);
                    emailE.val("");
                    captchaE.val("");
                } else {
                    myalert.alertInfo(message);
                }
            },
            'fail': function (error) {
                myalert.alertNetworkError();
            }
        });
    });
});