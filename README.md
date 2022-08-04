# QEMU AUTO IMG 

## What is it?
> It's a script to automate the conversion of ova/vdi/vmdk files to qcow2. For using in kvm/qemu.

## Whats required?

- python
- tar
- qemu-img

## How it work?

#### In your terminal
```
git clone https://www.github.com/WulffenSec/qemu-auto-img.git
cd qemu-auto-img
python qai.py <file to convert>
```

Giving the ova/vdi/vmdk file as an argument the script will convert it to qcow2.