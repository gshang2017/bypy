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

#build cross aarch64 host-qt

#qt 6.5.3 github
#wget https://github.com/gshang2017/bypy/releases/download/v7.9.0/qt.x86_64.aarch64cross.tar.gz
#tar xzf qt.x86_64.aarch64cross.tar.gz
#mv qt.x86_64.aarch64cross/qt ../bypy
#rm rf qt.x86_64.aarch64cross*

if [ ! -d ../bypy/qt ]; then
    mkdir -p ../bypy/qt
fi
if [ ! -d ../bypy/qt/bin ]; then
    cp -rf bypy/aarch64.cross.conf  bypy/linux.conf
    cp -rf bypy/hostqt.sources.json  bypy/sources.json
    python3 setup.py build_dep linux
    cp -rf bypy/b/linux/64/sw/pkg/qt-*/qt/* ../bypy/qt
    if [ -d ../bypy/qt/bin ]; then
        rm bypy/b/linux/64/chroot.img
        rm -rf bypy/b/linux/64/sw/pkg
    fi

fi

if [ -d ../bypy/qt/bin ]; then
    #build cross aarch64 img
    if [ ! -f bypy/b/linux/64/chrootcross.img ]; then
        cp -rf bypy/aarch64.conf  bypy/linux.conf
        cp -rf bypy/crossimg.sources.json  bypy/sources.json
        python3 setup.py build_dep linux
        mv bypy/b/linux/64/chroot.img bypy/b/linux/64/chrootcross.img
    fi

    if [ -f bypy/b/linux/64/chrootcross.img ]; then
        #patch cross bypy          
        cp -rf ../bypy/bypy.crossbuild.patch/*  ../bypy

        #crossbuild calibre aarch64 dep 
        if [ ! -d bypy/b/linux/64/sw/pkg/qt-webengine ]; then
            cp -rf bypy/aarch64.cross.conf bypy/linux.conf
            cp -rf bypy/cross.sources.json bypy/sources.json
            python3 setup.py build_dep linux
        fi

        if [ -d bypy/b/linux/64/sw/pkg/qt-webengine ]; then
            #build calibre aarch64 dep all
            cp -rf bypy/sources.json.all bypy/sources.json
            if [ -f bypy/b/linux/64/chroot.img ] && [ ! -f bypy/b/linux/64/chrootx86_64.img ] ; then
                mv bypy/b/linux/64/chroot.img bypy/b/linux/64/chrootx86_64.img
            fi
            if [ -f bypy/b/linux/64/chrootcross.img ]; then
                cp -rf bypy/aarch64.conf bypy/linux.conf
                cp bypy/b/linux/64/chrootcross.img bypy/b/linux/64/chroot.img
                cp -rf ../bypy-alpine-musl/* ../bypy
                python3 setup.py build_dep linux
                ##build calibre
                python3 setup.py linux64
            fi
        fi
    fi
fi
