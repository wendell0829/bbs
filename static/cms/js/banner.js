$(function () {
    $("#save_btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var submit_type = self.attr('data-type');
        var banner_id = self.attr('data-id');
        var name_input = $("input[name=name]");
        var img_url_input = $("input[name=img_url]");
        var link_url_input = $("input[name=link_url]");
        var priority_input = $("input[name=priority]");

        var name = name_input.val();
        var img_url = img_url_input.val();
        var link_url = link_url_input.val();
        var priority = priority_input.val();

        var url = '/cms/add_banner/';
        if (submit_type === 'update') {
            url = '/cms/update_banner/'
        }
        csrf_ajax.post({
            'url': url,
            'data': {
                'banner_id': banner_id,
                'name': name,
                'img_url': img_url,
                'link_url': link_url,
                'priority': priority
            },
            'success': function (data) {
                msg = data['message'];
                if (data['code'] === 200) {
                    myalert.alertSuccess(msg, function (isconfirm) {
                        if (isconfirm) {
                            window.location.reload()
                        }
                    })
                } else {
                    myalert.alertInfoToast(msg)
                }
            },
            'fail': function () {
                myalert.alertNetworkError()
            }
        })
    });

    $(".delete-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr("data-id");

        myalert.alertConfirm({
                'msg': '确定删除此轮播图吗？',
                'confirmCallback': function () {
                    csrf_ajax.post({
                        'url': '/cms/delete_banner/',
                        'data': {
                            'banner_id': banner_id
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
                }
            }
        )
    })
});
$(function () {
    $(".edit-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#BannerModal");

        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var img_url = tr.attr("data-img_url");
        var link_url = tr.attr("data-link_url");
        var priority = tr.attr("data-priority");

        var nameInput = dialog.find("input[name='name']");
        var imgInput = dialog.find("input[name='img_url']");
        var linkInput = dialog.find("input[name='link_url']");
        var priorityInput = dialog.find("input[name='priority']");
        var saveBtn = dialog.find("#save_btn");

        nameInput.val(name);
        imgInput.val(img_url);
        linkInput.val(link_url);
        priorityInput.val(priority);
        saveBtn.attr("data-type", 'update');
        saveBtn.attr('data-id', tr.attr('data-id'));
    });
});

$(function () {
    myqiniu.setUp({
        'domain': 'http://podxcwazy.bkt.clouddn.com/',
        'browse_btn': 'img-upload-btn',
        'uptoken_url': '/common/uptoken/',
        'success': function (up, file, info) {
            var image_url = file.name;
            var img_url_input = $("input[name=img_url]");
            img_url_input.val(image_url);
        }
    })
});



