#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 15:31
# @Author  : Derek.S
# @Site    : 
# @File    : index.py

from flask import render_template, request, Blueprint, abort, redirect, url_for
from model import IPResViews, paginate, searchAll
from search import search
from upload import checkFileName, ListfileName, importCSVToDB, createUID
from importCSV import getTaskStatus
from initapp import createCollections, checkInit, loadProvincesData

from app import app, executor
import os
import json


indexViews = Blueprint("indexViews", __name__)


@indexViews.route("/")
def indexPage():
    if(checkInit()):
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
    else:
        return redirect(url_for("indexViews.initAPP"))


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


@indexViews.route("/upload", methods=["GET", "POST"])
def uploadCSV():
    """
    上传CSV
    :return:
    """
    if(request.method == "GET"):
        return render_template("upload.html")
    elif(request.method == "POST"):
        file = request.files['file']
        if(file and checkFileName(file.filename)):
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            return render_template("jump.html", info="上传完成", url="indexViews.uploadCSV")
        else:
            return render_template("jump.html", info="未选择文件或文件名不符合规定", url="indexViews.uploadCSV")


@indexViews.route("/upload/getFileList", methods=["GET","POST"])
def getFileList():
    """
    返回uploads文件夹内的已上传文件
    :return:
    """
    FileList = ListfileName(app.config["UPLOAD_FOLDER"])
    return render_template("Filelist.html", FileList=FileList)


@indexViews.route("/upload/start", methods=["POST"])
def importStart():
    """
    启动导入
    :return:
    """
    uuid = createUID()
    jsonDatas = request.get_json()
    fileName = jsonDatas["fileName"]
    executor.submit(importCSVToDB, fileName, uuid)
    status = {
        "status": 1,
        "taskid": uuid
    }
    return json.dumps(status)


@indexViews.route("/upload/status", methods=["POST"])
def getStatus():
    """
    查询状态
    :return:
    """
    jsonDatas = request.get_json()
    taskid = jsonDatas["taskid"]
    result = getTaskStatus(taskid)
    return result


@indexViews.route("/_init", methods=["GET"])
def initAPP():
    """
    初始化应用
    :return:
    """
    checkResult = checkInit()
    if(checkResult == 0):
        ccRsult = createCollections()
        loadProvincesData()
        if(ccRsult == 1):
            return render_template("jump.html", info="初始化完成", url="indexViews.indexPage")
    return render_template("jump.html", info="已进行初始化", url="indexViews.indexPage")
