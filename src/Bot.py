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
                            ProxyHandler({'http': wrapper.proxy , 'https' : wrapper.proxy})
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
                logString += 'Response: ' + str(response.getcode()) + '\n' + str(response.info()) + '\n'

            except URLError, e:
                if hasattr(e,'code') :
                    print 'Error code : ' , e.code
                    logString += 'Error code : ' + str(e.code) + '\n'
                if hasattr(e, 'reason') :
                    print 'Error reason : ' , e.reason
                    logString += 'Error reason : ' + str(e.reason) + '\n'
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

def detectBrowsers(operativeSystem):
    if(operativeSystem == 'Windows'):
        import _winreg as wreg
        key = wreg.OpenKey(wreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Clients\\StartMenuInternet",0, wreg.KEY_READ)
        browsers = []
        try:
            i = 0
            while True:
                browsers.append(wreg.EnumKey(key, i))
                i += 1
        except WindowsError as e:
            print browsers
            return browsers
    if(operativeSystem == 'Linux'):
        filelist = open('browsers.list','r')
        list = filelist.readlines()
        parameters = ' | grep '
        for b in list:
            parameters += '-e ' + b + '\n'
        import subprocess
        applist = subprocess.check_output('compgen -c' + parameters, shell=True, executable='/bin/bash')
        print applist
        return applist


    return 'Informations not available'



# Check Environment Informations
import os
import platform
print 'Detected Operative System: ' + platform.system() + ' - ' + platform.release()
envFile = open('environment.txt', 'w')
envFile.write('Operative System: ' + platform.system() + ' - ' + platform.release() + '\n')

# Check installed browsers (Windows) from registry
envFile.write('Installed Browsers Detected : ' + str( detectBrowsers(platform.system())) )
envFile.close()



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
