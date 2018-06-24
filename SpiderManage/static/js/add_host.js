
$(function () {
    $("#save-banner-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        var host_nameE = $("input[name=host_name]");
        var ip_addressE = $("input[name=ip_address]");
        var port_numE = $("input[name=port_num]");


        var host_name = host_nameE.val();
        var ip_address = ip_addressE.val();
        var port_num = port_numE.val();
        var submitType = self.attr('data-type');
        var host_id = self.attr("host-id");

        if(!host_name || !ip_address || !port_num ){
            zlalert.alertInfoToast('请输入完整的主机数据！');
            return;
        }
        var url = '';
        if(submitType == 'update'){
            url = '/pupdate/';
        }else{
            url = '/pcreate/';
        }

        zlajax.post({
            "url": url,
            'data':{
                'host_name':host_name,
                'ip_address': ip_address,
                'port_num': port_num,
                'host_id': host_id
            },
            'success': function (data) {
                dialog.modal("hide");
                if(data['code'] == 200){
                    // 重新加载这个页面
                    window.location.reload();
                }else{
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                zlalert.alertNetworkError();
            }
        });
    });
});


$(function () {
    $("button[name='update']").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal("show");
        var tr = self.parent().parent();

        var host_id = tr.attr('host-id');
        var host_name = tr.attr('host-name');
        var ip_address = tr.attr('ip-address');
        var port_num = tr.attr('port-num');

        var host_nameE = dialog.find("input[name='host_name']");
        var ip_addressE = dialog.find("input[name='ip_address']");
        var port_numE = dialog.find("input[name='port_num']");
        var saveBtn = dialog.find("#save-banner-btn");

        host_nameE.val(host_name);
        ip_addressE.val(ip_address);
        port_numE.val(port_num);
        saveBtn.attr("data-type",'update');
        saveBtn.attr('host-id',tr.attr('host-id'));

    });
});



