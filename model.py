#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 20:51
# @Author  : Derek.S
# @Site    : 
# @File    : model.py

from app import mongo

def init_idRecode():
    """
    初始化自定义自增id
    :return:
    """
    initID = {
        'id': 0
    }
    dbCollectTest = mongo.db.collection_names()
    print(dbCollectTest)
    if "IPRMS_idRecode" not in dbCollectTest:
        mongo.db.IPRMS_idRecode.insert_one(initID)
        status = 0
    else:
        status = 1
    return status



def getID():
    """
    获取自定义ID的值
    :return:
    """
    id = mongo.db.IPRMS_idRecode.find_one()["id"]
    return id

