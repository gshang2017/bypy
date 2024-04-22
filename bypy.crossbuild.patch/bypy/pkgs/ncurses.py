#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

#from bypy.constants import PKG_CONFIG_PATH, build_dir, PKG_CONFIG_LIBDIR
from bypy.constants import build_dir, PKG_CONFIG_LIBDIR
from bypy.utils import simple_build, ModifiedEnv, apply_patch


def main(args):
    # make install tries to write to $HOME/.terminfo
    #apply_patch('cleanup-pkgconfig-ldflags.patch', level=1)
    with ModifiedEnv(HOME=build_dir()):
        simple_build(
            '--with-shared --without-debug --without-ada --enable-widec'
            ' --with-normal --enable-pc-files -without-tests --disable-stripping'
            #f' --with-pkg-config-libdir={PKG_CONFIG_PATH}'
#
            f' --with-pkg-config-libdir={PKG_CONFIG_LIBDIR}'
            
            # without the following ncurses will look in the BUILD_DIR
            # for terminfo files even on target systems. Instead use
            # a bunch of common locations.
            ' --with-terminfo-dirs=/usr/share/terminfo:/etc/terminfo:'
            '/lib/terminfo:/usr/lib/terminfo'
            ' --with-default-terminfo-dir=/usr/share/terminfo'
        )


def filter_pkg(parts):
    return (
        'terminfo' in parts or 'tabset' in parts or 'bin' in parts or
        '.terminfo' in parts
    )
