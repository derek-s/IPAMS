#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/6 15:31
# @Author  : Derek.S
# @Site    : 
# @File    : index.py

from flask import Flask, render_template, url_for, request, Blueprint

indexViews = Blueprint("indexViews", __name__)

@indexViews.route("/")
def indexPage():
    return  render_template("index.html")

@indexViews.route("/serach")
def Search():
    Search_Args = request.args
    KeyWord = Search_Args["keyword"]
    Mode = Search_Args["mode"]
    return KeyWord + Mode