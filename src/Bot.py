#! /usr/bin/env python

from ConfigurationFileReader import ConfigurationFileReader
from urllib2 import Request, URLError, urlopen
from time import sleep
from threading import Thread

SEPARATOR = '##############################'


def work():

    # Prepare request
    # Valid URL url = 'http://www.google.com'
    # Unreachable URL url = 'http://www.asjdsajdsakjdsaksadjkasd.com'
    # Invalid URL url = 'dsakjshdakjadshksdahjksad'
    url = 'https://www.google.com'
    # headers = {'User-Agent' : 'Mozilla 5.10'}
    # request = urllib2.Request(url, None, headers)

    while True:

        print 'Sleeping...'
        sleep(1)
        print 'Awake!'
        for i in xrange(3) :
            request = Request(url)
            request.add_header('User-agent', 'Mozilla 5.10')

            # Getting the response
            try:
                response = urlopen(request)
                # Print the headers
                print response.headers

                with open('log.txt', 'a') as log:
                    log.write(SEPARATOR + '\n')
                    for key, val in response.headers.items() :
                        log.write(''.join('{} : {}'.format(key, val)) + '\n')
                    log.write(SEPARATOR + '\n')

            except URLError, e:
                if hasattr(e,'code') :
                    print 'Error code : ' , e.code
                if hasattr(e, 'reason') :
                    print 'Error reason  : ' , e.reason
            except ValueError, v:
                print 'This URL is invalid'

        print 'Work Done! Sleeping...'
        sleep(3)
        print "Let's work!"

# Read file
fileReader = ConfigurationFileReader()
fileReader.readConfigurationFile()

# Start Thread
urlsLen = len(fileReader.configDict['Urls'])
for n in xrange(urlsLen) :
    Thread(target=work, args=()).start()



