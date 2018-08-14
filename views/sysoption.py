#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 17:11
# @Author  : Derek.S
# @Site    : 
# @File    : sysoption.py


from flask import Blueprint, render_template, request, abort
from model import getSystem, setLimit, setProvinces, provincesViews, paginate


sysOption = Blueprint("sysOption", __name__)


@sysOption.route("/system", methods=['GET', 'POST'])
def systemOption():
    """
    系统设置视图
    :return:
    """
    if(request.method == "GET"):
        sysOptData = getSystem()
        return render_template("system.html", data=sysOptData)
    elif(request.method == "POST"):
        Option = request.get_json()
        limitNum = int(Option["limitNum"])
        return setLimit(limitNum)


@sysOption.route("/system/provinces", methods=['GET'])
def provincesView():
    """
    行政区划视图
    :return:
    """
    if(request.method == "GET"):
        pageNum = int(request.args.get("page", 1))
        pDatas, totalPNum = provincesViews()
        if(pageNum <= totalPNum):
            return render_template("provinces.html", pDatas=pDatas, pagination=paginate(pDatas, pageNum))
        else:
            abort(404)
    elif(request.method == "POST"):
        abort(400)


@sysOption.route("/system/provinces/add", methods=['GET', 'POST'])
def provincesAdd():
    """
    新增行政区划视图
    :return:
    """
    if(request.method == "GET"):
        return render_template("provincesadd.html")
    elif(request.method == "POST"):
        pData = request.get_json()
        return setProvinces(pData)

