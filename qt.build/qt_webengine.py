#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>

import glob
import os

from bypy.constants import PREFIX, MAKEOPTS, islinux, iswindows
from bypy.utils import qt_build, replace_in_file, apply_patch, run


def main(args):
    os.chdir('/src')
    qtwebenginebuilddir='/src/qt-webengine-build'
    if not os.path.exists(qtwebenginebuilddir):
        os.makedirs(qtwebenginebuilddir)
        qtwebengine_files = list(glob.glob('/sources/qtwebengine-everywhere-src-*.tar.xz'))
        run(f'tar -xf "{qtwebengine_files[0]}" --strip-components=1  -C /src/qt-webengine-build')
        os.chdir('/src/qt-webengine-build')
        # workaround for bug in build system, not adding include path for
        # libjpeg when building iccjpeg, and mjpeg_decoder
        #jpeg_files = list(glob.glob(f'{PREFIX}/include/*jpeg*.h'))
        #jpeg_files += [
        #    f'{PREFIX}/include/{x}.h'
        #    for x in 'jerror jconfig jmorecfg'.split()
        #]
        #for header in jpeg_files:
        #    os.symlink(
        #        header,
        #        os.path.join('src/3rdparty/chromium',
        #                     os.path.basename(header)))
        # https://chromium-review.googlesource.com/c/v8/v8/+/2136489
        ##apply_patch('qt-webengine-icu67.patch'),
        #apply_patch('qt-webengine/qt-webengine-icu67.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-mallinfo.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-siginfo_t.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-pread-pwrite.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-fpstate.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-sysreg-for__WORDSIZE.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-stackstart.patch'),
        apply_patch('qt-webengine/qt-webengine-nasm.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-hacks.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-resolve.patch'),
        apply_patch('qt-webengine/qt-webengine-yasm-nls.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-pvalloc.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-execinfo.patch'),
        apply_patch('qt-webengine/qt-webengine-sandbox-sched_getparam.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-thread-stacksize.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-off_t.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-dispatch_to_musl.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-sandbox.patch'),
        apply_patch('qt-webengine/qt-webengine-remove-glibc-check.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-elf-arm.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-crashpad.patch'),
        #apply_patch('qt-webengine/qt-webengine-el8-arm-incompatible-ints.patch')
        apply_patch('qt-webengine/qt-webengine-qtbug-88976.patch')
        os.mkdir('build')
        os.chdir('build')
        conf = '-spellchecker'
        conf += ' -webp -webengine-icu'
        #delete utils.py  def qt_build #os.mkdir('build') #os.chdir('build')
        qt_build(conf, for_webengine=True)
    else:
        os.chdir('/src/qt-webengine-build/build')
        os.remove("config.cache")
        conf = '-spellchecker'
        conf += ' -webp -webengine-icu'
        #delete utils.py  def qt_build #os.mkdir('build') #os.chdir('build')
        qt_build(conf, for_webengine=True)
