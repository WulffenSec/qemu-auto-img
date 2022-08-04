#!/bin/env python3
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
        for p in process:
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
    
    print('Job done!')
qai(args)
