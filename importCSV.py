#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/17 0:05
# @Author  : Derek.S
# @Site    : 
# @File    : importCSV.py

from app import mongo
from model import getID
import json

def insertTaskIDToDB(taskid):
    """
    生成的taskid插入数据库
    :param taskid: taskid
    :return:
    """
    try:
        taskInfo = {
            "ID": taskid,
            "progress": 1,
            "countNum": 0,
            "ErrorCount": 0,
            "ErrorRowIDs": [],
            "totalRows": 0
        }
        mongo.db.IPRMS_TaskStatus.insert_one(taskInfo)
    except Exception as e:
        print(e)

def insertToDB(ipSource, ipStart, ipEnd, csvLocation, MRoom, ipUser, ipUsed, csvID, taskID, totalRows):
    """
    csv导入数据库
    :param ipSource: IP来源
    :param ipStart: 起始IP
    :param ipEnd: 终止IP
    :param csvLocation: csv内所属市州数据
    :param MRoom: 所属机房
    :param ipUser: 用户名称
    :param ipUsed: 使用IP
    :param csvID: csv文件内序号，方便错误定位
    :param taskID: 任务ID
    :param totalRows: csv内总行数
    :return: 插入行数
    """
    ID = getID()
    errorsCsvID = []
    try:
        mongo.db.IPRMS_TaskStatus.update_one({"ID": taskID}, {"$set": {"totalRows": totalRows}})
        selectPCData = mongo.db.IPRMS_Provinces.find_one({"City": {"$regex": str(csvLocation)}})
        if(selectPCData):
            CityName = selectPCData["City"]
            ProvincesName = selectPCData["Provinces"]
            Location = ProvincesName + CityName
            inData = {
                "ID": ID,
                "ipSource": ipSource,
                "ipStart": ipStart,
                "ipEnd": ipEnd,
                "Provinces": ProvincesName,
                "City": CityName,
                "Location": Location,
                "MRoom": MRoom,
                "ipUser": ipUser,
                "ipUsed": ipUsed
            }
        else:
            inData = {
                "ID": ID,
                "ipSource": ipSource,
                "ipStart": ipStart,
                "ipEnd": ipEnd,
                "Provinces": "",
                "City": "",
                "Location": csvLocation,
                "MRoom": MRoom,
                "ipUser": ipUser,
                "ipUsed": ipUsed
            }
            errorsCsvID.append(csvID)

        ID += 1
        # 插入数据并更新ID
        mongo.db.IPRMS_IPRes.insert_one(inData)
        mongo.db.IPRMS_idRecode.update_one({"Collection_ID": "IPRMS_IPRes"}, {"$set": {"id": ID}})
        if(not len(errorsCsvID)):
            mongo.db.IPRMS_TaskStatus.update_one(
                {"ID": taskID},
                {"$inc": {"countNum": 1}}
            )
        else:
            mongo.db.IPRMS_TaskStatus.update_one(
                {"ID": taskID},
                {"$inc": {"countNum": 1, "ErrorCount": len(errorsCsvID)},"$push": {"ErrorRowIDs": errorsCsvID[0]}}
            )

    except Exception as e:
        print(e)


def getTaskStatus(taskid):
    task = mongo.db.IPRMS_TaskStatus.find_one({"ID": taskid})
    totalRow = task["totalRows"]
    countNum = task["countNum"]
    if(countNum == 0):
        progress = 1
    else:
        progress = int(countNum / totalRow * 100)
    errorCount = task["ErrorCount"]
    errorRowIDs = task["ErrorRowIDs"]

    TaskStatus = {
        "status": 1,
        "countNum": countNum,
        "totalRow": totalRow,
        "progress": progress,
        "errorCount": errorCount,
        "errorRowIDs": errorRowIDs
    }

    return json.dumps(TaskStatus)