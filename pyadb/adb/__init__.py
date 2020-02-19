import re

from pyadb import common
from pyadb.utils import ShellLib
from .sub_command import *


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
                raise FileNotFoundError("Couldn't find ADB.")

        super().__init__(path)

        self._current_device = None

    @property
    def devices(self):
        out = self.execute_out('devices')
        devices = {}
        for line in out.splitlines()[1:]:
            device = re.match(r'(?P<device>.+)\s+(?P<state>.+)', line)
            if device is not None:
                device = device.groupdict()
                devices[device['device']] = device['state']
        return devices

    @property
    def version(self):
        out = self.execute_out('version')
        version = re.match(r'Android Debug Bridge version (?P<adb_version>.+)\nVersion (?P<sdk_version>.+)', out)
        if version is not None:
            version = version.groupdict()
        return version

    @property
    def _device_args(self):
        args = []
        if self._current_device is not None:
            args += ['-s', self._current_device]
        return args

    @property
    def current_device(self):
        return self._current_device

    def set_current_device(self, value):
        if value in self.devices:
            self._current_device = value

    def device_execute(self, *args, **kwargs):
        p_args = self._device_args + list(args)
        return self.execute(*p_args, **kwargs)

    def device_execute_out(self, *args, **kwargs):
        p_args = self._device_args + list(args)
        return self.execute_out(*p_args, **kwargs)

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
        out = self.device_execute_out('push', *local, remote, '--sync' if sync else None)
        result = re.findall(r'(\d+) files? pushed', out)
        if len(result) == 1:
            [num] = result
            return int(num) == len(local)

        return False

    def pull(self, *remote, local='./', preserve: bool = True):
        out = self.device_execute_out('pull', *remote, local, '-a' if preserve else None)
        result = re.findall(r'(\d+) files? pulled', out)
        if len(result) == 1:
            [num] = result
            return int(num) == len(local)

        return False

    def shell(self, *command, escape: str = None, no_stdin=False, disable_pty_alloc=False, force_pty_alloc=False,
              disable_exec_separation=False, **kwargs):
        return self.device_execute('shell',
                                   '-e %s' % escape if escape is not None else None,
                                   '-n' if no_stdin else None,
                                   '-T' if disable_pty_alloc else None,
                                   '-t' if force_pty_alloc else None,
                                   '-x' if disable_exec_separation else None,
                                   *command, **kwargs)

    def exec_out(self, *command, **kwargs):
        return self.device_execute('exec-out', *command, **kwargs)

    def install(self, package: str):
        return 'Success' in self.device_execute_out(
            'install', package,
        )

    def uninstall(self, package: str, keep_data=False):
        return 'Success' in self.device_execute_out(
            'uninstall', package,
            '-k' if keep_data else None
        )

    def reboot(self, mode: str):
        return self.device_execute('reboot', mode)

    def tcpip(self, port: int):
        return self.device_execute('tcpip', port)

    def usb(self):
        return self.device_execute('usb')

    def start_server(self):
        return self.execute('start-server')

    def kill_server(self):
        return self.execute('kill-server')

    def root(self):
        return self.device_execute('root')

    def unroot(self):
        return self.device_execute('unroot')

    def sideload(self, ota_package: str):
        return self.device_execute('sideload', ota_package)

    def get_state(self):
        return self.device_execute_out('get-state')

    def copy(self, device=None):
        obj = self.__class__(path=self.path)
        obj._current_device = self._current_device if device is None else device
        return obj

    @property
    def forward(self):
        return Forward(self.copy())

    @property
    def reverse(self):
        return Reverse(self.copy())

    @property
    def logcat(self):
        return Logcat(self.copy())
