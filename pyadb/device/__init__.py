import pyadb
from .helper import *
from ..adb import Forward, Reverse, Logcat


class Device:
    def __init__(self, adb: 'pyadb.PyADB', sn):
        self._adb = adb
        self._sn = sn

    def do(self, call):
        return self._adb.do(self, call)

    def execute(self, *args, **kwargs):
        [stat, out, err] = self.do(lambda adb: adb.shell(*args, **kwargs))
        return stat, out, err

    def execute_out(self, *args, **kwargs):
        [_, out, _] = self.execute(*args, **kwargs)
        return out

    @property
    def sn(self):
        return self._sn

    @property
    def adb(self):
        return self._adb

    @property
    def state(self):
        return self.do(lambda adb: adb.get_state())

    @property
    def abi(self):
        return self.execute_out('getprop', 'ro.product.cpu.abi')

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

    @property
    def forward(self) -> Forward:
        return self.do(lambda adb: adb.forward)

    @property
    def reverse(self) -> Reverse:
        return self.do(lambda adb: adb.reverse)

    @property
    def logcat(self) -> Logcat:
        return self.do(lambda adb: adb.logcat)

    def __repr__(self):
        return '<Device %s>' % self._sn
