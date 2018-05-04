# encoding: utf-8
"""
    __auth__: 孟德功
    __require__: 运行case核心文件
    __version__: 无要求
"""
from xlrt import get_case
from setting import FILES, BUNDLE_ID, ELEM_TIMEOUT, ALERT, PRINT
import lib
from lib.media import InitDevice
from lib.dingding import dingding
import time


class Running_test_case:
    def __init__(self, media=None):
        self.flag_run = 0
        self.flag_err = 0
        self.flag_warn = 0
        self.flag_assert = 0
        self.flag_assert_fail = 0
        self.module = None
        self.case = None
        self.is_run = 0
        self.is_warning = 0
        self.media = media
        self.err_info = None
        self.assert_info = None
        self.s = self.media.session(BUNDLE_ID)
        self.tc = get_case(FILES).excels()

    def start(self):
        # self.s.set_timeout(ELEM_TIMEOUT)
        case_data = self.tc
        for table in case_data:
            for case in table:
                self.screening(case)
        self.stop()

    def restart(self):
        self.s = self.media.session(BUNDLE_ID)

    def stop(self):
        self.s.close()
        InitDevice.kill_xb()
        InitDevice.kill_iproxy()

    def screening(self, case):
        if case:
            if case[0] != 'module':
                if self.flag_run == 0 and self.flag_err == 0 and self.flag_assert_fail == 0:
                    self.case_event(case)
                if int(self.is_warning) == 1:
                    if self.flag_warn == 0 and self.flag_err == 1 and self.flag_assert == 0:
                        self.flag_warn = 1
                        dingding(self.data('ERROR', case[0])).main()
                    if self.flag_assert == 0 and self.flag_assert_fail == 1 and self.flag_warn == 0:
                        self.flag_assert = 1
                        dingding(self.data('ASSERT', case[0])).main()
            else:
                try:
                    self.module = case[1]
                    self.case = case[3]
                    self.is_run = case[5]
                    self.is_warning = case[7]
                    self.flag_err = 0
                    self.flag_warn = 0
                    self.flag_assert = 0
                    self.flag_assert_fail = 0
                    self.assert_info = None
                    self.err_info = None
                    if int(self.is_run) == 0:
                        self.flag_run = 1
                    else:
                        self.print_color('other', '- ' * 5 + self.module + ' ' + self.case)
                        self.flag_run = 0
                        self.restart()
                except TypeError:
                    return False
                except Exception:
                    self.flag_err = 1
                    print ('请检查 module:%s  case:%s is_run:%s is_warning:%s'
                                     % (self.module, self.case, self.is_run, self.is_warning))
                    pass

    def case_event(self, case):
        try:
            self.s.set_alert_callback(self.alert_callback)
            self.print_color('run', case[0])
            if case[0] == u'点击':
                if len(case) == 3:
                    if case[1] == u'name':
                        self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).click_exists(timeout=ELEM_TIMEOUT)
                    elif case[1] == u'xpath':
                        self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).click_exists(timeout=ELEM_TIMEOUT)
                    elif case[1] == u'label':
                        self.s(label=case[2]).get(timeout=ELEM_TIMEOUT).click_exists(timeout=ELEM_TIMEOUT)
                else:
                    if case[1] == u'name':
                        self.s(name=case[2], index=int(case[3])).get(timeout=ELEM_TIMEOUT).click_exists(timeout=ELEM_TIMEOUT)
                    elif case[1] == u'label':
                        self.s(label=case[2], index=int(case[3])).get(timeout=ELEM_TIMEOUT).click_exists(timeout=ELEM_TIMEOUT)
            elif case[0] == u'输入':
                if case[1] == u'name':
                    if len(case) == 4:
                        self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).set_text(case[3])
                    else:
                        self.s(name=case[2], index=int(case[4])).get(timeout=ELEM_TIMEOUT).set_text(case[3])
                elif case[1] == u'xpath':
                    self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).set_text(case[3])
            elif case[0] == u'清除':
                if case[1] == u'name':
                    if len(case) == 3:
                        self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).clear_text()
                    else:
                        self.s(name=case[2], index=int(case[3])).get(timeout=ELEM_TIMEOUT).clear_text()
                elif case[1] == u'xpath':
                    self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).clear_text()
            elif case[0] == u'等待':
                time.sleep(int(case[1]))
            elif case[0] == u'截图':
                path = self.get_path() + '/var/screenshot/' + str(int(time.time()))
                self.media.screenshot('%s.png' % path)
            elif case[0] == u'停用':
                self.s.deactivate(int(case[1]))
            elif case[0] == u'坐标长按':
                self.s.tap_hold(float(case[1]), int(case[2]), time=int(case[3]))
            elif case[0] == u'坐标点击':
                self.s.tap(int(case[1]), int(case[2]))
            elif case[0] == u'坐标双击':
                self.s.double_tap(int(case[1]), int(case[2]))
            elif case[0] == u'坐标拖拽':
                self.s.swipe(int(case[1]), int(case[2]), int(case[3]), int(case[4]), float(case[5]))
            elif case[0] == u'长按':
                if case[1] == u'name':
                    if len(case) == 4:
                        e = self.s(name=case[2]).get(timeout=ELEM_TIMEOUT)
                    else:
                        e = self.s(name=case[2], index=int(case[4])).get(timeout=ELEM_TIMEOUT)
                    bounds = e.bounds
                    x = bounds.x
                    y = bounds.y
                    width = bounds.width
                    height = bounds.height
                    self.s.tap_hold(x + width / 2, y + height / 2, float(case[3]))
                elif case[1] == u'xpath':
                    e = self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT)
                    bounds = e.bounds
                    x = bounds.x
                    y = bounds.y
                    width = bounds.width
                    height = bounds.height
                    self.s.tap_hold(x + width / 2, y + height / 2, float(case[3]))
            elif case[0] == u'双击':
                if case[1] == u'name':
                    if len(case) == 3:
                        e = self.s(name=case[2]).get(timeout=ELEM_TIMEOUT)
                    else:
                        e = self.s(name=case[2], index=int(case[3])).get(timeout=ELEM_TIMEOUT)
                    bounds = e.bounds
                    x = bounds.x
                    y = bounds.y
                    width = bounds.width
                    height = bounds.height
                    self.s.double_tap(x + width / 2, y + height / 2)
                elif case[1] == u'xpath':
                    e = self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT)
                    bounds = e.bounds
                    x = bounds.x
                    y = bounds.y
                    width = bounds.width
                    height = bounds.height
                    self.s.double_tap(x + width / 2, y + height / 2)
            elif case[0] == u'左划':
                self.s.swipe_left()
            elif case[0] == u'右划':
                self.s.swipe_right()
            elif case[0] == u'上划':
                self.s.swipe_up()
            elif case[0] == u'下划':
                self.s.swipe_down()
            elif case[0] == u'断言':
                if case[1] == u'name':
                    if len(case) == 5:
                        if case[2] == u'value':
                            a = str(self.s(name=case[3]).get(timeout=ELEM_TIMEOUT).value)
                            if a == case[4]:
                                self.print_color('assert', a, case[4])
                            else:
                                self.flag_assert_fail = 1
                                self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                                self.print_color('assert_fail', a, case[4])
                        elif case[2] == u'text':
                            a = str(self.s(name=case[3]).get(timeout=ELEM_TIMEOUT).text)
                            if a == case[4]:
                                self.print_color('assert', a, case[4])
                            else:
                                self.flag_assert_fail = 1
                                self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                                self.print_color('assert_fail', a, case[4])
                        elif case[2] == u'className':
                            a = str(self.s(name=case[3]).get(timeout=ELEM_TIMEOUT).className)
                            if a == case[4]:
                                self.print_color('assert', a, case[4])
                            else:
                                self.flag_assert_fail = 1
                                self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                                self.print_color('assert_fail', a, case[4])
                        elif case[2] == u'label':
                            a = str(self.s(name=case[3]).get(timeout=ELEM_TIMEOUT).label)
                            if a == case[4]:
                                self.print_color('assert', a, case[4])
                            else:
                                self.flag_assert_fail = 1
                                self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                                self.print_color('assert_fail', a, case[4])
                    else:
                        if case[2] == u'value':
                            a = str(self.s(name=case[3], index=int(case[5])).get(timeout=ELEM_TIMEOUT).value)
                            if a == case[4]:
                                self.print_color('assert', a, case[4])
                            else:
                                self.flag_assert_fail = 1
                                self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                                self.print_color('assert_fail', a, case[4])
                        elif case[2] == u'text':
                            a = str(self.s(name=case[3], index=int(case[5])).get(timeout=ELEM_TIMEOUT).text)
                            if a == case[4]:
                                self.print_color('assert', a, case[4])
                            else:
                                self.flag_assert_fail = 1
                                self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                                self.print_color('assert_fail', a, case[4])
                        elif case[2] == u'className':
                            a = str(self.s(name=case[3], index=int(case[5])).get(timeout=ELEM_TIMEOUT).className)
                            if a == case[4]:
                                self.print_color('assert', a, case[4])
                            else:
                                self.flag_assert_fail = 1
                                self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                                self.print_color('assert_fail', a, case[4])
                        elif case[2] == u'label':
                            a = str(self.s(name=case[3], index=int(case[5])).get(timeout=ELEM_TIMEOUT).label)
                            if a == case[4]:
                                self.print_color('assert', a, case[4])
                            else:
                                self.flag_assert_fail = 1
                                self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                                self.print_color('assert_fail', a, case[4])
                elif case[1] == u'xpath':
                    if case[2] == u'value':
                        a = str(self.s(xpath=case[3]).get(timeout=ELEM_TIMEOUT).value)
                        if a == case[4]:
                            self.print_color('assert', a, case[4])
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                            self.print_color('assert_fail', a, case[4])
                    elif case[2] == u'text':
                        a = str(self.s(xpath=case[3]).get(timeout=ELEM_TIMEOUT).text)
                        if a == case[4]:
                            self.print_color('assert', a, case[4])
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                            self.print_color('assert_fail', a, case[4])
                    elif case[2] == u'className':
                        a = str(self.s(xpath=case[3]).get(timeout=ELEM_TIMEOUT).className)
                        if a == case[4]:
                            self.print_color('assert', a, case[4])
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                            self.print_color('assert_fail', a, case[4])
                    elif case[2] == u'label':
                        a = str(self.s(xpath=case[3]).get(timeout=ELEM_TIMEOUT).label)
                        if a == case[4]:
                            self.print_color('assert', a, case[4])
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '断言失败!返回结果:%s,期望结果:%s' % (a, case[4])
                            self.print_color('assert_fail', a, case[4])
            elif case[0] == u'存在':
                if case[1] == u'name':
                    if len(case) == 3:
                        if self.s(name=case[2]).exists:
                            self.print_color('exists', '成功!元素存在')
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '判断控件存在失败!'
                            self.print_color('e_fail', '失败!元素未找到')
                    else:
                        if self.s(name=case[2], index=int(case[3])).exists:
                            self.print_color('exists', '成功!元素存在')
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '判断控件存在失败!'
                            self.print_color('e_fail', '失败!元素未找到')
                elif case[1] == u'xpath':
                    if self.s(xpath=case[2]).exists:
                        self.print_color('exists', '成功!元素存在')
                    else:
                        self.flag_assert_fail = 1
                        self.assert_info = '判断控件存在失败!'
                        self.print_color('e_fail', '失败!元素未找到')
            elif case[0] == u'不存在':
                if case[1] == u'name':
                    if len(case) == 3:
                        if self.s(name=case[2]).wait_gone(10, raise_error=False):
                            self.print_color('exists', '成功!元素不存在')
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '判断控件不存在失败!'
                            self.print_color('e_fail', '失败!元素存在')
                    else:
                        if self.s(name=case[2], index=int(case[3])).wait_gone(10, raise_error=False):
                            self.print_color('exists', '成功!元素不存在')
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '判断控件不存在失败!'
                            self.print_color('e_fail', '失败!元素存在')
                elif case[1] == u'xpath':
                    if self.s(xpath=case[2]).wait_gone(10, raise_error=False):
                        self.print_color('exists', '成功!元素不存在')
                    else:
                        self.flag_assert_fail = 1
                        self.assert_info = '判断控件不存在失败!'
                        self.print_color('e_fail', '失败!元素存在')
            elif case[0] == u'上滚':
                if len(case) == 4:
                    if case[1] == u'name':
                        self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='up', distance=float(case[3]))
                    elif case[1] == u'xpath':
                        self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='up', distance=float(case[3]))
                    elif case[1] == u'label':
                        self.s(label=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='up', distance=float(case[3]))
                else:
                    self.s(name=case[2], index=int(case[4])).get(timeout=ELEM_TIMEOUT).scroll(direction='up',
                                                                                    distance=float(case[3]))
            elif case[0] == u'下滚':
                if len(case) == 3:
                    if case[1] == u'name':
                        self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='down', distance=float(case[3]))
                    elif case[1] == u'xpath':
                        self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='down', distance=float(case[3]))
                    elif case[1] == u'label':
                        self.s(label=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='down', distance=float(case[3]))
                else:
                    self.s(name=case[2], index=int(case[4])).get(timeout=ELEM_TIMEOUT).scroll(direction='down',
                                                                                    distance=float(case[3]))
            elif case[0] == u'左滚':
                if len(case) == 3:
                    if case[1] == u'name':
                        self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='left', distance=float(case[3]))
                    elif case[1] == u'xpath':
                        self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='left', distance=float(case[3]))
                    elif case[1] == u'label':
                        self.s(label=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='left', distance=float(case[3]))
                else:
                    self.s(name=case[2], index=int(case[4])).get(timeout=ELEM_TIMEOUT).scroll(direction='left',
                                                                                    distance=float(case[3]))
            elif case[0] == u'右滚':
                if len(case) == 3:
                    if case[1] == u'name':
                        self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='right', distance=float(case[3]))
                    elif case[1] == u'xpath':
                        self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='right', distance=float(case[3]))
                    elif case[1] == u'label':
                        self.s(label=case[2]).get(timeout=ELEM_TIMEOUT).scroll(direction='right', distance=float(case[3]))
                else:
                    self.s(name=case[2], index=int(case[4])).get(timeout=ELEM_TIMEOUT).scroll(direction='right',
                                                                                    distance=float(case[3]))
            elif case[0] == u'捏':
                if case[1] == u'name':
                    if len(case) == 5:
                        self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).pinch(scale=float(case[3]), velocity=float(case[4]))
                    else:
                        self.s(name=case[2], index=int(case[5])).get(timeout=ELEM_TIMEOUT).pinch(scale=int(case[3]),
                                                                                            velocity=int(case[4]))
                elif case[1] == u'xpath':
                    self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).pinch(scale=float(case[3]), velocity=float(case[4]))
            elif case[0] == u'是否激活':
                if case[1] == u'name':
                    if len(case) == 4:
                        a = str(self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).enabled)
                        if a == case[3]:
                            self.print_color('assert', a, case[3])
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '判断是否激活失败!返回结果:%s,期望结果:%s' % (a, case[3])
                            self.print_color('assert_fail', a, case[3])
                    else:
                        a = str(self.s(name=case[2], index=int(case[4])).get(timeout=ELEM_TIMEOUT).enabled)
                        if a == case[3]:
                            self.print_color('assert', a, case[3])
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '判断是否激活失败!返回结果:%s,期望结果:%s' % (a, case[3])
                            self.print_color('assert_fail', a, case[3])
                elif case[1] == u'xpath':
                    a = str(self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).enabled)
                    if a == case[3]:
                        self.print_color('assert', a, case[3])
                    else:
                        self.flag_assert_fail = 1
                        self.assert_info = '判断是否激活失败!返回结果:%s,期望结果:%s' % (a, case[3])
                        self.print_color('assert_fail', a, case[3])
            elif case[0] == u'是否可见':
                if case[1] == u'name':
                    if len(case) == 4:
                        a = str(self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).displayed)
                        if a == case[3]:
                            self.print_color('assert', a, case[3])
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '判断是否可见失败!返回结果:%s,期望结果:%s' % (a, case[3])
                            self.print_color('assert_fail', a, case[3])
                    else:
                        a = str(self.s(name=case[2], index=int(case[4])).get(timeout=ELEM_TIMEOUT).displayed)
                        if a == case[3]:
                            self.print_color('assert', a, case[3])
                        else:
                            self.flag_assert_fail = 1
                            self.assert_info = '判断是否可见失败!返回结果:%s,期望结果:%s' % (a, case[3])
                            self.print_color('assert_fail', a, case[3])
                elif case[1] == u'xpath':
                    a = str(self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).displayed)
                    if a == case[3]:
                        self.print_color('assert', a, case[3])
                    else:
                        self.flag_assert_fail = 1
                        self.assert_info = '判断是否可见失败!返回结果:%s,期望结果:%s' % (a, case[3])
                        self.print_color('assert_fail', a, case[3])
            elif case[0] == u'获取坐标':
                if case[1] == u'name':
                    bounds = self.s(name=case[2]).get(timeout=ELEM_TIMEOUT).bounds
                    x = bounds.x
                    y = bounds.y
                    width = bounds.width
                    height = bounds.height
                elif case[1] == u'xpath':
                    bounds = self.s(xpath=case[2]).get(timeout=ELEM_TIMEOUT).bounds
                    x = bounds.x
                    y = bounds.y
                    width = bounds.width
                    height = bounds.height
            else:
                self.print_color('other', '来我工位,扫码支付5毛,告诉我你[%s]谁定义的...' % case[0])
                return False
            if self.flag_assert_fail == 1:
                self.write_log('fail', case[0], self.assert_info)
            else:
                self.write_log('success', case[0])
        except TypeError:
            return False
        except Exception as e:
            path = self.get_path() + '/var/screen-err/' + self.module + '-' + self.case
            self.media.screenshot('%s.png' % path)

            if 'parameter not satisfying' in str(e):
                _e = 'Please try to increase the wait.'
            else:
                _e = e
            self.write_log('error', case[0], str(_e).replace('\n', ''))
            self.print_color('error', _e)
            self.flag_err = 1
            self.err_info = _e
            pass

    def alert_callback(self, session):
        bt = set(ALERT).intersection(session.alert.buttons())
        if len(bt) == 0:
            raise RuntimeError("Alert can not handled, buttons: " + ', '.join(session.alert.buttons()))
        session.alert.click(list(bt)[0])

    def get_path(self):
        import os
        return str(os.getcwd())

    def data(self, type, operate):
        data = dict()
        data['告警类型'] = type
        data['监控模块'] = self.module
        data['监控case'] = self.case
        data['告警事件'] = operate
        if self.flag_assert == 1 and self.flag_warn == 0:
            data['告警信息'] = str(self.assert_info)
        elif self.flag_assert == 0 and self.flag_warn == 1:
            data['告警信息'] = str(self.err_info)
        data['告警时间'] = time.strftime('%Y.%m.%d %H:%M:%S ')
        import json
        return json.dumps(data, indent=1, sort_keys=False, ensure_ascii=False)

    def print_color(self, type, para=None, para_1=None, para_2=None):
        if PRINT:
            time_color = '\033[1;37;0m' + time.strftime('%Y-%m-%d %H:%M:%S ') + '\033[0m'
            module = ' ' + self.module + '  ' + self.case + '  '
            if type == 'info':
                print '\033[1;37;0m[INFO]  ' + para + '\033[0m'
            elif type == 'error':
                print time_color + '\033[1;35;0m[ERROR] ' + str(para) + '\033[0m'
            elif type == 'run':
                print time_color + '\033[1;32;0m[RUN] ' + module + para + '\033[0m'
            elif type == 'assert':
                print time_color + '\033[1;33;0m[ASSERT] ' + '  返回值:' + para + '-期望值:' + para_1 + '\033[0m'
            elif type == 'assert_fail':
                print time_color + '\033[1;31;0m[A_FAIL] ' + '  返回值:' + para + '-期望值:' + para_1 + '\033[0m'
            elif type == 'exists':
                print time_color + '\033[1;33;0m[EXISTS] ' + para + '\033[0m'
            elif type == 'e_fail':
                print time_color + '\033[1;31;0m[E_FAIL] ' + para + '\033[0m'
            elif type == 'other':
                print time_color + '\033[1;36;0m[OTHER]  ' + para + '\033[0m'
            else:
                print '\033[1;36;0m 打印类型 print颜色,了解一下 \033[0m'

    def write_log(self, status, event, err=None):
        with open(self.get_path() + '/var/log/' + str(time.strftime('%Y%m%d')) + '.log', 'a') as a:
            if err:
                a.write(str(
                        time.strftime(
                                '%Y-%m-%d %H:%M:%S ')) + self.module + ' ' + self.case + ' ' + event + ' ' + status + ' ' + err + '\n')
            else:
                a.write(str(time.strftime(
                        '%Y-%m-%d %H:%M:%S ')) + self.module + ' ' + self.case + ' ' + event + ' ' + status + '\n')
            a.close()
            pass
