#!/usr/bin/env python
# encoding: utf-8
"""
    __auth__: 孟德功
    __require__: 获取手机信息
    __version__: 无要求
"""
from setting import BUNDLE_ID, WDA_PATH, DEVICE
import re
import os
import commands
import json
import requests
import getpass
import multiprocessing
import wd


class InitDevice:
    """
    连接设备
    """

    def __init__(self):
        self.port = 8100
        self.GET_IOS = "instruments -s devices"
        self.device = self.device()
        self.num = 0

    def media(self):
        return self.start_wda()

    def get_device(self):
        device = []
        value = os.popen(self.GET_IOS)
        for v in value.readlines():
            iOS = {}
            s_value = str(v).replace("\n", "").replace("\t", "").replace(" ", "")
            if v.rfind('Simulator') != -1:
                continue
            if v.rfind("(") == -1:
                continue
            if v.rfind('root') != -1:
                continue
            iOS['platformName'] = 'iOS'
            if re.compile(r'\((.*)\)').findall(s_value)[0] != 'null':
                iOS['platformVersion'] = re.compile(r'\((.*)\)').findall(s_value)[0]
                iOS['deviceName'] = re.compile(r'(.*)\(').findall(s_value)[0]
                iOS['udid'] = re.compile(r'\[(.*?)\]').findall(s_value)[0]
                iOS['bundled'] = BUNDLE_ID
                device.append(iOS)
        num = len(device)
        for i in device:
            i['proxyPort'] = self.port
            self.port += 100
        if device:
            print ('=' * 20 + ' 共 %d 台外接iOS设备 ' + '=' * 20) % num
        for i in device:
            print '\033[1;37;0m' + "{}".format(json.dumps(i, indent=4)) + '\033[0m'
        return device

    def device(self):
        # 目前仅支持一台设备
        d = []
        device = self.get_device()
        if device:
            print ('-' * 22 + ' 选择了第 %d 设备 ' + '-' * 22) % DEVICE
        try:
            if DEVICE > 0:
                d.append(device[DEVICE - 1])
            else:
                d.append(device[0])
        except:
            print '\n请重新选择设备...'
        for i in d:
            print '\033[1;37;0m' + "{}".format(json.dumps(i, indent=4)) + '\033[0m'
        return d

    def start_wda(self):
        list = []
        for d in self.device:
            deviceName = d['deviceName']
            port = d['proxyPort']
            udid = d['udid']
            self.kill_xb(platform=deviceName)
            self.start_iproxy(port, udid)
            while True:
                try:
                    RunServer(name=deviceName).run_server()
                except Exception as e:
                    self.start_wda()
                finally:
                    import time
                    time.sleep(13)
                    self.num += 1
                    if self.stause(port):
                        print '*' * 25 + ' 连接成功 ' + '*' * 25
                        break
                    if self.num == 5:
                        break
            wda_c = wd.Client('http://localhost:%s' % port)
            list.append(wda_c)
        return list

    def start_iproxy(self, port, udid):
        self.kill_iproxy(port=port)
        RunServer(port=port, udid=udid).run_port()

    def stause(self, port):
        url = 'http://127.0.0.1:%s/status' % str(port)
        response = None
        try:
            response = requests.get(url, timeout=1)
            if str(response.status_code).startswith('2'):
                return True
            else:
                return False
        except requests.exceptions.ConnectionError:
            return False
        except requests.exceptions.ReadTimeout:
            return False
        finally:
            if response:
                response.close()

    @staticmethod
    def kill_xb(platform=None):
        if platform == None:
            command = os.popen("ps -x | grep '/Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild'")
        else:
            command = os.popen("ps -x | grep 'platform=iOS,name=%s'" % platform)
        for i in command.readlines():
            if 'ps -x | grep' in i:
                continue
            if 'grep /Applications/Xcode.app/' in i:
                continue
            if 'grep platform=iOS,' in i:
                continue
            pid = str(i).replace("\n", "").replace("\t", "").split(' ')
            if pid[0]:
                os.popen('kill -9 %d' % int(pid[0]))
            try:
                if pid[1]:
                    os.popen('kill -9 %d' % int(pid[1]))
            except:
                pass

    @staticmethod
    def kill_iproxy(port=None):
        if port == None:
            os.system('pkill -9 iproxy')
        else:
            command = os.popen('lsof -i:%d' % int(port))
            for i in command.readlines():
                user = getpass.getuser()
                pid = str(i).replace("\n", "").replace("\t", "").replace(" ", "").replace('iproxy', '')
                if user in pid:
                    p = pid.split(user)[0]
                    os.system('kill -9 %d' % int(p))

    def thread(self, port=None, name=None, udid=None):
        p = multiprocessing.Process(target=self.start_iproxy, args=(port, udid))
        p.start()


class RunServer():
    def __init__(self, port=None, name=None, udid=None):
        self.proxy = 'iproxy %s %s %s' % (port, port, udid)
        self.server = "xcodebuild -project %s -scheme WebDriverAgentRunner -destination 'platform=iOS,name=%s' test" % (
            WDA_PATH, name)

    def server_cmd(self):
        commands.getstatusoutput(self.server)

    def port_cmd(self):
        commands.getstatusoutput(self.proxy)

    def run_server(self):
        multiprocessing.Process(target=self.server_cmd).start()

    def run_port(self):
        multiprocessing.Process(target=self.port_cmd).start()
