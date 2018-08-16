#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/16 23:40
# @Author  : Derek.S
# @Site    : 
# @File    : search.py

from flask import render_template, abort
from model import paginate, serachPrecise


def search(keyword, pageNum, Model, field):
    SearchResult, totalPNum, totalNum = serachPrecise(keyword, field)
    if (pageNum <= totalPNum or totalPNum == 0):
        return render_template(
            "search.html",
            IPRes=SearchResult,
            pagination=paginate(SearchResult, pageNum),
            totalNum=totalNum,
            keyword=keyword,
            Model=Model
        )
    else:
        abort(404)