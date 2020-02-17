import re

from .base import BaseHelper


class AppHelper(BaseHelper):
    def install(self, package):
        return self.device.do(lambda adb: adb.install(package))

    def uninstall(self, package):
        return self.device.do(lambda adb: adb.uninstall(package))

    def pm(self, *args, **kwargs):
        return self.device.exec('pm', *args, **kwargs)

    def am(self, *args, **kwargs):
        return self.device.exec('am', *args, **kwargs)

    def list(self, system_only=False, third_only=True, enabled_only=False, disabled_only=False):
        p_args = [
            'list', 'packages',
            '-s' if system_only else None,
            '-3' if third_only else None,
            '-e' if enabled_only else None,
            '-d' if disabled_only else None,
        ]
        [_, out, _] = self.pm(p_args)
        result = re.findall('package:(.*)', out)
        return result

    def enable(self, package):
        [_, out, _] = self.pm('enable', package)
        return 'enabled' in out

    def disable(self, package):
        [_, out, _] = self.pm('disable', package)
        return 'disabled' in out

    def set_hidden(self, package, hidden):
        if hidden:
            [_, out, _] = self.pm('hide', package)
            return 'true' in out
        else:
            [_, out, _] = self.pm('unhide', package)
            return 'false' in out

    def info(self, package):
        out = self.device.exec_out('dumpsys', 'package', package)
        return out

    def start(self, intent):
        [stat, _, _] = self.am('start', intent)
        return stat == 0
