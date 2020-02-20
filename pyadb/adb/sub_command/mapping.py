import re
from typing import Dict

import pyadb
from .base import BaseSubCommand


class Mapping(BaseSubCommand):
    def __init__(self, adb: 'pyadb.ADB', command: str):
        super().__init__(adb, command)
        self._no_rebind = True

    def bind_execute(self, *args, **kwargs):
        if self._no_rebind:
            args = ['--no-rebind'] + list(args)
        [_, _, err] = self.execute(*args, **kwargs)
        return err == ''

    @property
    def list(self):
        out = self.execute_out('--list')  # type: str
        items = {}  # type: Dict[str,list]
        for line in out.splitlines():
            item = re.match(
                r'(?P<device>\S+)\s+(?P<local>(?P<local_type>\S+):(?P<local_value>\S+))\s+(?P<remote_type>\S+):(?P<remote_value>\S+)',
                line
            )
            if item is not None:
                item = item.groupdict()
                device = item.pop('device')
                if item['local_type'] == 'tcp':
                    item['local_value'] = int(item['local_value'])
                if item['remote_type'] == 'tcp':
                    item['remote_value'] = int(item['remote_value'])
                if items.get(device) is None:
                    items[device] = []
                items[device].append(item)

        sn = self._adb.current_sn
        if sn is not None:
            return items[sn]
        else:
            return items

    def tcp(self, local_port: int, remote_port: int):
        return self.bind_execute('tcp:%s' % local_port, 'tcp:%s' % remote_port)

    def local_abstract(self, socket: str):
        return self.bind_execute('localabstract:%s' % socket)

    def local_reserved(self, socket: str):
        return self.bind_execute('localreserved:%s' % socket)

    def local_filesystem(self, socket: str):
        return self.bind_execute('localfilesystem:%s' % socket)

    def remove(self, local: str):
        [_, _, err] = self.execute('--remove', local)
        return err == ''

    def remove_all(self, current_device_only=True):
        if current_device_only:
            items = self.list
            if isinstance(items, list):
                b = True
                for item in items:
                    b = self.remove(item['local']) and b
                return b

        [_, _, err] = self.execute('--remove-all')
        return err == ''
