#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>

import os

from bypy.constants import PREFIX, islinux
from ..utils import ModifiedEnv, qt_build, apply_patch


def main(args):
  env = {}   
  env['PATH'] = '/opt/aarch64-linux-musl-cross/bin:' + os.environ['PATH']
  with ModifiedEnv(**env):
    qt_build()
