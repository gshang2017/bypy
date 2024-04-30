#!/bin/sh

#docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

#calibre version
CALIBRE_VER=7.9.0

#mkdir build dir
if [ ! -d calibre-build ]; then
    mkdir calibre-build
fi
cd calibre-build

#download bypy
if [ ! -d bypy ]; then
    if [ ! -f alpine-musl.zip ]; then
        wget  https://github.com/gshang2017/bypy/archive/refs/heads/alpine-musl.zip
    fi
    unzip alpine-musl.zip
    cp -rf bypy-alpine-musl bypy
fi

#download calibre src
if [ ! -d calibre ]; then
    if [ ! -f calibre-$CALIBRE_VER.tar.xz ]; then
        wget  https://download.calibre-ebook.com/$CALIBRE_VER/calibre-$CALIBRE_VER.tar.xz
    fi
    tar -xJf calibre-$CALIBRE_VER.tar.xz
    mv calibre-$CALIBRE_VER calibre
fi

#patch calibre src
cp -rf bypy/calibre.patch/*  calibre

#backup sources.json
cd calibre
if [ ! -f bypy/sources.json.all ]; then
    cp -rf bypy/sources.json bypy/sources.json.all
fi

#build cross armv7 host-qt

#qt 6.5.3 github
#wget https://github.com/gshang2017/bypy/releases/download/v7.9.0/qt.x86.armv7cross.tar.gz
#tar xzf qt.x86.armv7cross.tar.gz
#mv qt.x86.armv7cross/qt ../bypy
#rm rf qt.x86.armv7cross*

if [ ! -d ../bypy/qt ]; then
    mkdir -p ../bypy/qt
fi
if [ ! -d ../bypy/qt/bin ]; then
    cp -rf bypy/armv7.cross.conf  bypy/linux.conf
    cp -rf bypy/hostqt.sources.json  bypy/sources.json
    python3 setup.py build_dep linux 32
    cp -rf bypy/b/linux/32/sw/pkg/qt-*/qt/* ../bypy/qt
    if [ -d ../bypy/qt/bin ]; then
        rm bypy/b/linux/32/chroot.img
        rm -rf bypy/b/linux/32/sw/pkg
    fi
fi

if [ -d ../bypy/qt/bin ]; then
    #build cross armv7 img
    if [ ! -f bypy/b/linux/32/chrootcross.img ]; then
        cp -rf bypy/armv7.conf  bypy/linux.conf
        cp -rf bypy/crossimg.sources.json  bypy/sources.json
        python3 setup.py build_dep linux 32
        mv bypy/b/linux/32/chroot.img bypy/b/linux/32/chrootcross.img
    fi

    if [ -f bypy/b/linux/32/chrootcross.img ]; then
        #patch cross bypy
        cp -rf ../bypy/bypy.crossbuild.patch/*  ../bypy

        #crossbuild calibre armv7 dep 
        if [ ! -d bypy/b/linux/32/sw/pkg/qt-webengine ]; then
            cp -rf bypy/armv7.cross.conf bypy/linux.conf
            cp -rf bypy/cross.sources.json bypy/sources.json
            python3 setup.py build_dep linux 32
        fi

        if [ -d bypy/b/linux/32/sw/pkg/qt-webengine ]; then
           #build calibre armv7 dep all
            cp -rf bypy/sources.json.all bypy/sources.json
            if [ -f bypy/b/linux/32/chroot.img ] && [ ! -f bypy/b/linux/32/chrootx86.img ]; then
                mv bypy/b/linux/32/chroot.img bypy/b/linux/32/chrootx86.img
            fi
            if [ -f bypy/b/linux/32/chrootcross.img ]; then
                cp -rf bypy/armv7.conf bypy/linux.conf
                cp bypy/b/linux/32/chrootcross.img bypy/b/linux/32/chroot.img
                cp -rf ../bypy-alpine-musl/* ../bypy
                python3 setup.py build_dep linux 32
                ##build calibre
                if [ -d bypy/b/linux/32 ]; then
                    if [ -d bypy/b/linux/64 ] && [ ! -L bypy/b/linux/64 ]; then
                        mv bypy/b/linux/64 bypy/b/linux/64.bak
                    fi
                    if [ ! -L bypy/b/linux/64 ]; then
                        cd bypy/b/linux/
                        ln -s 32 64
                        cd ../../../
                    fi
                    python3 setup.py linux64
                fi
            fi
        fi 
    fi
fi
