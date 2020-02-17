from pyadb.adb import ADB
from pyadb.device import Device, KeyCode


class PyAdb(ADB):
    @property
    def devices(self):
        devices = []
        for sn in super().devices:
            device = Device(self, sn)
            devices.append(device)
        return devices

    @property
    def current_device(self):
        return Device(self, super().current_device)

    @current_device.setter
    def current_device(self, value):
        if isinstance(value, Device):
            self._current_device = value.sn

    def do(self, device: Device, call):
        _device = self._current_device
        self._current_device = device.sn
        result = call(self)
        self._current_device = _device
        return result


if __name__ == '__main__':
    adb = PyAdb()
    # adb.kill_server()
    # adb.start_server()

    print(adb.devices)
    print(adb.version)
    print(adb.push('/Users/hsojo/Downloads/Python网络爬虫权威指南（第2版）.pdf', remote='/sdcard/test/'))

    device = adb.devices[0]
    print(device.file.listdir('/sdcard/'))
    print(device.app.list())
    print(device.app.info(device.app.list()[2]))
    print(adb.last_exec)
    print(len(device.screen.cap()))
