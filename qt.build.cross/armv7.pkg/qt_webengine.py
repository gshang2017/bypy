#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>

import glob
import os

from bypy.constants import PREFIX, MAKEOPTS, islinux, iswindows
from bypy.utils import ModifiedEnv, qt_build, replace_in_file, apply_patch, run


def main(args):
  env = {}
  env['PATH'] = '/opt/armv7l-linux-musleabihf-cross/bin:' + os.environ['PATH']
  with ModifiedEnv(**env):
    os.chdir('/src')
    qtwebenginebuilddir='/src/qt-webengine-build'
    if not os.path.exists(qtwebenginebuilddir):
        os.makedirs(qtwebenginebuilddir)
        qtwebengine_files = list(glob.glob('/sources/qtwebengine-everywhere-src-*.tar.xz'))
        run(f'tar -xf "{qtwebengine_files[0]}" --strip-components=1  -C /src/qt-webengine-build')
        run('mv  /opt/cross/usr/lib/pkgconfig/libxml-2.0.pc /opt/cross/usr/lib/libxml-2.0.pc.bak')
        run('mv  /opt/cross/usr/lib/pkgconfig/libxslt.pc /opt/cross/usr/lib/libxslt.pc.bak')
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
        os.mkdir('/src/qt-webengine-build/src/3rdparty/chromium/sys')
        os.symlink( '/opt/cross/usr/include/sys/queue.h', os.path.join('src/3rdparty/chromium/sys','queue.h')),
        os.symlink( '/opt/cross/usr/include/sys/cdefs.h', os.path.join('src/3rdparty/chromium/sys','cdefs.h')),
        os.symlink( '/opt/cross/usr/include/fontconfig', os.path.join('src/3rdparty/chromium','fontconfig')),
        os.symlink( '/opt/cross/usr/include/X11', os.path.join('src/3rdparty/chromium','X11')),
        os.symlink( '/opt/cross/usr/include/xcb', os.path.join('src/3rdparty/chromium','xcb')),
        #
        # https://chromium-review.googlesource.com/c/v8/v8/+/2136489
        ##apply_patch('qt-webengine-icu67.patch'),
        apply_patch('qt-webengine/qt-webengine-icu67.patch'),
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
        #apply_patch('qt-webengine/qt-webengine-remove-glibc-check.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-elf-arm.patch'),
        apply_patch('qt-webengine/qt-webengine-musl-crashpad.patch'),
        apply_patch('qt-webengine/qt-webengine-el8-arm-incompatible-ints.patch')
        os.mkdir('build')
        os.chdir('build')
        conf = ' -pepper-plugins -printing-and-pdf  -webrtc  -spellchecker '
        conf += ' -webp -webengine-icu  '
        #delete utils.py  def qt_build #os.mkdir('build') #os.chdir('build')
        qt_build(conf, for_webengine=True)
    else:
        run('mv  /opt/cross/usr/lib/pkgconfig/libxml-2.0.pc /opt/cross/usr/lib/libxml-2.0.pc.bak')
        run('mv  /opt/cross/usr/lib/pkgconfig/libxslt.pc /opt/cross/usr/lib/libxslt.pc.bak')
        os.chdir('/src/qt-webengine-build/build')
        os.remove("config.cache")
        conf = '  -pepper-plugins -printing-and-pdf    -webrtc  -spellchecker'
        conf += ' -webp -webengine-icu  '
        #delete utils.py  def qt_build #os.mkdir('build') #os.chdir('build')
        qt_build(conf, for_webengine=True)
