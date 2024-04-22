#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from bypy.utils import simple_build
#
import os

needs_lipo = True


def main(args):
#
	if os.path.exists('/opt/armv7l-linux-musleabihf-cross'):
	    simple_build('--disable-udev --disable-dependency-tracking --disable-static --build=i686-linux --host=arm-linux ', no_parallel=True, use_cross_host=False)
	else:
		simple_build('--disable-udev --disable-dependency-tracking --disable-static ', no_parallel=True)
