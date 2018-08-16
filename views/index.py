#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 15:31
# @Author  : Derek.S
# @Site    : 
# @File    : index.py

from flask import render_template, request, Blueprint, abort
from model import IPResViews, paginate, searchAll, serachPrecise
from search import search

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
    pageNum = int(request.args.get("page", 1))
    Search_Args = request.args
    KeyWord = Search_Args["keyword"]
    Mode = Search_Args["mode"]
    if(Mode == "all"):
        Model = "模糊查询模式"
        SearchResult, totalPNum, totalNum  = searchAll(KeyWord)
        if (pageNum <= totalPNum or totalPNum == 0):
            return render_template(
                "search.html",
                IPRes=SearchResult,
                pagination=paginate(SearchResult, pageNum),
                totalNum=totalNum,
                keyword=KeyWord,
                Model=Model
            )
        else:
            abort(404)
    elif(Mode == "IPSource"):
        Model = "精准 IP来源单位模式"
        return search(KeyWord, pageNum, Model, "ipSource")
    elif (Mode == "StartIP"):
        Model = "精准 起始IP模式"
        return search(KeyWord, pageNum, Model, "ipStart")
    elif (Mode == "EndIP"):
        Model = "精准 终止IP模式"
        return search(KeyWord, pageNum, Model, "ipEnd")
    elif (Mode == "Address"):
        Model = "精准 所属地址模式"
        return search(KeyWord, pageNum, Model, "Location")
    elif (Mode == "mRoom"):
        Model = "精准 所属机房模式"
        return search(KeyWord, pageNum, Model, "MRoom")
    elif (Mode == "User"):
        Model = "精准 专线用户模式"
        return search(KeyWord, pageNum, Model, "ipUser")
    elif (Mode == "IPUsed"):
        Model = "精准 使用IP模式"
        return search(KeyWord, pageNum, Model, "ipUsed")
    elif (Mode == "Provinces"):
        Model = "精准 省份名称模式"
        return search(KeyWord, pageNum, Model, "Provinces")
    elif (Mode == "City"):
        Model = "精准 市州名称模式"
        return search(KeyWord, pageNum, Model, "City")
    else:
        abort(404)