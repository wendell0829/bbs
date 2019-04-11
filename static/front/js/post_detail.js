
$(function () {
    var ue = UE.getEditor("editor",{
        'serverUrl': '/ueditor/upload/',
        "toolbars": [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'insertcode', //代码语言
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
            ]
        ]
    });
    window.ue = ue;
});

$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            window.location = '/signin/?onlogin=True';
        }else{
            var content = window.ue.getContent();
            var post_id = $("#post-content").attr("data-id");
            csrf_ajax.post({
                'url': '/add_comment/',
                'data':{
                    'content': content,
                    'post_id': post_id
                },
                'success': function (data) {
                    if(data['code'] === 200){
                        myalert.alertSuccess(msg=data['message'],
                            confirmCallback=function (isconfirm) {
                                if(isconfirm){
                                    window.location.reload()
                                }
                            } );
                    }else{
                        myalert.alertInfo(data['message']);
                    }
                }
            });
        }
    });

    $("#like-btn").click(function (event) {
        event.preventDefault();

        var self = $(this);
        var post_id = $("#post-content").attr("data-id");
        var to_do = '1';
        if(self.text().indexOf("已") >= 0){
            to_do = '0'
        }

        csrf_ajax.post({
            'url': '/like/',
            'data': {
                'post_id': post_id,
                'to_do': to_do
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    window.location.reload()
                } else {
                    myalert.alertInfoToast(data['message'])
                }
            },
            'fail': function () {
                myalert.alertNetworkError()
            }
        })
    })
});