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
    if "idRecode" not in dbCollectTest:
        mongo.db.IPAMS_idRecode.insert_one(initID)
        status = 0
    else:
        status = 1
    return status