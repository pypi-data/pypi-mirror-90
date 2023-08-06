import os


from .utils import bz2, try_callback, raise_err
from . import ssh


def device(key, mode='v'):
    return Device(key, mode)


class Device():

    def __init__(self, key, mode='verbose'):
        self.__key = key
        self.__tid = None
        _msg_levels = ('n', 'c', 'e', 'v')
        assert mode in _msg_levels
        self._output_level = _msg_levels.index(mode)
        self.local_root = './clones'
        self.device_root = '~/clones'

    def __enter__(self):
        if not os.path.exists(self.local_root):
            os.makedirs(self.local_root)
        with self.__handler__('n') as f:
            f.call(f'mkdir {self.device_root}')
            f.cd(self.device_root)
            f.call(f'mkdir todo;mkdir env')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __handler__(self, mode):
        return ssh.open(self.__key, mode=mode)

    def call(self, command, mode='v'):
        with ssh.open(self.__key, mode=mode) as f:
            _, err_ = f.cd(self.device_root)
            out, err = f.call(command)
        return out, err_ + err

    def commit(self, src, tid=None, ignore=r'.*\.(pdf|dio|png|gif)'):
        return bz2.compress(src, self.local_root, ignore, tid)

    def checkout(self, tid):
        self.__tid = tid
        return tid

    @raise_err
    @try_callback
    def fetch(self, tid=None):
        if tid is None:
            tid = self.__tid
        assert tid is not None
        with self.__handler__('e') as f:
            f.cd(self.device_root + '/env')
            f.tarc(tid + '.tar.bz2', tid)
            f.mv(tid + '.tar.bz2', f'local:{self.local_root}/{tid}.tar.bz2')
        os.system(f'tar -jxvf {self.__root}/{tid}.tar.bz2 -C {self.__root}; rm {self.__root}/{tid}.tar.bz2')

    @raise_err
    @try_callback
    def push(self):
        with self.__handler__('e') as f:
            f.cd(self.device_root + '/todo')
            for branch in os.listdir(self.local_root):
                if branch.endswith('.tar.bz2'):
                    f.cp(f'local:{self.local_root}/{branch}', branch)
        os.system(f'rm -r {self.local_root}/*.tar.bz2')

    @raise_err
    @try_callback
    def pull(self):
        with self.__handler__('e') as f:
            f.cd(self.device_root)
            f.tarc('env.tar.bz2', './env')
            f.mv('env.tar.bz2', f'local:{self.local_root}/env.tar.bz2')
            f.call(f'rm ./env/* -r')
        os.system(f'tar -jxvf {self.local_root}/env.tar.bz2 -C {self.local_root};')
        os.system(f'rm {self.local_root}/env.tar.bz2; mv {self.local_root}/env/* {self.local_root}/; rm {self.local_root}/env -r')

    @raise_err
    @try_callback
    def ls(self, tid=None, pipe=None):
        if tid is None:
            tid = self.__tid
        assert tid is not None
        with self.__handler__('v') as f:
            f.cd(self.device_root + '/env')
            f.call(f'cat {tid}/log'+('' if pipe is None else f'|{pipe}'))

    @raise_err
    @try_callback
    def run(self, script):
        with self.__handler__('v') as f:
            f.cd(self.device_root + '/env')
            f.cp('local:'+script, './god.py')
            f.call(f'nohup python -u god.py >log 2>&1 &')
