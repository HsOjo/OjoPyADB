from .helper import *


class Device:
    def __init__(self, adb, sn):
        self._adb = adb
        self.sn = sn

    def do(self, call):
        return self._adb.do(self, call)

    def exec(self, *args, **kwargs):
        [stat, out, err] = self.do(lambda adb: adb.shell(*args, **kwargs))
        return stat, out, err

    def exec_out(self, *args, **kwargs):
        [_, out, _] = self.exec(*args, **kwargs)
        return out

    @property
    def status(self):
        return self._adb.devices[self.sn]

    @property
    def file(self):
        return FileHelper(self)

    @property
    def app(self):
        return AppHelper(self)

    @property
    def input(self):
        return InputHelper(self)

    @property
    def screen(self):
        return ScreenHelper(self)

    def __repr__(self):
        return '<Device %s>' % self.sn
