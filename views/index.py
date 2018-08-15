#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 15:31
# @Author  : Derek.S
# @Site    : 
# @File    : index.py

from flask import render_template, url_for, request, Blueprint, abort
from model import IPResViews, paginate


indexViews = Blueprint("indexViews", __name__)

@indexViews.route("/")
def indexPage():
    if (request.method == "GET"):
        pageNum = int(request.args.get("page", 1))
        IPResData, totalPNum, totalNum = IPResViews()
        if (pageNum <= totalPNum or totalPNum == 0):
            return render_template(
                "index.html",
                IPRes=IPResData,
                pagination=paginate(IPResData, pageNum),
                totalNum=totalNum
            )
        else:
            abort(404)
    elif (request.method == "POST"):
        abort(400)

@indexViews.route("/serach")
def Search():
    Search_Args = request.args
    KeyWord = Search_Args["keyword"]
    Mode = Search_Args["mode"]
    return KeyWord + Mode