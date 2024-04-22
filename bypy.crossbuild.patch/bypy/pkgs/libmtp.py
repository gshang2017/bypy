#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

from bypy.constants import PREFIX, LDFLAGS, CFLAGS, LIBDIR, islinux
from bypy.utils import simple_build, ModifiedEnv,replace_in_file


needs_lipo = True

# apk add libmtp-examples libmtp
def main(args):
#
    if islinux:
        replace_in_file(
            'Makefile.am',
            'util/mtp-hotplug',
            '/usr/bin/mtp-hotplug')
    with ModifiedEnv(
            LIBUSB_CFLAGS="-I%s/include/libusb-1.0" % PREFIX,
            LIBUSB_LIBS='-lusb-1.0',
            CFLAGS=CFLAGS + ' -DHAVE_ICONV',
            LDFLAGS=LDFLAGS + ' -liconv',
    ):
        conf = '--disable-mtpz --disable-dependency-tracking --disable-static --with-libiconv-prefix={0}'.format(PREFIX)
        if islinux:
             conf += '   --with-udev={0}/udev'.format(PREFIX)
        simple_build(conf)
