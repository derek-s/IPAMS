#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 21:35
# @Author  : Derek.S
# @Site    : 
# @File    : bgViews.py

from model import init_idRecode, getID
from flask import Blueprint


bgViews = Blueprint("bgViews", __name__)


@bgViews.route("/bg/_initID")
def initDBID():
    status = init_idRecode()
    if status == 1:
        idRecode_status = "集合已存在"
    else:
        idRecode_status = "集合新建完毕"
    return idRecode_status


@bgViews.route("/bg/_id")
def getDBID():
    return getID()