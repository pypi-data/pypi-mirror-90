

import os
from functools import wraps
import paramiko
import base64

from .utils import try_callback, raise_err


class Tunnel():
    _status_head = (
        '          ',
        '[ \033[1;32m  ok  \033[0m ]',
        '[ \033[1;31mfailed\033[0m ]',
    )

    def __init__(self, key, mode='verbose'):
        self.__key = key
        self.__client = None
        self.__root = '~'
        _msg_levels = ('n', 'c', 'e', 'v')  # nothing < command < error < verbose
        assert mode in _msg_levels
        self._output_level = _msg_levels.index(mode.lower()[0])

    @staticmethod
    def decode(key: str):
        sequence = base64.b64decode(key)
        return str(sequence, 'utf8').split('$')

    @staticmethod
    def connect(key):
        ssh = paramiko.SSHClient()  # 创建sshclient
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 指定当对方主机没有本机公钥的情况时应该怎么办，AutoAddPolicy表示自动在对方主机保存下本机的秘钥
        ssh.connect(*Tunnel.decode(key))
        return ssh

    @staticmethod
    def sftp_callback(transferred, total):
        print(f'\r{Tunnel._status_head[0]} transferred/total: {transferred}/{total} ({transferred/total:%})', end='')

    @staticmethod
    def ssh_callback(level, line=None, status=None, root=None, refresh_status=None):
        if level > 0:
            if refresh_status is not None:
                print('\r'+Tunnel._status_head[refresh_status])
            elif status is not None:
                print(f'{status} {root}$ {line}', end='')
            else:
                print(f'{Tunnel._status_head[0]} {line}', end='')

    def callback(func):
        @wraps(func)
        def core(self, command):
            # ('nothing', 'command', 'error', 'verbose') = 0, 1, 2, 3
            if command.startswith('mv') or command.startswith('cp'):
                Tunnel.ssh_callback(self._output_level, command+'\n', self._status_head[1], self.__root)  # sftp related command returns ok as default
                out, err = func(self, command)
                print('\n', end='')
                return out, err
            Tunnel.ssh_callback(self._output_level, command, self._status_head[0], self.__root)
            out, err = func(self, command)
            Tunnel.ssh_callback(self._output_level, refresh_status=(2 if len(err) > 0 else 1))
            for line in err:
                Tunnel.ssh_callback(self._output_level-1, str(line))
            for line in out:
                Tunnel.ssh_callback(self._output_level-2, line)
            return out, err
        return core

    def __enter__(self):
        self.__client = self.connect(self.__key)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__client.close()

    def __call__(self, command):
        _, stdout, stderr = self.__client.exec_command(f'. /etc/profile;. .bashrc;cd {self.__root};{command}')
        out = stdout.readlines()
        err = stderr.readlines()
        return out, err

    @raise_err
    @try_callback
    def __upload__(self, local, remote):
        with self.__client.open_sftp() as sftp:
            sftp.put(local, remote, callback=self.sftp_callback)

    @raise_err
    @try_callback
    def __download__(self, remote, local):
        with self.__client.open_sftp() as sftp:
            sftp.get(remote, local, callback=self.sftp_callback)

    @raise_err
    @try_callback
    def __nativecall__(self, command):
        os.system(command)

    @callback
    def call(self, command):
        out, err = [], []
        # supports for 'cd' command, allows relocating before each call.
        if command.startswith('cd'):
            out, err = self.__call__(command)
            if len(err) == 0:
                self.__root = command.split(' ')[-1]
                self.__root = self.__call__('pwd')[0][0].replace('\n', '')
            return out, err
        # hyper supports for 'mv' command, allows 'local:' pattern for sftp.
        if command.startswith('mv') or command.startswith('cp'):
            _, a, b = command.split(' ')
            if a.startswith('local:'):
                a = a.split('local:')[-1]
                b = self.__root + '/' + b
                self.__upload__(a, b)
                if command.startswith('mv'):
                    self.__nativecall__(f'rm {a}')
            elif b.startswith('local:'):
                b = b.split('local:')[-1]
                a = self.__root + '/' + a
                self.__download__(a, b)
                if command.startswith('mv'):
                    out, err = self.__call__(f'rm {a}')
            else:
                out, err = self.__call__(f'mv {a} {b}')
            return out, err
        return self.__call__(command)

    def cd(self, dir):
        return self.call('cd ' + dir)

    def tarc(self, src, target):
        return self.call('tar -jcvf ' + src + ' ' + target)

    def tarx(self, src, target):
        return self.call('tar -jxvf ' + src + ' -C ' + target)

    def mv(self, src, target):
        return self.call('mv ' + src + ' ' + target)

    def cp(self, src, target):
        return self.call('cp ' + src + ' ' + target)


def keygen(ip_address, user, password, port=22):
    sequence = f'{ip_address}${port}${user}${password}'
    return str(base64.b64encode(sequence.encode('utf8')), 'utf8')


def open(key, mode='v'):
    return Tunnel(key, mode)
