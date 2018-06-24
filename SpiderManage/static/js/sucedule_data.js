$(function () {
        $("button[name='control']").click(function (event) {
            var self = $(this);
            var tr = self.parent().parent();
            var host_id = tr.attr('host-id');

            window.location.href="/psucedule/" + host_id
        });
    });
