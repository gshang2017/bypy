#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>


import os

from bypy.constants import islinux, PREFIX
from bypy.utils import qt_build, require_ram, replace_in_file, apply_patch


def main(args):
  require_ram(2 if islinux else 8)
  conf = '-feature-qtwebengine-build -feature-qtwebengine-widgets-build'
  conf += ' -no-feature-qtwebengine-quick-build'
  conf += ' -webengine-printing-and-pdf -webengine-webrtc'
  if islinux:
      # use system ICU otherwise there is 10MB duplication
      conf += ' -webengine-icu'
  if islinux:
      apply_patch('0001-Enable-building-on-musl.patch', level=1)
      apply_patch('0002-temp-failure-retry.patch', level=1)
      apply_patch('0003-qt-musl-mallinfo.patch', level=1)
      apply_patch('0004-qt-musl-resolve.patch', level=1)
      apply_patch('0005-qt-musl-crashpad.patch', level=1)
      apply_patch('0006-no-execinfo.patch', level=1)
      apply_patch('0007-musl-sandbox.patch', level=1)
      apply_patch('0008-musl-stat.patch', level=1)        
      apply_patch('0107-chromium-cursed-scoped_file.patch', level=1)
      #apply_patch('0009-close.patch', level=1)
      apply_patch('0010-canonicalize-file-name.patch', level=1)
      apply_patch('0011-wtf-stacksize.patch', level=1)
      apply_patch('0014-missing-includes.patch', level=1)
      apply_patch('aarch64-skia.patch', level=1)
      apply_patch('chromium-use-alpine-target.patch', level=1)
      #apply_patch('clang16-aescrypto.patch', level=1)
      #apply_patch('default-pthread-stacksize.patch', level=1)
      #apply_patch('fix-narrowing-cast.patch', level=1)
      apply_patch('gcc13.patch', level=1)
      apply_patch('lfs64.patch', level=1)
      apply_patch('no-sandbox-settls.patch', level=1)
      apply_patch('pipewire-fcntl-call.patch', level=1)
      apply_patch('systypes.patch', level=1)
      apply_patch('fstatat-32bit.patch', level=1)
      apply_patch('qtwebengine-5.15.10_p20230623-ffmpeg-binutils-2.41.patch', level=1)
      apply_patch('0015-enable-x86.patch', level=1)
    qt_build(conf, for_webengine=True)


def is_ok_to_check_universal_arches(x):
    return os.path.basename(x) not in ('gn',)
