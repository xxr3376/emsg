# -*- coding: UTF-8 -*-

import os
import sys
import argparse
import importlib

from emsg.environment import environments

def main():
    parser = argparse.ArgumentParser(prog='python -m emsg',
                                     description='Environment Management Scripts Generator')
    parser.add_argument('config', help='path to configuration script')
    parser.add_argument('--output', default='-', help='path to output script, default to stdout')
    parser.add_argument('--generator', help='path to output script, default to stdout')
    args = parser.parse_args()

    sys.path.append(os.path.dirname(args.config))
    execfile(args.config)

    if args.generator:
        generator = args.generator
    else:
        # TODO choose most appropriate generator
        generator = 'batch'

    generate = importlib.import_module('emsg.generator.' + generator).generate
    generate(environments, args)

if __name__ == "__main__":
    main()

