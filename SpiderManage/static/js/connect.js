
$(function () {
       $("#host_list").find("tr").each(function(){
        var tdArr = $(this).children('td');
        var ip_address = tdArr.eq(3).text();//ip地址
        var port_num = tdArr.eq(4).text();//端口号
        tdArr.eq(0).text('连接中...');

        var host_cnt = ip_address + ':' + port_num

        // $.ajax({
        //     url:'http://' + host_cnt + '/daemonstatus.json',
        //     success:function (data) {
        //        var run_status = data.running;
        //        if (run_status == 0){
        //            tdArr.eq(0).text('正在运行');
        //        }else {
        //            tdArr.eq(0).text('未运行');
        //        }
        //     },
        //     'error':function () {
        //         tdArr.eq(0).text('未连接');
        //     }
        // });

           zlajax.post({
            'url': '/daemonstatus/',
            'data':{
                        'ip_address': ip_address,
                        'port_num' : port_num
                    },
            'success': function (data) {
               if (data['code']==200){
                   tdArr.eq(0).text('正在运行');
               }else {
                   tdArr.eq(0).text('未运行');
                   }
            },
            'error': function () {
                    tdArr.eq(0).text('未连接');
            }

        });
    });
});


