import pyadb
from .mapping import Mapping


class Forward(Mapping):
    def __init__(self, adb: 'pyadb.ADB'):
        super().__init__(adb, 'forward')

    def dev(self, device: str):
        return self.bind_execute('dev:%s' % device)

    def jdwp(self, pid: int):
        return self.bind_execute('jdwp:%s' % pid)
