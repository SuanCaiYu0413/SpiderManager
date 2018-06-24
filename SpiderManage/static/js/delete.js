$(function () {
    $("button[name='delete']").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var host_id = tr.attr('host-id');
        zlalert.alertConfirm({
            "msg":"您确定要删除这个主机吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/pdelete/',
                    'data':{
                        'host_id': host_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            zlalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});