import re

from pyadb import common
from pyadb.utils import ShellLib


class ADB(ShellLib):
    MODE_BOOTLOADER = 'bootloader'
    MODE_RECOVERY = 'recovery'
    MODE_SIDELOAD = 'sideload'
    MODE_SIDELOAD_AUTO_REBOOT = 'sideload-auto-reboot'

    STATE_DEVICE = 'device'
    STATE_BOOTLOADER = 'bootloader'
    STATE_OFFLINE = 'offline'

    def __init__(self, path=None):
        if path is None:
            [_, path, _] = common.execute(['which', 'adb'])
            if path == '':
                raise FileNotFoundError("Couldn't find adb.")

        super().__init__(path)

        self._current_device = None

    @property
    def devices(self):
        out = self.execute_out('devices')
        devices = {}
        for line in out.splitlines()[1:]:
            device = re.match('(?P<device>.+)\s+(?P<state>.+)', line)
            if device is not None:
                device = device.groupdict()
                devices[device['device']] = device['state']
        return devices

    @property
    def version(self):
        out = self.execute_out('version')
        version = re.match('Android Debug Bridge version (?P<adb_version>.+)\nVersion (?P<sdk_version>.+)', out)
        if version is not None:
            version = version.groupdict()
        return version

    @property
    def _common_args(self):
        args = []
        if self._current_device is not None:
            args += ['-s', self._current_device]
        return args

    @property
    def current_device(self):
        return self._current_device

    @current_device.setter
    def current_device(self, value):
        if value in self.devices:
            self._current_device = value

    def connect(self, host, port=None):
        if port is not None:
            target = '%s:%s' % (host, port)
        else:
            target = host
        out = self.execute_out('connect', target)
        return 'connected' in out

    def disconnect(self, host, port=None):
        if port is not None:
            target = '%s:%s' % (host, port)
        else:
            target = host
        out = self.execute_out('disconnect', target)
        return 'disconnected' in out

    def reconnect(self, host, port=None):
        if port is not None:
            target = '%s:%s' % (host, port)
        else:
            target = host
        self.execute('reconnect', target)

    def push(self, *local, remote='/sdcard/', sync: bool = False):
        p_args = self._common_args + ['push', *local, remote, '--sync' if sync else None]
        out = self.execute_out(*p_args)
        result = re.findall('(\d+) files pushed', out)

        if len(result) == 1:
            [num] = result
            return int(num) == len(local)

        return False

    def pull(self, *remote, local='./', preserve: bool = True):
        p_args = self._common_args + ['pull', *remote, local, '-a' if preserve else None]
        out = self.execute_out(*p_args)
        result = re.findall('(\d+) files pulled', out)

        if len(result) == 1:
            [num] = result
            return int(num) == len(local)

        return False

    def shell(self, *command, escape: str = None, no_stdin=False, disable_pty_alloc=False, force_pty_alloc=False,
              disable_exec_separation=False, **kwargs):
        p_args = self._common_args + [
            'shell',
            '-e %s' % escape if escape is not None else None,
            '-n' if no_stdin else None,
            '-T' if disable_pty_alloc else None,
            '-t' if force_pty_alloc else None,
            '-x' if disable_exec_separation else None,
            *command
        ]
        return self.execute(*p_args, **kwargs)

    def exec_out(self, *command, **kwargs):
        p_args = self._common_args + ['exec-out', *command]
        return self.execute(*p_args, **kwargs)

    def install(self, package: str):
        p_args = self._common_args + ['install', package]
        return 'Success' in self.execute_out(*p_args)

    def uninstall(self, package: str, keep_data=False):
        p_args = self._common_args + [
            'uninstall', package,
            '-k' if keep_data else None
        ]
        return 'Success' in self.execute_out(*p_args)

    def reboot(self, mode: str):
        p_args = self._common_args + ['reboot', mode]
        self.execute(*p_args)

    def tcpip(self, port: int):
        p_args = self._common_args + ['tcpip', port]
        self.execute(*p_args)

    def usb(self):
        p_args = self._common_args + ['usb']
        self.execute(*p_args)

    def start_server(self):
        self.execute('start-server')

    def kill_server(self):
        self.execute('kill-server')

    def root(self):
        p_args = self._common_args + ['root']
        self.execute(*p_args)

    def unroot(self):
        p_args = self._common_args + ['unroot']
        self.execute(*p_args)

    def sideload(self, ota_package: str):
        p_args = self._common_args + ['sideload', ota_package]
        return self.execute(*p_args)

    def get_state(self):
        return self.execute_out('get-state')
