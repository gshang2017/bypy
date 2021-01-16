#!/usr/bin/env python
# vim:fileencoding=utf-8
# License: GPLv3 Copyright: 2019, Kovid Goyal <kovid at kovidgoyal.net>

import os
import pwd
import shlex
import shutil
import subprocess
import sys
import tempfile
from functools import partial
from urllib.request import urlopen

from .conf import parse_conf_file
from .constants import base_dir
from .utils import call, print_cmd, single_instance

DEFAULT_BASE_IMAGE = (
    'http://dl-cdn.alpinelinux.org/alpine/'
    'v3.12/releases/x86_64/alpine-minirootfs-3.12.0-x86_64.tar.gz'
)

arch = '64'
img_path = sw_dir = sources_dir = img_store_path = None
conf = {}


def initialize_env():
    global img_path, img_store_path, sw_dir, sources_dir
    sources_dir = os.path.join(base_dir(), 'b', 'sources-cache')
    os.makedirs(sources_dir, exist_ok=True)
    output_dir = os.path.join(base_dir(), 'b', 'linux', arch)
    os.makedirs(output_dir, exist_ok=True)
    img_path = os.path.abspath(
        os.path.realpath(os.path.join(output_dir, 'chroot')))
    img_store_path = img_path + '.img'
    sw_dir = os.path.join(output_dir, 'sw')
    os.makedirs(sw_dir, exist_ok=True)
    conf.update(parse_conf_file(os.path.join(base_dir(), 'linux.conf')))


def mount_image():
    if not hasattr(mount_image, 'mounted'):
        call('sudo', 'mount', img_store_path, img_path)
    mount_image.mounted = True


def unmount_image():
    if hasattr(mount_image, 'mounted'):
        call('sudo', 'umount', img_path)
        del mount_image.mounted


def cached_download(url):
    bn = os.path.basename(url)
    local = os.path.join('/tmp', bn)
    if not os.path.exists(local):
        print('Downloading', url, '...')
        data = urlopen(url).read()
        with open(local, 'wb') as f:
            f.write(data)
    return local


def copy_terminfo():
    raw = subprocess.check_output(['infocmp']).decode('utf-8').splitlines()[0]
    path = raw.partition(':')[2].strip()
    if path and os.path.exists(path):
        bdir = os.path.basename(os.path.dirname(path))
        dest = os.path.join(img_path, 'usr/share/terminfo', bdir)
        call('sudo', 'mkdir', '-p', dest, echo=False)
        call('sudo', 'cp', '-a', path, dest, echo=False)


def chroot(cmd, as_root=True):
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    print_cmd(['in-chroot'] + cmd)
    user = pwd.getpwuid(os.geteuid()).pw_name
    env = {
        'PATH': '/sbin:/usr/sbin:/usr/local/bin:/bin:/usr/bin',
        'PS1': '\x1b[92mbypy\x1b[0m ({}-bit) %d {} '.format(
            arch, '#' if as_root else '$'),
        'HOME': '/root' if as_root else '/home/' + user,
        'USER': 'root' if as_root else user,
        'TERM': os.environ.get('TERM', 'xterm-256color'),
    }
    us = [] if as_root else ['--userspec={}:{}'.format(
        os.geteuid(), os.getegid())]
    as_arch = ['linux{}'.format(arch), '--']
    cmd = ['sudo', 'chroot'] + us + [img_path] + as_arch + list(cmd)
    copy_terminfo()
    call('sudo', 'cp', '/etc/resolv.conf',
         os.path.join(img_path, 'etc'), echo=False)
    ret = subprocess.Popen(cmd, env=env).wait()
    if ret != 0:
        raise SystemExit(ret)


def write_in_chroot(path, data):
    path = path.lstrip('/')
    p = subprocess.Popen([
        'sudo', 'tee', os.path.join(img_path, path)],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
    if not isinstance(data, bytes):
        data = data.encode('utf-8')
    p.communicate(data)
    if p.wait() != 0:
        raise SystemExit(p.returncode)


def _build_container(url=DEFAULT_BASE_IMAGE):
    user = pwd.getpwuid(os.geteuid()).pw_name
    archive = cached_download(url.format('amd64' if arch == '64' else 'i386'))
    if os.path.exists(img_path):
        call('sudo', 'rm', '-rf', img_path, echo=False)
    if os.path.exists(img_store_path):
        os.remove(img_store_path)
    os.makedirs(img_path)
    call('truncate', '-s', '2G', img_store_path)
    call('mkfs.ext4', img_store_path)
    mount_image()
    call('sudo tar -C "{}" -xpf "{}"'.format(img_path, archive), echo=False)
#aarch64
    if "aarch64"  in archive:
        qemuurl='https://github.com/multiarch/qemu-user-static/releases/download/v5.2.0-2/qemu-aarch64-static'
        call('sudo wget "{}" -P "{}"/usr/bin'.format(qemuurl,img_path), echo=False)
        call('sudo chmod +x  "{}"/usr/bin/qemu-aarch64-static'.format(img_path), echo=False)
#
#armv7l
    if "armv7l"  in archive:
        qemuurl='https://github.com/multiarch/qemu-user-static/releases/download/v5.2.0-2/qemu-arm-static'
        call('sudo wget "{}" -P "{}"/usr/bin'.format(qemuurl,img_path), echo=False)
        call('sudo chmod +x  "{}"/usr/bin/qemu-arm-static'.format(img_path), echo=False)
#
    ##if os.getegid() != 100:
    ##    chroot('groupadd -f -g {} {}'.format(os.getegid(), 'crusers'))
    ##chroot(
    ##    'useradd --home-dir=/home/{user} --create-home'
    ##    ' --uid={uid} --gid={gid} {user}'.format(
    ##        user=user, uid=os.geteuid(), gid=os.getegid())
    ##)
    # Prevent services from starting
    ##write_in_chroot('/usr/sbin/policy-rc.d', '#!/bin/sh\nexit 101')
    ##chroot('chmod +x /usr/sbin/policy-rc.d')
    # prevent upstart scripts from running during install/update
    ##chroot('dpkg-divert --local --rename --add /sbin/initctl')
    ##chroot('cp -a /usr/sbin/policy-rc.d /sbin/initctl')
    ##chroot('''sed -i 's/^exit.*/exit 0/' /sbin/initctl''')
    # remove apt-cache translations for fast "apt-get update"
    ##write_in_chroot(
    ##    '/etc/apt/apt.conf.d/chroot-no-languages',
    ##    'Acquire::Languages "none";'
    ##)
    deps = conf['deps']
    if isinstance(deps, (list, tuple)):
        deps = ' '.join(deps)
    ##deps_cmd = 'apt-get install -y ' + deps
    deps_cmd = 'apk add ' + deps
    for cmd in [
        # Basic build environment
        'apk update',
        'apk add shadow',
        'apk add build-base zsh perl cmake autoconf autoconf-archive automake git curl xz python3 linux-headers nasm libidn-dev libxml2-dev libtool freetype-dev fontconfig-dev meson  gettext-dev dbus-glib-dev ttf-dejavu',
        'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py',
        'python3.8 get-pip.py',
        'python3.8 -m pip install ninja',
        ##'apt-get update',
        ##'apt-get install -y build-essential cmake software-properties-common'
        ##' nasm chrpath zsh git uuid-dev libmount-dev'
        ##' dh-autoreconf',
        ##'add-apt-repository ppa:deadsnakes/ppa -y',
        ##'apt-get update',
        ##'apt-get install -y python3.7',
        ##'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py',
        ##'python3.7 get-pip.py',
        ##'python3.7 -m pip install ninja',
        ##'python3.7 -m pip install meson',
        deps_cmd,
        # Cleanup
        ##'apt-get clean',
        ##'chsh -s /bin/zsh ' + user,
    ]:
        chroot(cmd)


def build_container():
    url = conf['image']
    try:
        _build_container(url=url)
    except Exception:
        failed_img_path = img_store_path + '.failed'
        if os.path.exists(failed_img_path):
            os.remove(failed_img_path)
        os.rename(img_store_path, failed_img_path)
        raise


def check_for_image(tag):
    return os.path.exists(img_store_path)


def get_mounts():
    ans = {}
    lines = open('/proc/self/mountinfo', 'rb').read().decode(
            'utf-8').splitlines()
    for line in lines:
        parts = line.split()
        src, dest = parts[3:5]
        ans[os.path.abspath(os.path.realpath(dest))] = src
    return ans


def mount_all(tdir):
    scall = partial(call, echo=False)
    current_mounts = get_mounts()
    base = os.path.dirname(os.path.abspath(__file__))

    def mount(src, dest, readonly=False):
        dest = os.path.join(img_path, dest.lstrip('/'))
        if dest not in current_mounts:
            scall('sudo', 'mkdir', '-p', dest)
            scall('sudo', 'mount', '--bind', src, dest)
            if readonly:
                scall('sudo', 'mount', '-o', 'remount,ro,bind', dest)

    mount(tdir, '/tmp')
    mount(sw_dir, '/sw')
    mount(os.getcwd(), '/src', readonly=True)
    mount(sources_dir, '/sources')
    mount(os.path.dirname(base), '/bypy', readonly=True)
    mount('/dev', '/dev')
    scall('sudo', 'mount', '-t', 'proc', 'proc',
          os.path.join(img_path, 'proc'))
    scall('sudo', 'mount', '-t', 'sysfs', 'sys', os.path.join(img_path, 'sys'))
    scall('sudo', 'chmod', 'a+w', os.path.join(img_path, 'dev/shm'))
    scall('sudo', 'mount', '--bind', '/dev/shm',
          os.path.join(img_path, 'dev/shm'))


def umount_all():
    found = True
    while found:
        found = False
        for mp in sorted(get_mounts(), key=len, reverse=True):
            if mp.startswith(img_path) and '/chroot/src/' not in mp:
                call('sudo', 'umount', '-l', mp, echo=False)
                found = True
                break
    del mount_image.mounted


def run(args):
    # dont use /tmp since it could be RAM mounted and therefore
    # too small
    with tempfile.TemporaryDirectory(prefix='tmp-', dir='bypy/b') as tdir:
        zshrc = os.path.realpath(os.path.expanduser('~/.zshrc'))
        if os.path.exists(zshrc):
            shutil.copy2(zshrc, os.path.join(tdir, '.zshrc'))
        else:
            open(os.path.join(tdir, '.zshrc'), 'wb').close()
        try:
            mount_all(tdir)
            ##cmd = ['python3.7', '/bypy', 'main'] + args
            cmd = ['python3.8', '/bypy', 'main'] + args
            os.environ.pop('LANG', None)
            for k in tuple(os.environ):
                if k.startswith('LC') or k.startswith('XAUTH'):
                    del os.environ[k]
            chroot(cmd, as_root=False)
        finally:
            umount_all()


def singleinstance():
    name = f'bypy-{arch}-singleinstance-{os.getcwd()}'
    return single_instance(name)


def main(args=tuple(sys.argv)):
    global arch
    args = list(args)
    if len(args) > 1 and args[1] in ('64', '32'):
        arch = args[1]
        del args[1]
    if not singleinstance():
        raise SystemExit('Another instance of the linux container is running')
    initialize_env()
    try:
        if len(args) > 1:
            if args[1] == 'shutdown':
                raise SystemExit(0)
            if args[1] == 'container':
                build_container()
                return
        if not check_for_image(arch):
            build_container()
        else:
            mount_image()
        run(args)
    finally:
        unmount_image()


if __name__ == '__main__':
    main()
