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

    def clear(self, package):
        [_, out, _] = self.pm('clear', package)
        return 'Success' in out

    def info(self, package):
        out = self.device.execute_out('dumpsys', 'package', package)
        return out

    def get_main_intent(self, package):
        info = self.info(package)  # type: str
        activity = []
        found = False
        for line in info.splitlines():
            if found:
                item = re.match('\s*\S+ (?P<intent>(?P<package>\S+)/(?P<activity>\S+))', line)
                if item is not None:
                    activity.append(item.groupdict())
                else:
                    break
            else:
                if 'android.intent.action.MAIN' in line:
                    found = True

        if len(activity) > 1:
            return activity
        elif len(activity) > 0:
            return activity[0]
        else:
            return None

    def am(self, *args, **kwargs):
        return self.device.execute('am', *args, **kwargs)

    def start(self, intent):
        [stat, _, _] = self.am('start', intent)
        return stat == 0

    def force_stop(self, package):
        [stat, _, _] = self.am('force-stop', package)
        return stat == 0

    @property
    def current_activity(self):
        out = self.device.execute_out('dumpsys activity activities | grep mFocusedActivity')
        item = re.match(
            '\s+mFocusedActivity: ActivityRecord{\S+ \S+ (?P<intent>(?P<package>\S+)/(?P<activity>\S+)) \S+}', out)
        if item is not None:
            item = item.groupdict()
        return item
