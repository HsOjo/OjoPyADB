import pyadb
from pyadb.adb.sub_command.base import BaseSubCommand


class Logcat(BaseSubCommand):
    FORMAT_BRIEF = 'brief'
    FORMAT_HELP = 'help'
    FORMAT_LONG = 'long'
    FORMAT_PROCESS = 'process'
    FORMAT_RAW = 'raw'
    FORMAT_TAG = 'tag'
    FORMAT_THREAD = 'thread'
    FORMAT_THREAD_TIME = 'threadtime'
    FORMAT_TIME = 'time'

    PRIORITY_VERBOSE = 'V'
    PRIORITY_DEBUG = 'D'
    PRIORITY_INFO = 'I'
    PRIORITY_WARN = 'W'
    PRIORITY_ERROR = 'E'
    PRIORITY_FATAL = 'F'
    PRIORITY_SILENT = 'S'

    def __init__(self, adb: 'pyadb.ADB'):
        super().__init__(adb, 'logcat')
        self._tags = None
        self._filterspecs = {}

    def set_format(self, *format):
        if len(format) == 1 and format[0] is None:
            self._tags = None
        else:
            self._tags = list(format)

    def set_filterspecs(self, **tag_priority):
        self._filterspecs = tag_priority

    def dump(self, *args, **kwargs):
        filterspecs = None
        if len(self._filterspecs) > 0:
            filterspecs = "%s" % (' '.join(['%s:%s' % (k, v) for k, v in self._filterspecs.items()]))
        args = [
                   '-d', '-s' if filterspecs is not None else None,
                   '-v' if self._tags is not None else None,
                   ','.join(self._tags) if self._tags is not None else None
               ] + list(args) + [filterspecs]
        return self.execute_out(*args, **kwargs)

    def clear(self):
        self.execute('-c')
