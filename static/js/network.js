function _ajaxSetup(csrf_token) {
    $.ajaxSetup({
        'beforeSend': function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                var csrftoken = csrf_token;
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    });
}


$.deleteJSON = function (url, data, csrf_token, callback) {
    _ajaxSetup(csrf_token);
    $.ajax({
        url: url,
        type: "delete",
        contentType: "application/x-www-form-urlencoded",
        data: data,
        success: function (data, status) {
            callback(data, status);
        }
    });
};

$.putJSON = function (url, data, csrf_token, callback) {
    _ajaxSetup(csrf_token);
    $.ajax({
        url: url,
        type: "put",
        contentType: "application/json",
        dataType: "json",
        data: data,
        timeout: 20000,
        success: function (data, status) {
            callback(data, status);
        },
        error: function (xhr, textstatus, thrown) {

        }
    });
};

$.postJSON = function (url, data, csrf_token, callback) {
    _ajaxSetup(csrf_token);
    $.ajax({
        url: url,
        type: "post",
        contentType: "application/json",
        dataType: "json",
        data: data,
        timeout: 60000,
        success: function (data, status) {
            callback(data, status);
        },
        error: function (xhr, textstatus, thrown) {

        }
    });
};

$.getJSON = function (url, data, callback) {
    $.ajax({
        url: url,
        type: "get",
        contentType: "application/json",
        dataType: "json",
        timeout: 10000,
        data: data,
        success: function (data, status) {
            callback(data, status);
        }
    });
};

