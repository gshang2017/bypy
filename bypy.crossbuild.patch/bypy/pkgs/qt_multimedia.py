#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>

import os

from ..utils import qt_build, apply_patch
from bypy.constants import islinux

def main(args):
#
    if islinux:
        apply_patch('select.patch', level=1)
    qt_build(dep_name='qt-multimedia')
