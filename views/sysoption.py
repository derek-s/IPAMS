#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 17:11
# @Author  : Derek.S
# @Site    : 
# @File    : sysoption.py

from flask import Blueprint, render_template, request
from model import getSystem, setLimit


sysOption = Blueprint("sysOption", __name__)

@sysOption.route("/system", methods=['GET', 'POST'])
def systemOption():
    if(request.method == "GET"):
        sysOptData = getSystem()
        return render_template("system.html", data=sysOptData)
    elif(request.method == "POST"):
        Option = request.get_json()
        limitNum = int(Option["limitNum"])
        return setLimit(limitNum)

