#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/15 14:59
# @Author  : Derek.S
# @Site    : 
# @File    : ipres.py


from flask import render_template, url_for, request, Blueprint
from model import getProvincesName, setIPResAdd

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