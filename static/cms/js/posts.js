$(function () {
    $(".delete-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr('data-id');

        swal({
            title: '注意！',
            text: '确定要删除吗？',
            type: 'warning',
            showCancelButton: true,
            closeOnConfirm: false
        }, function (isConfirm) {
            if (isConfirm) {
                csrf_ajax.post({
                    'url': '/cms/delete_post/',
                    'data': {
                        'post_id': post_id,
                    },
                    'success': function (data) {
                        if (data['code'] === 200) {
                            swal({
                                title: '成功',
                                text: '删除成功！',
                                type: 'success'
                            }, function () {
                                window.location.reload()
                            })
                        }
                    },
                    'fail': function () {
                        myalert.alertNetworkError()
                    }
                })
            }

        })
    });

    $(".stick-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr('data-id');
        var to_do = self.attr('data-to_do');

        csrf_ajax.post({
            'url': '/cms/stick_post/',
            'data': {
                'post_id': post_id,
                'to_do': to_do
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    myalert.alertSuccess(data['message'],
                        function () {
                            window.location.reload()
                        })
                } else {
                    myalert.alertInfoToast(data['message'])
                }
            },
            'fail': function () {
                myalert.alertNetworkError()
            }
        })
    });
})







