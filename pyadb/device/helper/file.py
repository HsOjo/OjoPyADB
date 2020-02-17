from .base import BaseHelper


class FileHelper(BaseHelper):
    def pull(self, *args, **kwargs):
        return self.device.do(lambda adb: adb.pull(*args, **kwargs))

    def push(self, *args, **kwargs):
        return self.device.do(lambda adb: adb.push(*args, **kwargs))

    def listdir(self, *path):
        out:str = self.device.exec_out('ls', *path)
        result = out.splitlines()
        return result

    def delete(self, *path):
        [stat, _, _] = self.device.exec('rm', '-fr', *path)
        return stat == 0

    def copy(self, *src, dest):
        [stat, _, _] = self.device.exec('cp', '-fr', *src, dest)
        return stat == 0

    def move(self, *src, dest):
        [stat, _, _] = self.device.exec('mv', '-f', *src, dest)
        return stat == 0
