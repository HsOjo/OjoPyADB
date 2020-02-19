from pyadb.adb import ADB
from pyadb.device import Device, KeyCode


class PyADB(ADB):
    @property
    def devices(self):
        devices = {}
        for sn, state in super().devices.items():
            devices[sn] = Device(self, sn)
        return devices

    @property
    def current_device(self):
        return Device(self, super().current_device)

    def set_current_device(self, device: Device):
        if isinstance(device, Device):
            self._current_device = device.sn

    def do(self, device: Device, call):
        _device = self._current_device
        self._current_device = device.sn
        result = call(self)
        self._current_device = _device
        return result


if __name__ == '__main__':
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
        print(device.input.text('Hello World!\tThis input method is ASCII only...'))
        print(device.file.listdir('/sdcard/'))
        print(device.display.size())
        img = device.display.screen_cap()
        print(len(img))
