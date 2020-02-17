import os
import time
import traceback
from io import StringIO
from subprocess import PIPE, Popen, TimeoutExpired


def popen(cmd, sys_env=True, **kwargs):
    if isinstance(cmd, list):
        for i in range(len(cmd)):
            if not isinstance(cmd[i], str):
                cmd[i] = str(cmd[i])

    kwargs.setdefault('encoding', 'utf-8')
    kwargs.setdefault('stdin', PIPE)
    kwargs.setdefault('stdout', PIPE)
    kwargs.setdefault('stderr', PIPE)

    if sys_env and kwargs.get('env') is not None:
        kwargs['env'] = os.environ.copy().update(kwargs['env'])
    return Popen(cmd, **kwargs)


def execute(cmd, input_str=None, timeout=None, **kwargs):
    p = popen(cmd, **kwargs)
    try:
        out, err = p.communicate(input_str, timeout=timeout)
    except TimeoutExpired:
        out = ''
        err = get_exception()
        p.kill()
    stat = p.returncode

    if isinstance(out, str):
        out = out.rstrip('\n')
    return stat, out, err


def get_exception():
    with StringIO() as io:
        traceback.print_exc(file=io)
        io.seek(0)
        content = io.read()

    return content


def time_count(func):
    def core(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print('%s time usage: %f' % (func.__name__, time.time() - t))
        return result

    return core
