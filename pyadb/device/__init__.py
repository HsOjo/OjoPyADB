from .helper import *


class Device:
    def __init__(self, adb, sn):
        self._adb = adb
        self.sn = sn

    def do(self, call):
        return self._adb.do(self, call)

    def execute(self, *args, **kwargs):
        [stat, out, err] = self.do(lambda adb: adb.shell(*args, **kwargs))
        return stat, out, err

    def execute_out(self, *args, **kwargs):
        [_, out, _] = self.execute(*args, **kwargs)
        return out

    @property
    def state(self):
        return self.do(lambda adb: adb.get_state())

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
    def display(self):
        return DisplayHelper(self)

    def __repr__(self):
        return '<Device %s>' % self.sn
