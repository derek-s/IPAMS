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
            var inputCount = $("input[name='oper']").length
            $("input[name='oper']").each(function () {
                if ($(this).prop("checked")) {
                    check += 1
                }
                if (inputCount === check) {
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

        $(document).on("change", "select#select_provinces", function(){
            var selectCity = $(this).parent().next().children()
            if($(this).val() == "Pvs_Null"){
                selectCity.empty()
                selectCity.append('<option value="City_Null">请选择市州</option>')
            } else {
                selectCity.empty()
            }
            jsLoadCity($(this).val(), selectCity)
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
    var tdList = $("td.provinces_ntd")
    var pDatas = []
    tdList.each(function(){
        var pData = {}
        pData["Provinces"] = $(this).find("input#input_province").val()
        pData["City"] = $(this).find("input#input_city").val()
        pDatas.push(pData)
    })
    pushData(pDatas, "systemOption.provincesAdd")
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
    deleteData(data, "sysOption.provincesDelete")
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
        PvsDataArray.push(PvsData)
    })
    Pvs_ModfiyLayer(PvsDataArray, "post")
}

function ipresPush(){
    var tdList = $("td.ipres_ntd")
    var ipDatas = []
    tdList.each(function(){
        var ipData = {}
        ipData["ipSource"] = $(this).find("#input_ipsource").val()
        ipData["ipStart"] = $(this).find("#input_startip").val()
        ipData["ipEnd"] = $(this).find("#input_endip").val()
        ipData["Provinces"] = $(this).find("#select_provinces").val()
        ipData["City"] = $(this).find("#select_city").val()
        ipData["MRoom"] = $(this).find("#input_mroom").val()
        ipData["ipUser"] = $(this).find("#input_PVCTUser").val()
        ipData["ipUsed"] = $(this).find("#input_PVCTIP").val()
        ipDatas.push(ipData)
    })
    pushData(ipDatas, "IPRESViews.ipresAdd")
}

function IPPushAdd(domObj){
    var base = $("table#ipres_table > tbody")
    var oLineFind = $(domObj).parents("tr.ipres_ntr")
    var ProvinceName = oLineFind.find("select#select_provinces").val()
    var CityName = oLineFind.find("select#select_city").val()
    var oCopyLine = oLineFind.clone()
    oCopyLine.find("option[value = '" + ProvinceName + "']" ).attr("selected", "selected")
    oCopyLine.find("option[value = '" + CityName + "']" ).attr("selected", "selected")
    base.append(oCopyLine)
}
function IPPushDel(domObj){
    if($("tr.ipres_ntr").length === 1){
        alert("只有1行时不得删除")
    }else{
        $(domObj).parents("tr.ipres_ntr").remove()
    }
}

function jsLoadCity(ProvinceName, nextCityDom){
    var url = Flask.url_for("bgViews.getCity")
    $.ajax({
        async: false,
        url: url,
        data: JSON.stringify({"pName": ProvinceName}),
        type: "post",
        dataType: "json",
        contentType: "application/json",
        success: function(data){
            var CityList = data["CityList"]
            if(CityList.length != 0){
                nextCityDom.append('<option value="City_Null">请选择市州</option>')
                $.each(CityList, function(one){
                    CityName = CityList[one]
                    nextCityDom.append('<option value="' + CityName + '">' + CityName + '</option>')
                })
            }
        }
    })
}

function ipAddLayer(){
    var url = Flask.url_for("IPRESViews.ipresAdd")
    layer_ipAdd = layer.open({
        id: "IPAddLayer",
        type: 2,
        area: ['1366px', '300px'],
        skin: 'layui-layer-rim',
        title: "添加IP",
        content: url,
        resize: true,
            resizing: function(){
                var height = ($(".layui-layer-rim").css("height"))
                $("#IPAddLayer > iframe").css({
                    'height': (parseInt(height)-55)+"px"
                })
            }
    })
}

function pushData(Datas, URL){
    url = Flask.url_for(URL)
    if(pDataCheck(Datas)){
        if(confirm('准备添加数据，是否继续？')){
            $.ajax({
                url: url,
                type: "post",
                data: JSON.stringify(Datas),
                datatype: "json",
                contentType: "application/json",
                success: function(data){
                    data = JSON.parse(data)
                    if(data.status == 1){
                        if(data.Count){
                            alert("添加成功 共添加 " + data.Count + " 条数据")
                        }else{
                            alert("添加成功")
                        }
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

function ipRes_OP(idArray){
    if($("select#OPSelect").val() == "delete"){
        if(isNull(idArray)){
            alert("尚未选中任何需要操作的数据！")
        }else{
            ipRES_Delete(idArray)
        }
    }else if($("select#OPSelect").val() == "modify"){
        if(isNull(idArray)){
            alert("尚未选中任何需要操作的数据！")
        }else{
            ipres_ModfiyLayer(idArray, "get")
        }
    }
}

function ipRES_Delete(idArray){
    data = {
        "idArray" : idArray
    }
    deleteData(data, "IPRESViews.ipresDelete")
}


function deleteData(Datas, URL){
    var url = Flask.url_for(URL)
    if(confirm("确认删除信息么？")){
        $.ajax({
            url: url,
            type: "POST",
            data: JSON.stringify(Datas),
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


function ipres_ModfiyLayer(idArray, op){
    url = Flask.url_for('IPRESViews.ipresModify')
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
                        id: "ipRes_ModifyLayer",
                        type: 1,
                        skin: 'layui-layer-rim',
                        title: '修改IP资源信息',
                        area: ['1366px', '600px'],
                        content: html,
                        resize: true,
                        resizing: function(){
                            var height = ($(".layui-layer-rim").css("height"))
                            $("#ipRes_ModifyLayer").css({
                                'height': (parseInt(height)-55)+"px"
                            })
                        }
                    })
                }
            })
        }
    }else if(op == "post"){
        if(confirm("确定修改么？")){
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

function ipres_GetDataModify(){
    var tdList = $("tr.ipres_ntr")
    var ipDatas = []
    tdList.each(function(){
        var ipData = {}
        ipData["ID"] = $(this).find("#id_ipres").text()
        ipData["ipSource"] = $(this).find("#input_ipsource").val()
        ipData["ipStart"] = $(this).find("#input_startip").val()
        ipData["ipEnd"] = $(this).find("#input_endip").val()
        ipData["Provinces"] = $(this).find("#select_provinces").val()
        ipData["City"] = $(this).find("#select_city").val()
        ipData["MRoom"] = $(this).find("#input_mroom").val()
        ipData["ipUser"] = $(this).find("#input_PVCTUser").val()
        ipData["ipUsed"] = $(this).find("#input_PVCTIP").val()
        ipDatas.push(ipData)
    })
    ipres_ModfiyLayer(ipDatas, "post")
}