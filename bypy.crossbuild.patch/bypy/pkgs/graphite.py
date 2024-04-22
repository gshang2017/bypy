#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2020, Kovid Goyal <kovid at kovidgoyal.net>

import os
import re

from ..constants import CMAKE, PREFIX, build_dir, islinux
from ..utils import ModifiedEnv, replace_in_file, run


def main(args):
    if islinux:
           replace_in_file(
            'src/CMakeLists.txt',
            'add_definitions(-mfpmath=sse -msse2)',
            'add_definitions()')
    os.mkdir('build')
    os.chdir('build')
#
    with ModifiedEnv( 
            LDFLAGS='-L/sw/sw/lib -Wl,-rpath-link,/sw/sw/lib -L/opt/cross/usr/lib -Wl,-rpath-link,/opt/cross/usr/lib',
       ):
        cmd = [
            CMAKE, '-G', 'Unix Makefiles', '-Wno-dev',
            '-DCMAKE_BUILD_TYPE=RELEASE',  
#
            '-DCMAKE_LIBRARY_PATH=sw/sw/lib;/opt/cross/usr/lib' ,  
            '-DCMAKE_INSTALL_PREFIX=' + build_dir(), '-Wno-dev', '..'
        ]
        run(*cmd)
        run('make')
        run('make install')
        replace_in_file(
            os.path.join(build_dir(), 'lib/pkgconfig/graphite2.pc'),
            re.compile(re.escape(build_dir())), PREFIX)
