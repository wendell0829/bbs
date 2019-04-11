$(function () {
    $("#test-btn").click(function (event) {
        event.preventDefault();
        //
        swal({
            title: '注意！',
            text: '确定要删除吗？',
            type: 'warning',
            showCancelButton: true,
            closeOnConfirm: false
        }, function (isConfirm) {
            if (isConfirm) {
                swal({
                    title: '成功',
                    text: '删除成功',
                    type: 'success'
                }, function () {
                        window.location.reload();
                        alert('重新加载完毕！')
                })
            }
        })
        // swal(
        //     {
        //         title: "您确定要删除这条数据吗",
        //         text: "删除后将无法恢复，请谨慎操作！",
        //         type: "warning",
        //         showCancelButton: true,
        //         closeOnConfirm: false,
        //     }, function (isConfirm) {
        //         if (isConfirm) {
        //             swal({
        //                 title: "删除成功！",
        //                 text: "您已经永久删除了这条数据。",
        //                 type: "success"
        //             }, function () {
        //                 window.location .reload()
        //             })
        //         }
        //     }
        // )
    })
})





