function myAlert(msg, tag = 'danger') {
    msglabel = 'Error'
    if (tag == 'success') msglabel = 'Success'
    html = '<div class="alert alert-' + tag + ' alert-dismissible fade show" style="width: 20%;position: fixed; right: 10px; top: 110px;">'
    html += '<button type="button" class="close" data-dismiss="alert">&times;</button>'
    html += '<strong>' + msglabel + ': </strong> ' + msg
    html += '</div>'

    $('body:first').prepend(html)
    setTimeout(removeAllAlert, 3000)
}

function removeAllAlert() {
    $('.alert>button').click()
}

function sel_upload_data_type(label) {
    $('#sel_upload_data_type_btn').html(label)
}

function upload() {
    // Check input
    if ($("#result").val() == '') {
        alert("Input data is not valid!")
        return false
    }

    // Toggle
    $("#upload_btn>span").removeClass("hide")
    $("#result-div").removeClass("hide")
    $("#query-div").addClass("hide")

    $.post("/upload_salesforce_data", {
        "data": $("#result").val(),
        "type": $('#sel_upload_data_type_btn').html().replaceAll("\n", "").trim(),
    },
    function(data, status) {
        console.log(status, data)
        if (data.errorMessage) {
            $("#result").val('Failed to upload salesforce data.\n\n' + data.errorMessage)
        } else {
            $("#result").val(JSON.stringify(data, null, 8).replace('null', '""'));
        }
        $("#upload_btn>span").addClass("hide")
    }).fail(function(data) {
        if (data.responseText)
            $("#result").val('Failed to upload salesforce data!\n\n' + data.responseText)
        else
        $("#result").val('Failed to upload salesforce data!')
        $("#upload_btn>span").addClass("hide")
    })
}

function uploadDlg() {
    // Toggle
    $("#result").html("")
    $("#query-div").addClass("hide")
    $("#view_button").addClass("hide")
    $("#upload_dlg_button").addClass("hide")
    $("#result-div").removeClass("hide")
    $("#upload_btn").removeClass("hide")
    $("#view_dlg_button").removeClass("hide")
    $("#date1").addClass("hide")
    $("#date2").addClass("hide")
}

function back() {
    // Toggle
    $("#result-div").addClass("hide")
    $("#upload_btn").addClass("hide")
    $("#view_dlg_button").addClass("hide")
    $("#query-div").removeClass("hide")
    $("#view_button").removeClass("hide")
    $("#upload_dlg_button").removeClass("hide")
    $("#date1").removeClass("hide")
    $("#date2").removeClass("hide")
}

function view() {
    $('#view_button>span').removeClass('hide')

    $.post("/view_salesforce_data", {
        "date1": $("#date1").val(),
        "date2": $("#date2").val(),
        "type": $('#sel_upload_data_type_btn').html().replaceAll("\n", "").trim(),
    },
    function(data, status) {
        console.log(status, data)
        if (data.errorMessage) {
            alert('Failed to load salesforce data.\n\n' + data.errorMessage)
            clean_table()
        } else {
            if (data && 'records' in data && data.records.length) {
                h = ""
                t = "<th>No</th>"
                for (i = 0; i < data.records.length; i++) {
                    h += "<tr><td>"+(1+i)+"</td>"
                    for (let key in data.records[i]) {
                        if (key != 'attributes') {
                            if (i == 0) 
                                t += "<th>" + key + "</th>"
                            h += "<td>" + data.records[i][key] + "</td>"
                        }
                    }
                    h += "</tr>"
                }
                $('thead').html(t)
                $('tbody').html(h)
                show_table()
            } else {
                clean_table()
            }

            if (data && 'done' in data && 'totalSize' in data) {
                if (data.done == true) {
                    myAlert(data.totalSize + ' records are loaded.', 'success')
                } else {
                    $('#view_button>span').removeClass('hide')
                    load_extra(data.nextRecordsUrl)
                }
            }
        }
    }).fail(function(data) {
        if (data.responseText)
            alert('Failed to load salesforce data!\n\n' + data.responseText)
        else
            alert('Failed to load salesforce data!')
        clean_table()
    })
}

function load_extra(nextRecordsUrl) {
    $.post("/load_extra", {
        "nextRecordsUrl": nextRecordsUrl,
    },
    function(data, status) {
        console.log(status, data)
        if (data.errorMessage) {
            alert('Failed to load salesforce data.\n\n' + data.errorMessage)
            $('#view_button>span').addClass('hide')
        } else {
            if (data && 'records' in data && data.records.length) {
                h = ""
                for (i = 0; i < data.records.length; i++) {
                    h += "<tr><td>"+(1+i)+"</td>"
                    for (let key in data.records[i]) {
                        if (key != 'attributes') {
                            h += "<td>" + data.records[i][key] + "</td>"
                        }
                    }
                    h += "</tr>"
                }
                $('tbody').append(h)
            }

            if (data && 'done' in data && 'totalSize' in data) {
                if (data.done == true) {
                    myAlert(data.totalSize + ' records are loaded.', 'success')
                    show_table()
                } else
                    load_extra(data.nextRecordsUrl)
            }
        }
    }).fail(function(data) {
        if (data.responseText)
            alert('Failed to load salesforce data!\n\n' + data.responseText)
        else
            alert('Failed to load salesforce data!')
        $('#view_button>span').addClass('hide')
    })
}

function clean_table() {
    $('table').addClass('hide')
    $('#view_button>span').addClass('hide')
}

function show_table() {
    $('table').removeClass('hide')
    $('#view_button>span').addClass('hide')
}

function createDlg() {
    $("#name").val('')
    $("#fields").val('')
    $('.field-div:not(.last-field)').remove()
    $("#createModal").modal('show')
}

function createObj() {
    // Check input
    if ($("#name").val() == '') {
        alert("Input name.")
        $("#name").focus()
        return false
    }

    if ($(".field-div input:not(:placeholder-shown)").length == 0) {
        alert("Input field name.")
        $("input:placeholder-shown").focus()
        return false
    }

    var fields = []
    var objs = $('.field-div')
    for (let i = 0; i < objs.length; i++) {
        var n = $(objs[i]).find('input:eq(0)').val().trim()
        if (n.length == 0)
            continue

        var t = $(objs[i]).find('button:eq(0)').html().trim()
        if (t == 'Text') {
            fields.push({
                'fullName': n + '__c',
                'label': n,
                'type': 'Text',
                'length': 255
            })
        } else {
            fields.push({
                'fullName': n + '__c',
                'label': $(objs[i]).find('button:eq(1)').html().trim(),
                'type': 'TextArea',
            })
        }
    }

    $.post("/create_custom_obj", {
        "name": $("#name").val(),
        "fields": JSON.stringify(fields),
    },
    function(data, status) {
        console.log(status, data)
        if (data != 'OK') {
            myAlert('Failed to create a custom object.\n\n' + data)
        } else {
            $("#createModal").modal('hide')
            myAlert('Created successfully!', 'success')
        }
    }).fail(function(data) {
        if (data.responseText)
            $("#result").val('Failed to create a custom object!\n\n' + data.responseText)
        else
            $("#result").val('Failed to create a custom object!')
    })
}

function select_pparent_label(el, label) {
    if (label == 'Text')
        $(el).parent().parent().next().hide()
    else if (label == 'Lookup')
        $(el).parent().parent().next().show()
    $(el).parent().parent().find('button:first').html(label)
}

function onchange_field_name(el) {

    if (!$(el).parent().hasClass('last-field'))
        return
    
    var par = $(el).parent().parent()
    var obj = $(el).parent().clone()
    obj.find('input').val('')
    select_pparent_label(obj.find('button:first'), 'Text')
    obj.find('button:eq(1)').parent().hide()
    $("*").removeClass('last-field')
    par.append(obj)
}

function remove_field_div(el) {
    var el1 = $(el).parent().parent()
    if (!el1.hasClass('last-field'))
        el1.remove()
    else {
        el.parent().prev().val('')
    }
}

$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});