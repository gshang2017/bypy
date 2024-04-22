#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>



from bypy.constants import PREFIX, ismacos, iswindows
from bypy.utils import cmake_build, simple_build, ModifiedEnv


def main(args):
    if ismacos or iswindows:
        cmake_build(
            LIBXSLT_WITH_PYTHON='OFF', LIBXML2_INCLUDE_DIR=f'{PREFIX}/include',
            relocate_pkgconfig=False
        )
    else:
#
         with ModifiedEnv(
            CFLAGS='-I/sw/sw/include -I/opt/cross/usr/include',
            LDFLAGS='-L/sw/sw/lib -Wl,-rpath-link,/sw/sw/lib -L/opt/cross/usr/lib -Wl,-rpath-link,/opt/cross/usr/lib',
       ):
            simple_build(
                '--disable-dependency-tracking --disable-static'
                ' --enable-shared --without-python --without-debug')
