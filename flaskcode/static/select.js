
$(function () {
    $("#search").click(function (event) {
        event.preventDefault();
        var select_key = $("input[name='select']").val();
        if(!select_key){
            alert('请输入关键词! ')
            return;
        }
        $.ajax({
            type:'get',
            url: '/select/',
            data: {'select_key':select_key},
            success:function (data) {
                alert(data.result);
            }
        });
    });
});