# CentOS-ISO-Downloader
A quick python script to list, test speed and download a CentOS ISO image. I'm using it just to avoid going on CentOS mirrorlist and lookup the URL to wget. It works with CentOS 6, 7 or 8.

The scripts have basically the same functionality but

- get-iso.py is in python 3 and it uses threads
- get-iso-2 is in python 2, here for historical reasons and doesn't use threads. I'm also not updating it..

This is pretty much a learning experiment, but get-iso.py is actually working quite well, I'm using it to download ISOs for KVM.

## Setup
Prerequisites:
`pip3 install requests urllib3 pyOpenSSL bs4`

Then get the py script and make it executable.

## Usage
`./get-iso.py (-v,-t,-d,-s)`

Arguments:
- `-v` or `--version`, select the CentOS version. Valid options are 6, 7 or 8. Default is 7 (CentOS7).
- `-d` or `--download`, show the URL with the best download speed and then download the **MINIMAL** ISO, which for CentOS8 is the boot ISO since the full DVD is over 6 GB.
- `-t` or `--tree`, show best speed OS directory tree and exit. Useful for Anaconda kickstart.
- `-s` or `--speed`, show the speed of each URL tested.

## Example

Check the best speed and then download the latest CentOS8 ISO.
```
./get-iso.py -v 8 -d
```
