#!/usr/bin/env python
# encoding: utf-8
"""
    __auth__: 孟德功
    __require__: 配置各种环境变量
    __version__: 无要求
"""
FILES = ['group', 'login']  # 选择所要执行/AT-wda/case中的文件名

BUNDLE_ID = 'com.*************'   # App bundle id

PRINT = True    # 打印case运行日志

DEVICE = 1  # 选择第一台(目前仅支持单台设备,若插入多个设备,可以自行选择其中一台执行)

ALERT = [u'不再提醒', 'OK', u'知道了', 'Allow', u'允许', u'稍后', u'好']    # 处理不知何时就会突然弹出的警告框,可以根据业务拓展

WDA_PATH = '/Users/*******/Documents/Macaca/WebDriverAgent/WebDriverAgent.xcodeproj' # WebDriverAgent.xcodeproj 的绝对路径

DD_TOKEN = '********************************************'  # 钉钉的token(在钉钉pc版中可以获取机器人的token)

ELEM_TIMEOUT = 20    # 获取元素最大等待时长
