#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/10 13:01
# @Author  : Derek.S
# @Site    : 
# @File    : run.py

from app import app
from views.index import indexViews
from views.bgviews import bgViews
from views.sysoption import sysOption
from views.ipres import IPRESViews

app.register_blueprint(bgViews)
app.register_blueprint(indexViews)
app.register_blueprint(sysOption)
app.register_blueprint(IPRESViews)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)