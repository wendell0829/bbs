$(function () {
    $("#save_btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var submit_type = self.attr('data-type');
        var board_id = self.attr('data-id');
        var name_input = $("input[name=name]");
        var moderator_email_input = $("input[name=moderator_email]");
        var desc_input = $("input[name=desc]");

        var name = name_input.val();
        var moderator_email = moderator_email_input.val();
        var desc = desc_input.val();

        var url = '/cms/add_board/';
        if (submit_type === 'update') {
            url = '/cms/update_board/'
        }
        csrf_ajax.post({
            'url': url,
            'data': {
                'board_id': board_id,
                'name': name,
                'moderator_email': moderator_email,
                'desc': desc,
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
        var board_id = tr.attr("data-id");

        myalert.alertConfirm({
                'msg': '确定删除此板块吗？',
                'confirmCallback': function () {
                    csrf_ajax.post({
                        'url': '/cms/delete_board/',
                        'data': {
                            'board_id': board_id
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
        var dialog = $("#BoardModal");

        dialog.modal("show");

        var tr = self.parent().parent();
        var name = tr.attr("data-name");
        var moderator_email = tr.attr("data-moderator-email");
        var desc = tr.attr("data-desc");

        var nameInput = dialog.find("input[name='name']");
        var moderator_emailInput = dialog.find("input[name='moderator_email']");
        var descInput = dialog.find("input[name='desc']");
        var saveBtn = dialog.find("#save_btn");

        nameInput.val(name);
        moderator_emailInput.val(moderator_email);
        descInput.val(desc);

        saveBtn.attr("data-type", 'update');
        saveBtn.attr('data-id', tr.attr('data-id'));
    });
});
