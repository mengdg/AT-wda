# encoding: utf-8
"""
    __auth__: 孟德功
    __require__: 所有事件二次封装
    __version__: 无要求
"""


class Event:
    def __init__(self, media=None):
        self.media = media

    def click(self, type, button_name):
        self.media(type, button_name).click()

    def set_text_name(self, local, text):
        self.media(name=local).set_text(text)

    def set_text_xpath(self, local, text):
        self.media(xpath=local).set_text(text)

    def wait(self, timeout=20.0):
        import time
        time.sleep(timeout)

    def close(self):
        self.media.close()

    def deactivate(self, timeout=5.0):
        self.media.deactivate(timeout)

    def tap(self, x, y):
        self.media.tap(x=x, y=y)

    def double_tap(self, x, y):
        self.media.double_tap(x, y)

    def swipe(self, x1, y1, x2, y2, time=0.5):
        self.media.swipe(x1, y1, x2, y2, time)

    def swipe_left(self):
        self.media.swipe_left()

    def swipe_right(self):
        self.media.swipe_right()

    def swipe_up(self):
        self.media.swipe_up()

    def swipe_down(self):
        self.media.swipe_down()

    def tap_hold(self, x, y, time=1.0):
        self.media.tap_hold(x=x, y=y, time=time)

        # def

        # self.media.wait(timeout)
