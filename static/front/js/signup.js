$(function () {
    $('#img-captcha-img').click(function (event) {
        event.preventDefault();
        var img = $(this);
        var src = img.attr("src");
        var src_new = param.setParam(src, "cnumber", Math.random());
        img.attr("src", src_new)
    });
    $('#sms-captcha-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var mobile = $("input[name=mobile]").val();
        var patt = /^1[3-9]\d{9}/;
        if (patt.test(mobile)) {
            csrf_ajax.post({
                'url': '/common/sms_captcha/?mobile=' + mobile,
                'data': {
                    'mobile': mobile,
                },
                'success': function (data) {
                    // code==200
                    // code != 200
                    var message = data['message'];
                    if (data['code'] === 200) {
                        myalert.alertSuccessToast(message);
                        self.attr("disabled", "disabled");
                        var timecount = 60;
                        var timer = setInterval(function () {
                            timecount --;
                            self.text(timecount + 's');
                            if(timecount <= 0){
                                self.removeAttr("disabled");
                                self.text('重新发送')
                            }
                        }, 1000)
                    } else {
                        myalert.alertInfo(message);
                    }
                },
                'fail': function (error) {
                    myalert.alertNetworkError();
                }
            })
        }
        else {
            myalert.alertInfo('请填写正确格式的手机号码')
        }

    });

    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var mobile_input = $("input[name='mobile']");
        var sms_captcha_input = $("input[name='sms_captcha']");
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");
        var img_captcha_input = $("input[name='img_captcha']");

        var mobile = mobile_input.val();
        var sms_captcha = sms_captcha_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var img_captcha = img_captcha_input.val();

        csrf_ajax.post({
            'url': '/signup/',
            'data': {
                'mobile': mobile,
                'username': username,
                'password1': password1,
                'password2': password2,
                'sms_captcha': sms_captcha,
                'img_captcha': img_captcha
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    var msg = data['message'] + "即将跳转到登录页面";
                    var jump = function (isconfirm) {
                    if(isconfirm){
                        location.href = '/signin'
                    }else{
                        location.href = '/'
                    }
                };
                    myalert.alertSuccess(msg, jump);
                }
                else {
                    myalert.alertInfoToast(data['message'])
                }
            },
            'fail': function () {
                myalert.alertNetworkError()
            }
        })
    })
});
