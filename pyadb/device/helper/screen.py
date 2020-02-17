import base64

from .base import BaseHelper


class ScreenHelper(BaseHelper):
    def cap(self) -> bytes:
        [_, out, _] = self.device.exec('screencap -p|base64', encoding=None)
        out = base64.b64decode(out)
        return out
