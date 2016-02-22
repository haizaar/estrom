#!/usr/bin/env python

import sys
import argparse
from importlib import import_module

from estrom import roadrunner, logging
from settings import settings as s

if __name__ == "__main__":
    logging.setup(s.logging)
    parser = argparse.ArgumentParser(
        description="Run particular Autobahn module"
    )
    parser.add_argument("module",
                        help="""Name of the module from estrom directory.
                                The module must implement Component class.""")

    args = parser.parse_args()
    module = import_module("estrom."+args.module, package="estrom")
    roadrunner.run_componenet(module.Component)
