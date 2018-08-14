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

function isNull( str ){
    if ( str == "" ) return true
    var regu = "^[ ]+$"
    var re = new RegExp(regu)
    return re.test(str)
    }


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

function pCopy(domObj) {
    var base = $("table#provinces_table > tbody")
    var oLineFind = $(domObj).parents("tr.provinces_ntr")
    var oCopyLine = oLineFind.clone()
    base.append(oCopyLine) 
}

function pDel(domObj) {
    if($("tr.provinces_ntr").length === 1){
        alert("只有1行时不得删除")
    }else{
        $(domObj).parents("tr.provinces_ntr").remove()
    }
}

function provincesPush() {
    var trList = $("td.provinces_ntd")
    var pDatas = []
    trList.each(function(){
        var pData = {}
        pData["Provinces"] = $(this).find("input#input_province").val()
        pData["City"] = $(this).find("input#input_city").val()
        pDatas.push(pData)
    })
    if(pDataCheck(pDatas)){
        if(confirm('准备添加数据，是否继续？')){
            $.ajax({
                url: Flask.url_for('sysOption.provinces'),
                type: "post",
                data: JSON.stringify(pDatas),
                datatype: "json",
                contentType: "application/json",
                success: function(data){
                    data = JSON.parse(data)
                    if(data.status == 1){
                        alert("添加成功")
                        parent.layer.closeAll()
                    }
                    else{
                        alert("添加失败")
                    }
                }
            })
        }
    }
}

function pDataCheck(pDatas) {
    for (x in pDatas){
        if (isNull(pDatas[x].Provinces)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
        if (isNull(pDatas[x].City)) {
            alert("存在未填写项，请核对数据。")
            return false
        }
    }
    return true
}


function provincesAddLayer() {
    var url = Flask.url_for("sysOption.provincesAdd")
    layer_sysOpt = layer.open(
        {
            type: 2,
            skin: 'layui-layer-rim',
            title: "新增省市信息",
            area: ['600px', '300px'],
            content: url,
            resize: true,
            maxmin: true,
            resizing: function(){
                var height = ($("#layui-layer1").css("height"))
                $("#layui-layer-iframe1").css({
                    'height': (parseInt(height)-55)+"px"
                })
            },
            full: function(){
                var height = ($("#layui-layer1").css("height"))
                $("#layui-layer-iframe1").css({
                    'height': (parseInt(height)-55)+"px"
                })
            },
            restore: function(){
                var height = ($("#layui-layer1").css("height"))
                $("#layui-layer-iframe1").css({
                    'height': (parseInt(height)-55)+"px"
                })
            }
        }
    )
}