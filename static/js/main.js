/// <reference path="C:/Users/Derek.S/AppData/Roaming/npm/node_modules/@types/jquery/index.d.ts" />
$(document).ready(
    function () {

        $("#checkboxall").click(function () {
            if ($("#checkboxall").prop("checked")) {
                $("[name='oper']").prop("checked", true)
            } else {
                $("[name='oper']").prop("checked", false)
            }
        })
        $(document).on("click", '[name="oper"]', function () {
            var check = 0
            if ($("#checkboxall").prop("checked")) {
                $("#checkboxall").prop("checked", false)
            }
            var inputcount = $("input[name='oper']").length
            $("input[name='oper']").each(function () {
                if ($(this).prop("checked")) {
                    check += 1
                }
                if (inputcount === check) {
                    $("#checkboxall").prop("checked", true)
                }
            })
        })

        id_array = new Array()

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            }
        })
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
                url: Flask.url_for('sysOption.provincesAdd'),
                type: "post",
                data: JSON.stringify(pDatas),
                datatype: "json",
                contentType: "application/json",
                success: function(data){
                    data = JSON.parse(data)
                    if(data.status == 1){
                        alert("添加成功")
                        parent.layer.closeAll()
                        parent.location.reload()
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
            id: "Pvs_AddLayer",
            type: 2,
            skin: 'layui-layer-rim',
            title: "新增省市信息",
            area: ['600px', '300px'],
            content: url,
            resize: true,
            resizing: function(){
                var height = ($(".layui-layer-rim").css("height"))
                console.log(height)
                $("#Pvs_AddLayer > iframe").css({
                    'height': (parseInt(height)-55)+"px"
                })
            }
        }
    )
}

function getCheckBoxID(){
    var CheckBoxArray = []
    $("input[name='oper']:checked").each(
        function () {
            CheckBoxArray.push($(this).val())
        }
    )
    CheckBoxArray = Array.from(new Set(CheckBoxArray))
    return CheckBoxArray
}


function Pvs_OP(idArray){
    if($("select#OPSelect").val() == "delete"){
        if(isNull(idArray)){
            alert("尚未选中任何需要操作的数据！")
        }else{
            Pvs_Delete(idArray)
        }
    }else if($("select#OPSelect").val() == "modify"){
        if(isNull(idArray)){
            alert("尚未选中任何需要操作的数据！")
        }else{
            Pvs_ModfiyLayer(idArray, "get")
        }
    }
}


function Pvs_Delete(idArray) {
    data = {
        "idArray" : idArray
    }
    if(confirm("确认删除信息么？")){
        $.ajax({
            url: Flask.url_for('sysOption.provincesDelete'),
            type: "POST",
            data: JSON.stringify(data),
            dataType: "json",
            contentType: "application/json",
            success: function(data){
                if(data.status == 1){
                    alert("删除成功 共删除 " + data.result + " 条记录")
                    parent.location.reload()
                }
                else{
                    alert("删除失败")
                }
            }
        })
    }
}


function Pvs_ModfiyLayer(idArray, op){
    url = Flask.url_for('sysOption.provincesModify')
    if(op == "get"){
        if(idArray){
            var postArray = {
                "op": "get",
                "idArray": idArray
            }
            $.ajax({
                url: url,
                type: "post",
                data: JSON.stringify(postArray),
                contentType: "application/json",
                dataType: "html",
                success: function(html){
                    layer.open({
                        id: "Pvs_ModifyLayer",
                        type: 1,
                        skin: 'layui-layer-rim',
                        title: '修改省市信息',
                        area: ['600px', '300px'],
                        content: html,
                        resize: true,
                        resizing: function(){
                            var height = ($(".layui-layer-rim").css("height"))
                            console.log(height)
                            $("#Pvs_ModifyLayer").css({
                                'height': (parseInt(height)-55)+"px"
                            })
                        }
                    })
                }
            })
        }
    }else if(op == "post"){
        if(confirm("确定修改省市信息么？")){
            if(idArray){
                var PostArray = {
                    "op": "post",
                    "idArray": idArray
                }
                $.ajax({
                    url: url,
                    type: "post",
                    data: JSON.stringify(PostArray),
                    datatype: "json",
                    contentType: "application/json",
                    success: function(resp) {
                        resp = JSON.parse(resp)
                        if(resp.status == 1){
                            alert("操作成功 共修改 " + resp.UpdateCount + " 条记录")
                            parent.layer.closeAll()
                            parent.location.reload()
                        }
                        else {
                            alert("操作失败")
                        }
                    }
                })
            }
        }
    }
}

function Pvs_GetDataModify(){
    var PvsDataArray = new Array()
    var PvsTD = $("tr.provinces_modinput")
    PvsTD.each(function(){
        var PvsData = {}
        PvsData["ID"] = $(this).find("#id_province").text()
        PvsData["Provinces"] = $(this).find("#input_province").val()
        PvsData["City"] = $(this).find("#input_city").val()
        console.log(PvsData)
        PvsDataArray.push(PvsData)
    })
    console.log(PvsDataArray)
    Pvs_ModfiyLayer(PvsDataArray, "post")
}