#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 20:51
# @Author  : Derek.S
# @Site    : 
# @File    : model.py

from app import mongo
import json


def init_idRecode():
    """
    初始化自定义自增id
    :return:
    """
    initID = {
        'id': 0
    }
    dbCollectTest = mongo.db.collection_names()
    if "IPRMS_idRecode" not in dbCollectTest:
        try:
            mongo.db.IPRMS_idRecode.insert_one(initID)
            status = 0
        except:
            status = 1
    else:
        status = 1
    return status


def getID():
    """
    获取自定义ID的值
    :return:
    """
    id = mongo.db.IPRMS_idRecode.find_one()["id"] + 1
    return id


def setLimit(limit=20):
    """
    设置分页参数
    :param limit: int limit num
    :return: None
    """
    limitDict = {
        "limit": limit
    }
    try:
        mongo.db.IPRMS_System.insert_one(limitDict)
        status = {
            "status": 1,
            "msg": "操作成功"
        }
    except:
        status = {
            "status": 1,
            "msg": "操作失败"
        }
    return json.dumps(status)


def getSystem():
    """
    取系统设置参数
    :return:  int limit num
    """
    option = {}
    try:
        limitNum = mongo.db.IPRMS_System.find_one()["limitNum"]
        option["limitNum"] = int(limitNum)
    except Exception as e:
        print(e)
    return option


def getIPRes():
    pass