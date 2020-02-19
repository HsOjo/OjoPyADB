# OjoPyADB

该项目使用 Python3 编写，目的在于为 Python3 提供简单、实用的 ADB 功能。

## 功能简介

该模块目前集成了以下功能：

* 应用管理（安装、卸载、启动、停止、清除数据、冻结、获取状态等一系列操作）
* 文件管理（拉取、推送、复制、移动、删除、查看等基本功能）
* 输入控制（文字、按键、点击、滑动）
* 显示管理（调整分辨率、DPI、截屏）

日后将根据需求往里添加相应功能。

## 如何使用

如下所示。

### 安装

* 从 0.0.3 版本开始，该模块将上传到 pypi，你也可以直接使用 pip 进行安装。

```bash
pip install OjoPyADB
```

#### 手动安装

1. 打开[Release 页面](https://github.com/HsOjo/OjoPyADB/releases)，找到最新版本的安装文件。

2. （可选）通过浏览器下载到本机，然后使用 **pip** 执行以下命令，进行安装。

```bash
pip install OjoPyADB-0.0.1-py3-none-any.whl
```

* 当然，你也可以直接复制安装包的下载链接，使用 **pip** 进行在线安装。（执行以下命令）

```bash
# 注意，这里的链接为 0.0.1 版本，请自行替换成最新版本。
pip install https://github.com/HsOjo/OjoPyADB/releases/download/0.0.1/OjoPyADB-0.0.1-py3-none-any.whl
```

### 实例代码

以下是一些简单的用法，具体参数可以参考 IDE 的代码提示，多尝试便可。

```python3
from pyadb import PyADB, KeyCode

adb = PyADB()
print(adb.version)
print(adb.devices)
print(adb.forward.list)
if len(adb.devices) > 0:
    device = list(adb.devices.values())[0]
    print(device.abi)
    print(device.sn, device.state)
    print(device.app.current_activity)
    print(device.input.keyevent(KeyCode.HOME))
    print(device.input.keyevent(KeyCode.SEARCH))
    device.input.text('Hello World!\tThis input method is ASCII only...')
    print(device.file.listdir('/sdcard/'))
    print(device.display.size())
    img = device.display.screen_cap()
    print(len(img))
    logcat = device.logcat
    logcat.set_filterspecs(**{'ActivityManager': logcat.PRIORITY_INFO})
    print(logcat.dump())
```
