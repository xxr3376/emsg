# -*- coding: UTF-8 -*-

import ConfigParser

from emsg.environment import environment

class EnvWrapper(object):
    def __init__(self, attr):
        self.__name__ = 'EnvWrapper'
        self.attr = attr

    def __call__(self, env):
        for k in self.attr:
            env.__setattr__(k, self.attr[k])

def parse_config_file(filename):
    with open(filename) as f:
        config = ConfigParser.ConfigParser()
        config.readfp(f)
        for sec in config.sections():
            if sec.find(':') >= 0:
                name, description = sec.split(':', 2)
            else:
                name = description = sec

            env = {
                'name': name,
                'description': description,
            }

            var = env['var'] = dict(config.items(sec))
            if 'path' in var:
                env['path'] = filter(None, var.pop('path').split('\n'))
            if 'cmd' in var:
                env['cmd'] = filter(None, var.pop('cmd').split('\n'))

            environment(EnvWrapper(env))

