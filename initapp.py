#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/20 17:53
# @Author  : Derek.S
# @Site    : 
# @File    : initapp.py

from app import mongo
import json

def checkInit():
    """
    检查初始化状态
    :return:
    """

    initStatus = mongo.db.IPRMS_System.find_one({"sysOption": "init"})
    if(initStatus):
        return 1
    else:
        return 0


def createCollections():
    """
    创建集合并初始化数据
    :return:
    """
    try:
        sysLimit = {
            "sysOption": "limitNum",
            "limitNum": 20
        }
        initOff = {
            "sysOption": "init",
            "init": True
        }
        mongo.db.IPRMS_System.insert_one(sysLimit)
        mongo.db.IPRMS_System.insert_one(initOff)

        IPResID = {
            "Collection_ID": "IPRMS_IPRes",
            "id": 0
        }
        ProvincesID = {
            "Collection_ID": "IPRMS_Provinces",
            "id": 0
        }
        mongo.db.IPRMS_idRecode.insert_one(IPResID)
        mongo.db.IPRMS_idRecode.insert_one(ProvincesID)

        return 1
    except Exception as e:
        print(e)
        return 0


def loadProvincesData():
    """
    导入初始化省市区数据
    :return:
    """
    id = mongo.db.IPRMS_idRecode.find_one({"Collection_ID": "IPRMS_Provinces"})["id"]
    with open("sc.json") as sc:
        scJson = json.load(sc)
        for each in scJson:
            each["ID"] = id
            id += 1
    mongo.db.IPRMS_Provinces.insert_many(scJson)
    mongo.db.IPRMS_idRecode.update_one({"Collection_ID": "IPRMS_Provinces"}, {"$set": {"id": id}})