import re

from .base import BaseHelper


class AppHelper(BaseHelper):
    def install(self, package):
        return self.device.do(lambda adb: adb.install(package))

    def uninstall(self, package):
        return self.device.do(lambda adb: adb.uninstall(package))

    def pm(self, *args, **kwargs):
        return self.device.execute('pm', *args, **kwargs)

    def list(self, system_only=False, third_only=True, enabled_only=False, disabled_only=False):
        p_args = [
            'list', 'packages',
            '-s' if system_only else None,
            '-3' if third_only else None,
            '-e' if enabled_only else None,
            '-d' if disabled_only else None,
        ]
        [_, out, _] = self.pm(*p_args)
        result = re.findall(r'package:(.*)', out)
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

    def clear(self, package):
        [_, out, _] = self.pm('clear', package)
        return 'Success' in out

    def info(self, package):
        out = self.pm('dump', package)
        return out

    def am(self, *args, **kwargs):
        return self.device.execute('am', *args, **kwargs)

    def start(self, intent):
        [_, _, err] = self.am('start', intent)
        return err != ''

    def start_by_package(self, package):
        [_, _, err] = self.device.do(
            lambda adb: adb.shell('monkey', '-p', package, '-c', 'android.intent.category.LAUNCHER', '1'))
        return err != ''

    def force_stop(self, package):
        [_, _, err] = self.am('force-stop', package)
        return err != ''

    @property
    def current_activity(self):
        logcat = self.device.do(lambda adb: adb.logcat)
        logcat.set_filterspecs(**{'ActivityManager': logcat.PRIORITY_INFO})
        logcat.set_format(logcat.FORMAT_TAG)
        out = logcat.dump()  # type: str
        out = out[out.rfind('START'):]
        out = out[out.find('cmp='):out.find('\n')]
        item = re.match('cmp=(?P<intent>(?P<package>\S+)/(?P<activity>\S+))', out)
        if item is not None:
            item = item.groupdict()
        return item
