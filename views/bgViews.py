#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 21:35
# @Author  : Derek.S
# @Site    : 
# @File    : bgViews.py

from model import init_idRecode
from flask import Blueprint


bgViews = Blueprint("bgViews", __name__)


@bgViews.route("/bg/_initID")
def initDBID():
    #return 0
    return init_idRecode()