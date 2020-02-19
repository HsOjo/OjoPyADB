import re

from .base import BaseHelper


class DisplayHelper(BaseHelper):
    def screen_cap(self, display_id=None) -> bytes:
        p_args = [
            'screencap', '-p',
            ('-d %s' % display_id) if display_id is not None else None,
        ]
        [_, out, _] = self.device.do(lambda adb: adb.exec_out(*p_args, encoding=None))
        return out

    def wm(self, *args, **kwargs):
        return self.device.execute('wm', *args, **kwargs)

    def size(self, physical=False):
        [_, out, _] = self.wm('size')
        out: str
        size = {}
        for line in out.splitlines():
            item = re.match(r'(?P<key>.*?) size: (?P<width>\d+)x(?P<height>\d+)', line)
            if item is not None:
                size[item['key']] = (int(item['width']), int(item['height']))

        if not physical:
            return size.get('Override', size['Physical'])
        else:
            return size['Physical']

    def set_size(self, width=None, height=None):
        if width is None and height is None:
            self.wm('size', 'reset')
        else:
            w, h = self.size()
            self.wm('size', '%sx%s' % (w if width is None else width, h if height is None else height))

    def set_density(self, density=None):
        if density is None:
            self.wm('density', 'reset')
        else:
            self.wm('density', density)
