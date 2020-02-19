from pyadb import common


class ShellLib:
    def __init__(self, path):
        self.path = path
        self.last_exec = None

    def execute_out(self, *args, **kwargs):
        [_, out, _] = self.execute(*args, **kwargs)
        return out

    def execute(self, *args, **kwargs):
        p_args = [arg for arg in args if arg is not None]
        [stat, out, err] = common.execute([self.path, *p_args], **kwargs)
        self.last_exec = {
            'args': p_args, 'status': stat, 'stdout': out, 'stderr': err,
            'exec': ' '.join(str(i) for i in [self.path, *p_args])
        }
        return stat, out, err

    def popen(self, *args, **kwargs):
        return common.popen([self.path, *args], **kwargs)
