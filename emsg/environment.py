# -*- coding: UTF-8 -*-

environments = []

def environment(func):
    env = Environment(func.__name__)
    env.description = func.__doc__
    environments.append(env)
    func(env)
    return func

class Environment(object):
    def __init__(self, name):
        self.name = name
        self.description = None
        self.path = []
        self.var = {}
        self.cmd = []

    def batch_cmd(self):
        bat = ['ECHO {}'.format(self.description)]
        if self.path:
            bat.append('SET PATH={};%PATH%'.format(';'.join(env.path)))
        return '\t' + '\r\n\t'.join(bat) + '\r\n'

