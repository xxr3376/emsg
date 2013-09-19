# -*- coding: UTF-8 -*-

from emsg.api import *

@environment
def test(env):
    '''Description for test'''
    env.path.append('__PATH__')
    env.cmd.append('__CMD__')
    env.var['__VAR__'] = 'VALUE'

