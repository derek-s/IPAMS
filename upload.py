#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/17 0:05
# @Author  : Derek.S
# @Site    : 
# @File    : upload.py

from werkzeug.utils import secure_filename
from app import app, executor
from importCSV import insertTaskIDToDB, insertToDB
import uuid
import os
import json


def checkFileName(filename):
    """
    检查文件名
    :param filename: 文件名
    :return:
    """
    FileName = secure_filename(filename)
    print(FileName)
    if(FileName.split(".", 1)[1] in ("csv")):
        print(FileName)
        return True


def ListfileName(path):
    """
    获取文件名
    :return:
    """
    FileNameSet = set()
    for eachFile in os.listdir(path):
        FileNameSet.add(eachFile)
    return FileNameSet


def createUID():
    """
    生成UUID用作taskid
    :return: uuid str
    """
    return str(uuid.uuid1())


def importCSVToDB(filename, taskID):
    """
    启动导入
    :param filename: 文件名
    :return:
    """
    try:
        insertTaskIDToDB(taskID)
        path = str(app.config["UPLOAD_FOLDER"])
        needFile = path + "/" + filename
        with open(needFile, "r") as File:
            csvContent = File.readlines()
        File.close()
        totalRows = len(csvContent)
        for eachLine in csvContent:
            eachLineSplit = eachLine.split(",")
            csvID = eachLineSplit[0]
            ipSource = eachLineSplit[1]
            ipStart = eachLineSplit[2]
            ipEnd = eachLineSplit[3]
            csvLocation = eachLineSplit[4]
            MRoom = eachLineSplit[5]
            ipUser = eachLineSplit[6]
            ipUsed = eachLineSplit[7]
            insertToDB(
                ipSource, ipEnd, ipStart, csvLocation,
                MRoom, ipUser, ipUsed, csvID, taskID, totalRows
            )
    except Exception as e:
        print(e)

