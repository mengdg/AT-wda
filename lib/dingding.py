# -*- coding:utf-8 -*-
"""
    __auth__: 孟德功
    __require__: 发送报警信息
    __version__: 无要求
"""

import json
import requests
import sys
from setting import DD_TOKEN

reload(sys)
sys.setdefaultencoding('utf-8')


class dingding:
    def __init__(self, content=None):
        self.URL = 'https://oapi.dingtalk.com/robot/send?access_token=%s'% DD_TOKEN
        self.HEADERS = {"Content-Type": "application/json ;charset=utf-8 "}
        self.content = content

        self.data_text = dict()
        self.data_text['msgtype'] = 'text'
        self.data_text['text'] = {'content': self.content}
        self.data_text['at'] = {'isAtall': True}

    def main(self):
        text_json = json.dumps(self.data_text)
        requests.post(self.URL, data=text_json, headers=self.HEADERS)
