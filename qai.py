#!/bin/env python3
import colorama
import argparse
import sys
import subprocess


def banner() -> None:
    """
    Prints the banner
    """
    green = colorama.Fore.GREEN
    reset = colorama.Fore.RESET
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
    if cmd != file + ': POSIX tar archive':
        print('No valid OVA File. Type of file readed:', cmd.split(': ')[1])
        return False
    else:
        return True


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='qai.py', usage='qai.py -i ova-file.ova',
            description='\t\tExtract and rename OVA files to qcow2 for qemu.')

    parser.add_argument('-i', '--input',
                        help='\t\tOVA file to be work on.',
                        action='store', required=True, metavar='string')

    args = parser.parse_args()

    if (args.input.split('.')[-1] == 'ova') is False:
        print('You must use a OVA file as input file.')
        sys.exit(1)

    banner()
    checked = checkFile(args.input)
    if checked is False:
        sys.exit(1)
    ready = checkSoftware()
    if ready is False:
        print('Error finding "qemu-img", check your system if needs to be installed.') # noqa
        sys.exit(1)

"""
# Imports.
import subprocess
import sys
import re


args = sys.argv

def qai(args):

    # Help menu
    help_menu = '''
    ------------------------------------------------------
    -                   qemu-auto-img                    -
    ------------------------------------------------------
    -  Made by: Marcos Dos Santos | Github: WulffenSec   -
    ------------------------------------------------------
    Version 0.1
    Usage examples:
        qai appliance.ova
    Options:
        -h          --help          |   Display help menu
    '''

    # Checking args.
    disk_format = None
    for a in args:
        if re.findall('qai',a):
            continue
        elif a == '-h' or a == '--help':
            print(help_menu)
            quit()
        elif re.findall('ova',a):
            file = a
            disk_format = 'ova'
        elif re.findall('vmdk',a):
            file = a
            disk_format = 'vmdk'
        elif re.findall('vdi',a):
            file = a
            disk_format = 'vdi'
        elif re.findall('ovf',a):
            print('The file you need to input has to be a OVA or VMDK or VDI file')
            quit()
        else:
            print(help_menu)
            quit()
    
    # Checks for a file.
    if disk_format == None:
        print(help_menu)
        quit()

    # Checks if qemu-img is install.
    print('Checking for qemu-img:')
    process = subprocess.run(['which','qemu-img'])
    if process.returncode == 1:
        print('qemu-img not found. Install it and come back.')
    else:
        print('Found!')
    
    # OVA work, extract find the disk file and set variable.
    if disk_format == 'ova':
        try:
            print('\nExtracting the files from the OVA file')
            process = subprocess.check_output(['tar','xvf',file])
        except Exception:
            print('File not found!')
            quit()
        process = str(process)
        process = process.split('\\n')
        extra_disk = list()
        for p in process:
            if re.findall('disk00[2-9]+',p):
                extra_disk.append(p)
                continue
            if re.findall('vmdk',p):
                disk_format = ('vmdk')
                file = p
                if p.startswith("b'"):
                    p.split("'")
                    p = p[1]
                    file = p
            elif re.findall('vdi',p):
                disk_format = ('vdi')
                file = p
                if p.startswith("b'"):
                    p.split("'")
                    p = p[1]
                    file = p

        print('Done!\n')

    # Doing the qemu work.
    print('Converting the disk img to qcow2')
    if disk_format == 'vmdk':
        output = file.split('vmdk')
    elif disk_format == 'vdi':
        output = file.split('vdi')
    else:
        print('Something went wrong')
        quit()
    
    output = output[0]
    output = output + 'qcow2'

    subprocess.run(['qemu-img','convert','-O','qcow2',file,output])
    print('Done!')
    
    # Multi disk inside OVA converting
    if len(extra_disk) >= 1:
        print('\nMore than one disk detected, converting...\n')
        for x in extra_disk:
            print('Converting the disk img to qcow2')
            if disk_format == 'vmdk':
                output = x.split('vmdk')
            elif disk_format == 'vdi':
                output = x.split('vdi')
            else:
                print('Something went wrong')
                quit()
            
            output = output[0]
            output = output + 'qcow2'

            subprocess.run(['qemu-img','convert','-O','qcow2',x,output])
            print('Done!\n')

    print('Job done!')
qai(args)
"""
