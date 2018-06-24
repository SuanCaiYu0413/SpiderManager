
$(function () {
        var tbody = $("#host_list");
        var host_id = tbody.attr('host-id');

           zlajax.post({
            'url': '/lprojects/',
            'data':{'host_id': host_id},
            'success': function (data) {
                    var projects = data['data'][1];
                    var spider_list = data['data'][0]
                    if (projects){
                   			var htmTr="";
                            $(projects).each(function (index,item) {
				            htmTr+="<tr ><td>"+host_id+"</td><td>"+item+'</td><td><button id="fat-btn" class="btn btn-success btn-xs" data-loading-text="Loading..." type="button"> 启动</button></td><td></td></tr>'});
			$("#host_list").append(htmTr);
			
               }else {
                 var htmTr = "<tr ><td>"+host_id+"</td><td>"+'请求失败'+'</td><td></td></tr>';
                        $("#host_list").append(htmTr);
                   }
                if (spider_list){
                        $(spider_list).each(function (k,v) {
                            var finished_spiders = v['finished']
                            var html1="";
                            var html2="";

                            $(finished_spiders).each(function (k,v) {
                                var spider_name = v['spider']
                                var spider_id = v['id']
                                var start_time = v['start_time']
                                var end_time = v['end_time']
                                var infos = '我是第'+k+'个'

                                html1 += '<tr data-toggle="collapse"  data-target='+'#'+k+'><td>>>'+spider_name+'</td><td>'+spider_id+'</td><td>'+start_time+'</td><td>'+end_time+'</td></tr>'
                                html2 += '<div id='+k+' class="panel-collapse collapse"><div class="panel-body">'+infos+'</div></div>'

                            });
                            $("#spider_list").append(html1);
                            $("#collapse-text").append(html2);
                        })

                }else {
                    return '';
                }
            },
            'error': function () {
                    var htmTr = "<tr ><td>"+host_id+"</td><td>"+'暂无'+'</td><td></td></tr>';
                        $("#host_list").append(htmTr);
            }
        });
});
