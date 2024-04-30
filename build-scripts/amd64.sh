#!/bin/sh

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
    mv bypy-alpine-musl bypy
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

#build calibre dep
cd calibre
python3 setup.py build_dep linux

#build calibre
python3 setup.py linux64

