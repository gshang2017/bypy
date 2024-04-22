#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

from bypy.utils import simple_build, replace_in_file
from ..constants import islinux

def main(args):
#
    if islinux:
        replace_in_file(
        'Makefile.am',
        'SUBDIRS = dbus-gmain dbus tools test doc',
        'SUBDIRS = dbus-gmain dbus')   
        replace_in_file(
        'Makefile.in',
        'SUBDIRS = dbus-gmain dbus tools test doc',
        'SUBDIRS = dbus-gmain dbus')            
        replace_in_file(
        'dbus/Makefile.am',
        'SUBDIRS = . examples',
        'SUBDIRS = .')
        replace_in_file(
        'dbus/Makefile.in',
        'SUBDIRS = . examples',
        'SUBDIRS = .')
    simple_build('--disable-dependency-tracking --disable-static')
