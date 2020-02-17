# OjoPyAdb

This project is written with Python 3, which aims to provide a simple and practical ADB function for Python 3.

## Introduction

The module currently integrates the following functions:

* Application management (installation, uninstall, start, stop, clear data, freeze, get status, etc.)
* File management (pull, push, copy, move, delete, view and other basic functions)
* Input control (text, key, click, slide)
* Display management (adjust resolution, DPI, screenshot)

In the future, corresponding functions will be added according to the requirements.

## How to use

As shown below.

### Installation

1. Open the [release page](https://github.com/hsojo/ojopyadb/releases) to find the latest version of the installation file.

2. (Optional) download to this machine through browser, and then use **PIP** to execute the following command to install.

```bash
pip install OjoPyADB-0.0.1-py3-none-any.whl
```

3. Of course, you can also directly copy the download link of the installation package and use **pip** for online installation. (execute the following command)

```bash
# Note: that the link here is version 0.0.1, please replace it with the latest version.
pip install https://github.com/HsOjo/OjoPyADB/releases/download/0.0.1/OjoPyADB-0.0.1-py3-none-any.whl
```

### Instance code

Here are some simple usage. For specific parameters, please refer to the code prompt of IDE. Try more.

```python3
from pyadb import PyADB, KeyCode

adb = PyADB()
print(adb.version)
print(adb.devices)
if len(adb.devices) > 0:
    device = adb.devices[0]
    print(device.sn, device.state)
    print(device.app.current_activity)
    print(device.input.keyevent(KeyCode.HOME))
    print(device.input.keyevent(KeyCode.SEARCH))
    print(device.input.text('Hello World!\tThis input method is ASCII only...'))
    print(device.file.listdir('/sdcard/'))
    print(device.display.size())
    img = device.display.screen_cap()
    print(len(img))
```
