#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from bypy.constants import iswindows, NMAKE, LIBDIR
from bypy.utils import simple_build, run, install_binaries, ModifiedEnv
#
import os

needs_lipo = True


def main(args):
    if iswindows:
        run(f'"{NMAKE}" -f build\\visualc.mk')
        install_binaries('src\\optipng\\optipng.exe', 'bin',
                         fname_map=lambda x: 'optipng-calibre.exe')
    else:
    	#simple_build('-with-system-libs', use_envvars_for_lipo=True)
#
    if os.path.exists('/opt/armv7l-linux-musleabihf-cross'):
        with ModifiedEnv(
            LD='/opt/armv7l-linux-musleabihf-cross/bin/armv7l-linux-musleabihf-gcc',
        ):
            simple_build('-with-system-libs', use_envvars_for_lipo=True, use_cross_host=False)

    else: 
         with ModifiedEnv(
            LD='/opt/aarch64-linux-musl-cross/bin/aarch64-linux-musl-gcc',
        ):
            simple_build('-with-system-libs', use_envvars_for_lipo=True, use_cross_host=False)
