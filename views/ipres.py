#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 14:59
# @Author  : Derek.S
# @Site    : 
# @File    : ipres.py


from flask import render_template, url_for, request, Blueprint
from model import getProvincesName, setIPResAdd, delIP, getIPResModify, setIPResModify

IPRESViews = Blueprint("IPRESViews", __name__)


@IPRESViews.route("/ipres/add", methods=['GET', 'POST'])
def ipresAdd():
    if(request.method == "GET"):
        Provinces = getProvincesName()
        return render_template("ipresadd.html", pNames=Provinces)
    elif(request.method == "POST"):
        ipDatas = request.get_json()
        result = setIPResAdd(ipDatas)
        return result


@IPRESViews.route("/ipres/del", methods=['POST'])
def ipresDelete():
    idJson = request.get_json()
    return delIP(idJson)

@IPRESViews.route("/ipres/modify", methods=['POST'])
def ipresModify():
    postJson = request.get_json()
    op = postJson["op"]
    if(op == "get"):
        rawData = getIPResModify(postJson)
        Provinces = getProvincesName()
        return render_template("ipresmodify.html", ipResDatas=rawData, Provinces=Provinces)
    elif(op == "post"):
        return setIPResModify(postJson)