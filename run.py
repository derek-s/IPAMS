#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 13:01
# @Author  : Derek.S
# @Site    : 
# @File    : run.py

from app import app
from views.index import indexViews
from views.bgViews import bgViews

app.register_blueprint(bgViews)
app.register_blueprint(indexViews)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)