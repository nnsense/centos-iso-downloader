#!/usr/bin/python2

# pip install requests urllib3 pyOpenSSL bs4 --force --upgrade
import sys
import urllib
import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser( description="Search and download the latest CentOS7 ISO selecting the best speed mirror.", epilog="By nnsense - 2018")
parser.add_argument("-v","--verbose", help="Show each mirror's speed and ask if download latest image (by default, it just select and downloads the ISO)", required=False, action="store_true")
parser.add_argument("-l","--list", help="Show best speed download link and exit", required=False, action="store_true")
parser.add_argument("-t","--tree", help="Show best speed directory tree (for kickstart) and exit", required=False, action="store_true")
args = parser.parse_args()

url = "http://isoredirect.centos.org/centos/7/isos/x86_64"
f = urllib.urlopen(url)
html = f.read()
source = BeautifulSoup(html, 'html.parser');

bestspeed = 10

for link in source.find_all('a'):
    href = unicode(link.string)
    if( href.startswith('http') and 'x86_64' in href):
        url = href.rstrip()
        speedtest = requests.get(href.rstrip()).elapsed.total_seconds()
        
        if args.verbose:
            print str(speedtest) + " - Mirror: " + url
            
        if speedtest < bestspeed:
            bestspeed = speedtest
            besturl = url

print "Best speed: " + besturl + " (speed: " + str(bestspeed) + ")"

isoAsk = "n"

if args.verbose and not args.list:
    isoAsk = raw_input('Download latest CentOS7? (Y/n): ')

    while isoAsk != "Y" and isoAsk != "n":
        isoAsk = raw_input('Download latest CentOS7? (Y/n): ')

f = urllib.urlopen(besturl)
html_linksPage = f.read()
linksPage = BeautifulSoup(html_linksPage, 'html.parser');

for link in linksPage.find_all('a'):
    href = unicode(link.string)
    if ( 'torrent' not in href and 'Minimal' in href ):
        file_name = href.rstrip()
        
if args.list and not args.tree:
    print "Best download option: " + besturl + "/" + file_name
    exit()

if args.tree:
    dirtree = besturl.replace("isos","os")
    print "Use directory tree: " + dirtree
    exit()
    
if isoAsk == "Y" or args.verbose == False:
    with open(file_name, "wb") as f:
            print "Downloading %s" % file_name
            
            response = requests.get(besturl + "/" + file_name, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()
                    print
else:
    print "Quitting"

