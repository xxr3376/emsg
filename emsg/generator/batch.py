# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

import os
import sys
import string
import codecs
import time
import datetime

template = string.Template('''\
@ECHO OFF
rem Environment Management Scripts Generator - $time

IF /I NOT "%~1" == "" \
IF /I NOT "%~1" == "-h" \
IF /I NOT "%~1" == "--help" \
IF /I NOT "%~1" == "/?" (
    GOTO update
)

ECHO %0 ENV [ENV...]
ECHO %0 [-u^|--update]
ECHO %0 [-e^|--edit]
ECHO.
$help
EXIT /B

:update
IF /I NOT "%~1" == "-u" \
IF /I NOT "%~1" == "--update" \
IF /I NOT "%~1" == "/u" (
    GOTO edit
)
                           
ECHO Updating Script...
PUSHD $emsg_root
"$python_exe" -m emsg --output "$output" "$config" & \
POPD & \
EXIT /B

:edit
IF /I NOT "%~1" == "-e" \
IF /I NOT "%~1" == "--edit" \
IF /I NOT "%~1" == "/e" (
    GOTO main
)

SET _EMSG_TEMP=%TEMP%\_emsg.%RANDOM%.txt

COPY $config %_EMSG_TEMP% & \
%EDITOR% %_EMSG_TEMP% & \
COPY %_EMSG_TEMP% $config & \
CALL %0 -u & \
EXIT /B

:main
$main

TITLE %_ENVS%%~1
SET "_ENVS=%_ENVS%%~1 "

:nextarg
IF "%2" == "" EXIT /B
CALL %0 %2 %3 %4 %5 %6 %7 %8 %9
''')

def generate(envs, args):
    output = args.output
    if output != '-':
        output = os.path.abspath(output)

    data = {
        'help': generate_help(envs),
        'main': generate_main(envs),
        'emsg_root': os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')),
        'python_exe': sys.executable,
        'output': output,
        'config': os.path.abspath(args.config),
        'time': datetime.datetime.fromtimestamp(time.time()),
    }

    rst = template.substitute(**data)
    rst = rst.replace('\n', os.linesep)
    if output == '-':
        sys.stdout.write(rst)
    else:
        with codecs.open(output, 'wb', sys.getfilesystemencoding()) as out:
            out.write(rst)

def generate_help(envs):
    info = []
    name_len = 1
    for env in envs:
        if env.description:
            name_len = max(name_len, len(env.name))
            description = ' - ' + env.description
        else:
            description = ''
        info.append((env.name, description))

    fmt = 'ECHO     {:' + str(name_len) + 's}{}'
    return '\n'.join(fmt.format(*i) for i in info)

def generate_main(envs):
    rst = ''
    for env in envs:
        body = []

        if env.var:
            for name, value in env.var.viewitems():
                body.append('SET "{}={}"'.format(name, value))

        if env.path:
            body.append('SET "PATH={};%PATH%"'.format(';'.join(env.path)))

        if env.cmd:
            body.append('\n    '.join(env.cmd))

        if env.description:
            description = env.description
        else:
            description = env.name
        body.append('ECHO {}'.format(description))

        rst += 'IF /I "%~1" == "{}" (\n    {}\n) ELSE '.format(env.name, '\n    '.join(body))
    rst += '(\n    ECHO Invalid Argument\n    GOTO nextarg\n)'
    return rst

