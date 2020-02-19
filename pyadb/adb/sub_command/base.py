import pyadb


class BaseSubCommand:
    def __init__(self, adb: 'pyadb.ADB', command: str):
        self._adb = adb
        self._command = command

    @property
    def adb(self):
        return self._adb

    def execute(self, *args, **kwargs):
        [stat, out, err] = self._adb.device_execute(self._command, *args, **kwargs)
        return stat, out, err

    def execute_out(self, *args, **kwargs):
        [_, out, _] = self.execute(*args, **kwargs)
        return out
