#!/usr/bin/env python
# License: GPLv3 Copyright: 2023, Kovid Goyal <kovid at kovidgoyal.net>


from bypy.utils import cmake_build,ModifiedEnv


def main(args):
#
	with ModifiedEnv( 
	    CMAKE_LIBRARY_PATH='/sw/sw/lib:/opt/cross/usr/lib',
	):
		cmake_build()
