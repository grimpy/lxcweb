# all the imports
import subprocess
import os
import re

IPREC = re.compile("^\s+inet\s(?P<ip>.*?)\/", re.M)


def command(cmd, *args):
    cargs = [ cmd ]
    cargs.extend(args)
    return subprocess.check_output(cargs)

class LXC(object):
    def __init__(self, path='/var/lib/lxc'):
        self._path = path

    def list(self):
        names = command("lxc-ls", "-x").strip().split()
        machines = [ Machine(name, self._path) for name in names ]
        return machines

    def getMachine(self, name):
        return Machine(name, self._path)


class Machine(object):

    WAITMAP = {'start': 'RUNNING', 'freeze': 'FROZEN', 'unfreeze': 'RUNNING', 'stop': 'STOPPED'}

    def __init__(self, name, basepath, status=None):
        self.name = name
        self._path = os.path.join(basepath, name)
        self._status = status
        self._ip = None

    def _action(self, action, wait=True, extra=None):
        args = ["-n", self.name]
        if extra:
            args.extend(extra)
        result = command("lxc-%s" % action, *args)
        if wait and action in self.WAITMAP:
            command('lxc-wait', "-n", self.name, "-s", self.WAITMAP[action])
        return result

    @property
    def ip(self):
        if not self._ip:
            if self.get_status() == 'RUNNING':
                ipinfo = command("lxc-attach", "-s", "NETWORK", "-n", self.name, "--", "ip", "a", "s", "dev", "eth0")
                for match in IPREC.finditer(ipinfo):
                    self._ip = match.group('ip')
                    break
            else:
                self._ip = 'N/A'
        return self._ip

    def start(self, wait=True):
        return self._action('start', wait, ['-d'])

    def stop(self, wait=True):
        return self._action('stop', wait)

    def clone(self, newname):
        return command('lxc-clone', '-o', self.name, '-n', newname)

    def get_status(self, reload=False):
        if not self._status or reload:
            self._status = command("lxc-info", "-n", self.name, "-s").strip().split()[-1]
        return self._status

    def delete(self):
        self._action('destroy')

    status = property(fget=get_status)

