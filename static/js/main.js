/// <reference path="C:/Users/Derek.S/AppData/Roaming/npm/node_modules/@types/jquery/index.d.ts" />
$(document).ready(
    function () {

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            }
        })


        /* init Search Select */
        $('#Search_S').selectpicker({
            style: 'btn-primary',
            size: 4
        });
    }
)

function systemOptionLayer() {
    var url = Flask.url_for("sysOption.systemOption")
    layer_sysOpt = layer.open(
        {
            type: 2,
            skin: 'layui-layer-rim',
            title: "系统设置",
            area: ['500px', '300px'],
            content: url
        }
    )
}

function saveOption() {
    var url = Flask.url_for("sysOption.systemOption")
    limitNum = $("#limitInput").val()
    data = {
        "limitNum": limitNum
    }
    $.ajax({
        url: url,
        type: "post",
        data: JSON.stringify(data),
        datatype: "json",
        contentType: "application/json",
        success: function(resp){
            resp = JSON.parse(resp)
            if(resp.status == 1){
                alert("修改成功")
                parent.layer.closeAll()
            }else{
                alert("修改失败")
            }
        }
    })
}