# pip install requests urllib3 pyOpenSSL bs4 --force --upgrade
import sys
import re
import urllib
import requests
import argparse
from threading import Thread
from asyncio import Queue
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser( description="Search and optionally download the latest CentOS7 ISO selecting the best speed mirror.", epilog="By nnsense - 2018")
parser.add_argument("-v","--version", help="Specify CentOS version: 6, 7 or 8. Default: 7", required=False, default=7)
parser.add_argument("-d","--download", help="Download the ISO", required=False, action="store_true")
parser.add_argument("-t","--tree", help="Show best speed directory tree (for kickstart) and exit", required=False, action="store_true")
args = parser.parse_args()


def main():

    centos_version = str(args.version)

    url = "http://isoredirect.centos.org/centos/" + centos_version + "/isos/x86_64"

    f = urllib.request.urlopen(url)
    html = f.read()
    source = BeautifulSoup(html, 'html.parser')
    
    
    
    threads = []
    queue = Queue()
    
    # Testing each url for speed
    for link in source.find_all('a'):
        href = str(link.string)
        
        if href.startswith('http') and 'x86_64' in href:
            thread = Thread( target=TestSpeed, args=( href,queue ) )
            thread.start()
            threads.append(thread)
        
    for th in threads:
        th.join()

    bestspeed = 0.5
    
    while not queue.empty():
        speedtst = queue.get_nowait()

        besturl = speedtst['url']
        speed = speedtst['speed']
                
        print(str(speed) + " - Mirror: " + url)
            
        if speed < bestspeed:
            bestspeed = speed
            besturl = url


    print( "-- Best speed: " + besturl + " (speed: " + str(bestspeed) + ")" )

    if args.tree:
        dirtree = besturl.replace("isos","os")
        print("Use directory tree: " + dirtree)

    if args.download:
        # Fetch the new page from the best speed link
        f = urllib.request.urlopen(besturl)
        
        html_linksPage = f.read()
        linksPage = BeautifulSoup(html_linksPage, 'html.parser');

        # For each link
        for link in linksPage.find_all('a'):
            href = str(link.string)

            if(re.search('minimal.*iso$', href.lower(), re.IGNORECASE) or re.search('boot.*iso$', href.lower(), re.IGNORECASE)):
                    file_name = href.rstrip()

        with open(file_name, "wb") as f:

            print("Downloading %s" % file_name)
            
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


def TestSpeed(href, queue):
    try:
        speed = requests.get(href.rstrip(), timeout=1).elapsed.total_seconds()
        url = href.rstrip()
        speedtest = {"url": url, "speed": speed}
        queue.put_nowait(speedtest)
    except:
        pass
        
if __name__ == '__main__': main()
