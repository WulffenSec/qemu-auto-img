# QEMU AUTO IMG

## What is it?
> It's a script to automate the conversion of OVA files to qcow2. For using in QEMU.

## Whats required?

- python
- qemu-img

## How it work?

#### In your terminal

```python
git clone https://www.github.com/WulffenSec/qemu-auto-img.git
cd qemu-auto-img
pip install -r requirements.txt
python qai.py -i <file to convert>
```

Providing a OVA file the script is going to automate the uncompression and rename of the files.
