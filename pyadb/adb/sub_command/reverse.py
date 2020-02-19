import pyadb
from .mapping import Mapping


class Reverse(Mapping):
    def __init__(self, adb: 'pyadb.ADB'):
        super().__init__(adb, 'reverse')
