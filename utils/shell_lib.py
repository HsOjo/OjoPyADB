import common


class ShellLib:
    def __init__(self, path):
        self.path = path
        self.last_exec = None

    def exec_out(self, *args, **kwargs):
        [_, out, _] = self.exec(*args, **kwargs)
        return out

    def exec(self, *args, **kwargs):
        p_args = [arg for arg in args if arg is not None]
        [stat, out, err] = common.execute([self.path, *p_args], **kwargs)
        self.last_exec = {'status': stat, 'stdout': out, 'stderr': err}
        return stat, out, err

    def popen(self, *args, **kwargs):
        return common.popen([self.path, *args], **kwargs)
