from .base import BaseHelper


class FileHelper(BaseHelper):
    def pull(self, *remote, local='./', preserve: bool = True):
        params = self.params(locals())
        return self.device.do(lambda adb: adb.pull(*params.pop('remote'), **params))

    def push(self, *local, remote='/sdcard/', sync: bool = False):
        params = self.params(locals())
        return self.device.do(lambda adb: adb.push(*params.pop('local'), **params))

    def listdir(self, *path):
        out: str = self.device.execute_out('ls', *path)
        result = out.splitlines()
        return result

    def delete(self, *path):
        [stat, _, _] = self.device.execute('rm', '-fr', *path)
        return stat == 0

    def copy(self, *src, dest):
        [stat, _, _] = self.device.execute('cp', '-fr', *src, dest)
        return stat == 0

    def move(self, *src, dest):
        [stat, _, _] = self.device.execute('mv', '-f', *src, dest)
        return stat == 0
