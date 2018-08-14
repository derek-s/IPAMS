#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/9 20:51
# @Author  : Derek.S
# @Site    : 
# @File    : model.py

from app import mongo
from flask_pymongo import DESCENDING


from math import ceil
import json


limitNum = int(mongo.db.IPRMS_System.find_one({"sysOption": "limitNum"})["limitNum"])


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
    TODO: 需要修改一下更新方式，现在都是插入
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
            "status": 0,
            "msg": "操作失败"
        }
    return json.dumps(status)


def getSystem():
    """
    取系统设置参数
    :return:  int limit num
    TODO: 跟随setLimit函数同步修改
    """
    option = {}
    try:
        limitNum = mongo.db.IPRMS_System.find_one()["limitNum"]
        option["limitNum"] = int(limitNum)
    except Exception as e:
        print(e)
    return option


def setProvinces(ProvincesData):
    """
    添加行政区划信息 仅支持到地市一级
    :param ProvincesData: Dict Data
    :return:
    """
    try:
        mongo.db.IPRMS_Provinces.insert_many(ProvincesData)
        status = {
            "status": 1,
            "msg": "操作成功"
        }
    except Exception as e:
        print(e)
        status = {
            "status": 0,
            "msg": "操作失败"
        }
    return json.dumps(status)


def provincesViews():
    """
    查看行政区划数据
    :return:
    """
    try:
        provincesData = mongo.db.IPRMS_Provinces.find({})
        totalPNum = ceil(provincesData.count() / limitNum)
        return provincesData, totalPNum
    except Exception as e:
        print(e)


def getIPRes():
    pass


class Pagination:
    def __init__(self, items, page, per_page, total_items):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total_items = total_items
        self.num_pages = int(ceil(total_items / per_page))

    @property
    def has_next(self):
        return self.page < self.num_pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def next_page(self):
        return self.page + 1

    @property
    def prev_page(self):
        return self.page - 1

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.num_pages + 1):
            if num <= left_edge or \
                    (num > self.page - left_current - 1 and \
                     num < self.page + right_current) or \
                    num > self.num_pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def paginate(queryset, page=1, per_page=limitNum):
    skip  = (page - 1)*per_page
    limit = per_page

    return Pagination(queryset.limit(limit).skip(skip), page=page, per_page=per_page, total_items=queryset.count())