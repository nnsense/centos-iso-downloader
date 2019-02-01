# CentOS-ISO-Downloader
A quick python script to list, test speed and download a CentOS ISO image. I'm using it just to avoid going on CentOS mirrorlist and lookup the URL to wget. 

The three scripts have basically the same functionality but

- get-iso-2 is in python 2
- get-iso-3 is in python 3
- get-iso.py is in python 3 and it uses threads

## Setup
Prerequisites:
`pip install requests urllib3 pyOpenSSL bs4`

Then get the main py script.

## Usage
`./get-centos.py (-v,-l)`

Arguments:
- `-v` or `--verbose`, enables script's verbose and interactive execution. It's basically showing the URLs the script fetched from mirrorlist, along with the speed, and it asks for downloading (instead of going ahead and download without confirmation) the latest ISO.
- `-l` or `--list`, show best speed download link and exit. Can be used along to `-v` to also show each mirror's speed.
- `-t` or `--tree`, show best speed OS directory tree and exit. Useful for kickstarts.
