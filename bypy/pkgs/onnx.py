#!/usr/bin/env python
# License: GPLv3 Copyright: 2024, Kovid Goyal <kovid at kovidgoyal.net>

import os

from bypy.constants import CMAKE, PREFIX, PYTHON, UNIVERSAL_ARCHES, ismacos, iswindows, islinux
from bypy.utils import copy_headers, install_binaries, replace_in_file, run, run_shell, apply_patch

run_shell


def main(args):
#
    if islinux:
        apply_patch('no-execinfo.patch', level=1)
        apply_patch('0001-Remove-MATH_NO_EXCEPT-macro.patch', level=1)
    build_sh = 'build.bat' if iswindows else './build.sh'
    if islinux:
        cmdline = f'sh {build_sh} --config Release --build_shared_lib --parallel --compile_no_warning_as_error --skip_submodule_sync --skip_tests'
    else:
        cmdline = f'{build_sh} --config Release --build_shared_lib --parallel --compile_no_warning_as_error --skip_submodule_sync --skip_tests'
    kw = {}
    if ismacos:
        arches = ';'.join(UNIVERSAL_ARCHES)
        cmdline += f' --cmake_extra_defines CMAKE_OSX_ARCHITECTURES={arches} CMAKE_VERBOSE_MAKEFILE=ON'
        kw['append_to_path'] = os.path.dirname(CMAKE)
    elif iswindows:
        replace_in_file('tools/ci_build/build.py', 'target_arch = platform.machine()', 'target_arch = platform.machine().upper()')
        kw['append_to_path'] = os.path.dirname(PYTHON)
    else:
        cmdline += f' --allow_running_as_root --cmake_extra_defines CMAKE_SYSTEM_PREFIX_PATH={PREFIX}'
    if islinux:
        #alpine need flatbuffers-locale.patch
        cmdline_1 = cmdline + ' || exit 0'
        run('sh','-c',cmdline_1,**kw)
        apply_patch('flatbuffers-locale.patch.noauto', level=1)
        run('sh','-c',cmdline,**kw)
    else:
        run(cmdline,**kw)
    # run_shell()
    copy_headers('include/onnxruntime/core/session/*.h', 'onnx/include')
    copy_headers('include/onnxruntime/core/providers/cpu/*.h', 'onnx/include')
    copy_headers('include/onnxruntime/core/framework/provider_options.h', 'onnx/include')
    if ismacos:
        install_binaries('build/*/Release/libonnxruntime*.dylib', 'onnx')
    elif iswindows:
        install_binaries('build/Windows/Release/Release/onnxruntime*.dll', 'onnx')
        install_binaries('build/Windows/Release/Release/onnxruntime*.lib', 'onnx')
    else:
        install_binaries('build/*/Release/libonnxruntime.so*', 'onnx')
