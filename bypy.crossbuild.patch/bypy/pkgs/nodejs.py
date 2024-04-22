#!/usr/bin/env python
# License: GPLv3 Copyright: 2021, Kovid Goyal <kovid at kovidgoyal.net>

from ..constants import iswindows, islinux, LIBDIR
from ..utils import simple_build, run, require_ram, ModifiedEnv, replace_in_file,apply_patch
#
import os

allow_non_universal = True


def main(args):
#
    if islinux:
           replace_in_file(
            'common.gypi',
            '-m64',
            '')
           replace_in_file(
            'tools/v8_gypfiles/toolchain.gypi',
            '-m64',
            '')
           replace_in_file(
            'tools/gyp/pylib/gyp/generator/ninja.py',
            '-m64',
            '')
           replace_in_file(
            'deps/cares/config.guess',
            '-m64',
            '')  
           replace_in_file(
            'deps/npm/node_modules/node-gyp/addon.gypi',
            '-m64',
            '')  
           replace_in_file(
            'deps/npm/node_modules/node-gyp/gyp/pylib/gyp/generator/ninja.py',
            '-m64',
            '')                                      
           replace_in_file(
            'deps/openssl/openssl/Configurations/10-main.conf',
            '-m64',
            '')
           replace_in_file(
            'configure.py',
            'o[\'cflags\']+=[\'-msign-return-address=all\']',
            '')             

#
    if os.path.exists('/opt/armv7l-linux-musleabihf-cross'):
        with ModifiedEnv(
            AR_host='ar',
            CC_host='gcc',
            CXX_host='g++',
            LINK_host='g++',
            GYP_DEFINES='armv7=1',
            CCFLAGS='-march=armv7-a+fp',
            CXXFLAGS='-march=armv7-a+fp',
        ):
            if not iswindows:
                if islinux:
                    require_ram(1)       
                    conf = '--cross-compiling --dest-cpu=arm --dest-os=linux --with-arm-fpu=vfpv3'  
                return simple_build(conf, use_cross_host=False)
            run('.\\vcbuild.bat')

    else:                                                 
        with ModifiedEnv(
            AR_host='ar',
            CC_host='gcc',
            CXX_host='g++',
            LINK_host='g++',
        ):
        	if not iswindows:
            	if islinux:
        	    	require_ram(1)       
        	    	conf = '--cross-compiling --dest-os=linux --dest-cpu=arm64'
            	return simple_build(conf, use_cross_host=False)
        	run('.\\vcbuild.bat')
