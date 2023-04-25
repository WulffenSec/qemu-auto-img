#!/bin/env python3
import argparse
import sys
import subprocess


def banner() -> None:
    """
    Prints the banner
    """
    green = '\033[32m'
    reset = '\033[37m'
    banner = f'''
    {green} ██████  ███████ ███    ███ ██    ██{reset}        █████  ██    ██ ████████  ██████       {green} ██ ███    ███  ██████{reset}
    {green}██    ██ ██      ████  ████ ██    ██{reset}       ██   ██ ██    ██    ██    ██    ██      {green} ██ ████  ████ ██{reset}
    {green}██    ██ █████   ██ ████ ██ ██    ██{reset} █████ ███████ ██    ██    ██    ██    ██ █████{green} ██ ██ ████ ██ ██   ███{reset}
    {green}██ ▄▄ ██ ██      ██  ██  ██ ██    ██{reset}       ██   ██ ██    ██    ██    ██    ██      {green} ██ ██  ██  ██ ██    ██{reset}
    {green} ██████  ███████ ██      ██  ██████ {reset}       ██   ██  ██████     ██     ██████       {green} ██ ██      ██  ██████{reset}
    {green}    ▀▀{reset} Github: WulffenSec | Version: 0.2
    ''' # noqa
    print(banner)


def checkFile(file) -> bool:
    """
    Checks if the OVA file actually is a OVA file
    """
    cmd = subprocess.check_output(['file', file]).decode().split('\n')[0]
    ova = file + ': POSIX tar archive'
    vmdk = file + ': VMware4 disk image'
    if cmd == ova or cmd == vmdk:
        return True
    else:
        print('No valid file. Type of file readed:', cmd.split(': ')[1])
        return False


def checkSoftware() -> bool:
    """
    Checks if qemu-img is installed.
    """
    cmd = subprocess.call(['which', 'qemu-img'],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
    if cmd == 0:
        return True
    else:
        return False


def unGzip(file) -> bool:
    """
    Unzip GZ files.
    """
    cmd = subprocess.call(['gzip', '-d', file],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
    if cmd == 0:
        return True
    else:
        return False


def unTar(file) -> list:
    """
    Untar OVA files.
    """
    cmd = subprocess.check_output(['tar', 'xvf', file]).decode()
    return cmd.split('\n')


def qemuImg(files) -> bool:
    """
    Converts the file into qcow2.
    """
    for file in files:
        if file.split('.')[-1] == 'vmdk':
            output = file.split('.vmdk')[0] + '.qcow2'
        elif file.split('.')[-1] == 'vdi':
            output = file.split('.vdi')[0] + '.qcow2'
        cmd = subprocess.call(['qemu-img', 'convert', '-O', 'qcow2',
                               file, output], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    if cmd == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='qai.py', usage='qai.py -i ova-file.ova',
            description='\t\tExtract and rename and convert OVA/VMDK/VDI files to qcow2 for qemu.') # noqa

    parser.add_argument('-i', '--input',
                        help='\t\tOVA/VMDK/VDI file to be work on.',
                        action='store', required=True, metavar='string')

    args = parser.parse_args()
    file = args.input

    banner()

    gz = (file.split('.')[-1] == 'gz')
    if gz is True:
        print('Gzip compress file detected, uncompressing...')
        unZip = unGzip(file)
        if unZip is False:
            print('Error uncompressing gz file.')
            sys.exit(1)
        ova = (file.split('.')[-2] == 'ova')
        vmdk = (file.split('.')[-2] == 'vmdk')
        vdi = (file.split('.')[-2] == 'vdi')
        file = file.split('.gz')[0]
    else:
        ova = (file.split('.')[-1] == 'ova')
        vmdk = (file.split('.')[-1] == 'vmdk')
        vdi = (file.split('.')[-1] == 'vdi')

    if ova is True or vmdk is True or vdi is True:
        pass
    else:
        print('You must use a OVA/VMDK/VDI file as input file.')
        sys.exit(1)

    checked = checkFile(file)
    if checked is False:
        sys.exit(1)

    ready = checkSoftware()
    if ready is False:
        print('Error finding "qemu-img", check your system if needs to be installed.') # noqa
        sys.exit(1)
    files: list = []
    if ova is True:
        print('Uncompressing OVA file...')
        unTared = unTar(file)
        for tar in unTared:
            if tar != '':
                if tar.split('.')[-1] == 'gz':
                    print('Gzip compress file detected, uncompressing...')
                    unZip = unGzip(tar)
                    if unZip is False:
                        print('Error uncompressing gz file.')
                        sys.exit(1)
                    vmdk = (tar.split('.')[-2] == 'vmdk')
                    vdi = (tar.split('.')[-2] == 'vdi')
                    files.append(tar.split('.gz')[0])
                else:
                    vmdk = (tar.split('.')[-1] == 'vmdk')
                    vdi = (tar.split('.')[-1] == 'vdi')
                    if tar.split('.')[-1] == 'vmdk' or\
                            tar.split('.')[-1] == 'vdi':
                        files.append(tar)
    else:
        files.append(file)

    print('Converting file/files into qcow2')
    converted = qemuImg(files)
    if converted is True:
        print('Convertion done.')
        sys.exit(0)
    else:
        print('Fail to convert file/files.')
        sys.exit(1)
