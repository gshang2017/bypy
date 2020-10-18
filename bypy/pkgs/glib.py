#!/usr/bin/env python2
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

import os
from bypy.constants import LIBDIR, PREFIX
from bypy.utils import meson_build, ModifiedEnv, apply_patch


def main(args):
    with ModifiedEnv(
            LD_LIBRARY_PATH=LIBDIR,
            PATH=f'{PREFIX}/bin:' + os.environ['PATH']
    ):
        os.makedirs(
            os.path.join(f'{PREFIX}/lib/dbus-1.0/include'), exist_ok=True)
        #ggettext.c:(.text+0x5db): undefined reference to `libintl_dngettext'
        apply_patch('glib/glib-musl-libintl.patch')
        meson_build(
            force_posix_threads='true', internal_pcre='true', gtk_doc='false',
            man='false', selinux='disabled', iconv='external')
