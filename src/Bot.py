#! /usr/bin/env python

from ConfigurationFileReader import ConfigurationFileReader
from urllib2 import Request, URLError, urlopen
from time import sleep
from threading import Thread
from RequestBuilder import RequestBuilder

SEPARATOR = '##############################'


def work(wrapper):

    # Prepare request
    # Valid URL url = 'http://www.google.com'
    # Unreachable URL url = 'http://www.asjdsajdsakjdsaksadjkasd.com'
    # Invalid URL url = 'dsakjshdakjadshksdahjksad'
    # headers = {'User-Agent' : 'Mozilla 5.10'}
    # request = urllib2.Request(url, None, headers)

    while True:

        print 'Sleeping...'
        sleep(1)
        print 'Awake!'
        for i in xrange(wrapper.contacts) :
            request = Request(wrapper.url)
            request.add_header('User-agent', wrapper.userAgent)

            # Getting the response
            try:
                response = urlopen(request)
                # Print the headers
                # print response.headers

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
        sleep(wrapper.frequency)
        print "Let's work!"

# Read file
fileReader = ConfigurationFileReader()
fileReader.readConfigurationFile()

# Request builder
builder = RequestBuilder(fileReader.configDict)
builder.buildForABot()

# Start Thread
# urlsLen = len(fileReader.configDict[Constants.URLS])
for w in builder.workers :
    Thread(target=work, args=[w]).start()



