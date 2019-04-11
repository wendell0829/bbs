$(function () {
    $('#img-captcha-img').click(function (event) {
        event.preventDefault();
        var img = $(this);
        var src = img.attr("src");
        var src_new = param.setParam(src, "cnumber", Math.random());
        img.attr("src", src_new)
    });
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var mobile_input = $("input[name='mobile']");
        var password_input = $("input[name='password']");
        var remember_input = $("input[name='remember']");
        var img_captcha_input = $("input[name='img_captcha']");

        var mobile = mobile_input.val();
        var password = password_input.val();
        var remember = remember_input.val();
        var img_captcha = img_captcha_input.val();

        csrf_ajax.post({
            'url': '/signin/',
            'data': {
                'mobile': mobile,
                'password': password,
                'remember': remember,
                'img_captcha': img_captcha
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    var msg = data['message'] + '即将跳转到您之前浏览的界面';
                    var return_to = $("#return-to").text();
                    if(return_to){
                        myalert.alertSuccess(msg, function (isconfirm) {
                            if (isconfirm) {
                                location.href = return_to
                            } else {
                                location.href = '/'
                            }
                        })
                    }else{
                        location.href = '/'
                    }

                } else {
                    myalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                myalert.alertNetworkError()
            }
        })
    })
})

