# AT-wda

自动化 WebDriverAgent python 项目(2018/4/27)

主要功能:
* `Excel` 编写自动化case
   /支持多sheet
   /支持多Excel
   /支持case跳过
   /支持case钉钉报警
* 自动找设备
* 自动连接设备
* 自动xcodebuild
* 每个case执行完成，重启app
* 支持case异常/断言错误
* 处理不定时弹出的警告
* 控制台展示运行日志
* 日志记录
* case执行异常后截图
* 多机并行(暂未实现)

大部分的工作已经完成, 还有部分问题还会持续更新

项目基于开源的facebook-wda [openatx/facebook-wda](https://github.com/openatx/facebook-wda)

## 安装
1. 请下载 WebDriverAgent 安装并配置

	下载地址 <https://github.com/facebook/WebDriverAgent>
	配置地址 <https://testerhome.com/topics/7220>

2. 请下载 [AT-wad](https://github.com/mengdg/AT-wda)

3. 请安装 usbmuxd 以便于通过 USB 通道测试 iOS 真机，不需要测试真机则不用安装

    ```python
        brew install usbmuxd
    ```

4. 请安装元素查看器

* Macaca app-inspector

    ```python
        DEVELOPMENT_TEAM_ID=****** npm install macaca-ios -g
    ```

* WebDriverAgent 自带inspector <http://localhost/8100/inspector>

## 配置

请打开文件 /AT-wda/lib/setting.py

```python

FILES = ['group', 'login']  # 选择所要执行/AT-wda/case中的文件名
BUNDLE_ID = 'com.blued.international'   # App bundle id
PRINT = True    # 打印case运行日志
DEVICE = 1  # 选择第一台(目前仅支持单台设备,若插入多个设备,可以自行选择其中一台执行)
ALERT = [u'不再提醒', 'OK', u'知道了', 'Allow', u'允许', u'稍后', u'好']    # 处理不知何时就会突然弹出的警告框,可以根据业务拓展
WDA_PATH = '/Users/degongmeng/Documents/Macaca/WebDriverAgent/WebDriverAgent.xcodeproj' # WebDriverAgent.xcodeproj 的绝对路径
DD_TOKEN = '*********************************************'  # 钉钉的token(在钉钉pc版中可以获取机器人的token)
ELEM_TIMEOUT = 20    # 获取元素最大等待时长

```

## Tests
测试用例放在 `/AT-wda/case/` 目录下
* 请打开文件 /AT-wda/case/group.xlsx

| module | 模块名 | case | case名 | is_run | 1 | is_warning | 0 |
|--------|--------|--------|--------|--------|--------|--------|--------|
| 等待 | 2 | | | | | | |
| 点击 | name | Done | | | | | |

    `module`后的表格填写模块名
    `case`后的表格填写case名
    `is_run`后的表格填写是否运行该case(是 1 否 0)
    `is_warning`后的表格填写是否运行失败后报警(是 1 否 0)

## 目前支持的 event

```python
ok 点击  name/xpath/label    定位元素    索引(可选,默认0,xpath无需加索引)
ok 输入  name/xpath  定位元素    输入的内容   索引(可选,默认0,xpath无需加索引)
ok 清除  name/xpath  定位元素    索引(可选,默认0,xpath无需加索引)
ok 等待  时长(s)
ok 截图
ok 停用  时长(s)   #停用时app置后台
ok 坐标长按    x   y   时长(s)
ok 坐标点击    x   y
ok 坐标双击    x   y
ok 坐标拖拽    x   y   tox     toy     持续时长(s)
ok 长按  name/xpath  定位元素    时长(s)   索引(可选,默认0,xpath无需加索引)
ok 双击  name/xpath  定位元素    索引(可选,默认0,xpath无需加索引)
ok 左划
ok 右划
ok 上划
ok 下划
ok 断言  name/xpath  value/text/className(文本控件值类型)    定位元素    期望value/text/className   索引(可选,默认0,xpath无需加索引)
ok 存在  name/xpath  定位元素    索引(可选,默认0,xpath无需加索引)
ok 不存在    name/xpath 定位元素  索引(可选,默认0,xpath无需加索引)
ok 捏   name/xpath  定位元素    比例  速度  索引(可选,默认0,xpath无需加索引)
ok 是否激活    name/xpath  定位元素    期望结果    索引(可选,默认0,xpath无需加索引)
ok 是否可见    name/xpath  定位元素    期望结果    索引(可选,默认0,xpath无需加索引)
```

## Run

运行测试用例
```python
/AT-wda/main.py
```

## 查看结果
* 控制台可以查看到运行结果
* 运行日志存在 /AT-wda/var/log
* 查看截图 /AT-wda/var/screenshot
* 查看异常截图 /AT-wda/var/screen-err
