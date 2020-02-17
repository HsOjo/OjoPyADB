from .base import BaseHelper


class FileHelper(BaseHelper):
    def pull(self, *args, **kwargs):
        return self.device.do(lambda adb: adb.pull(*args, **kwargs))

    def push(self, *args, **kwargs):
        return self.device.do(lambda adb: adb.push(*args, **kwargs))

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
