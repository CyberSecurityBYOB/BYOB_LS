#! /usr/bin/env python

import Constants
from ConfigurationFileReader import ConfigurationFileReader
from urllib2 import Request, URLError, urlopen, install_opener, build_opener, ProxyHandler
from time import sleep, strftime
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

        for i in xrange(0,wrapper.contacts) :
            # This string will be included in logfile, it's initialized with SEPARATOR
            logString = SEPARATOR[:] + '\n'
            logString += 'Botnet for ' + wrapper.url + '\n'
            logString += 'Connection #: ' + str(i) + '\n'
            logString += 'UserAgent: ' + wrapper.userAgent + '\n'
            logString += strftime("%a, %d %b %Y %H:%M:%S") + '\n'

            request = Request(wrapper.url)
            request.add_header('User-agent', wrapper.userAgent)

            # Setting proxy
            if (wrapper.proxy != Constants.UNKNOWN):
                try:
                    # Install the ProxyHandler
                    install_opener(
                        build_opener(
                            # Add ProxyHandler
                            ProxyHandler({'http': wrapper.proxy})
                        )
                    )

                    # Log proxy
                    logString += 'Proxy: '+ wrapper.proxy + '\n'

                except Exception as e:
                    # Log proxy error
                    logString += 'Proxy Error: ' + e + '\n'

            # Getting the response
            try:
                response = urlopen(request)
                # Print the headers
                # print response.headers

                # Log the response
                logString += 'Response: \n'
                for key, val in response.headers.items() :
                    logString += ''.join('{} : {}'.format(key, val)) + '\n'

            except URLError, e:
                if hasattr(e,'code') :
                    print 'Error code : ' , e.code
                    logString += 'Error code : ' , e.code + '\n'
                if hasattr(e, 'reason') :
                    print 'Error reason  : ' , e.reason
                    logString += 'Error reason : ' , e.reason + '\n'
            except ValueError, v:
                print 'This URL is invalid'
                logString += 'Error: This URL is invalid' + '\n'

            finally:
                # update log file
                logString += SEPARATOR[:] + '\n'
                with open('log.txt', 'a') as log:
                    log.write(logString)

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
