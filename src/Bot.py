#! /usr/bin/env python

import Constants
from ConfigurationFileReader import ConfigurationFileReader
from urllib2 import Request, URLError, urlopen, install_opener, build_opener, ProxyHandler
from time import sleep, strftime, strptime, localtime
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

    # Print configuration of the botnet in log File

    for i in xrange(0,wrapper.contacts) :

        # Check if the  thread must sleep
        if isTimeToSleep(wrapper):
            print 'Sleeping...'
            sleep(timeToSleep(wrapper))
            print '...Awake'

        print 'Lets do it!'

        # This string will be included in logfile, it's initialized with SEPARATOR
        logString = SEPARATOR[:] + '\n'
        logString += 'Botnet for ' + wrapper.url + '\n'
        logString +=  str(wrapper)
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

            logString += SEPARATOR[:] + '\n'
            with open('log.txt', 'a') as log:
                log.write(logString)

            # Exit the thread, url is incorrect
            import thread
            thread.exit()

        finally:
            # update log file
            logString += SEPARATOR[:] + '\n'
            with open('log.txt', 'a') as log:
                log.write(logString)

    print 'Work Done, Bye!'

def isHourToSleep(wrapper):
    minH = wrapper.sleepModeMinHour
    maxH = wrapper.sleepModeMaxHour

    # No need to sleep
    if minH == maxH:
        return False

    now = localtime().tm_hour

    if now >= minH and now <= maxH:
        print 'Devo dormire, sono le ' + str(now) + ' e intervallo: ' + str(minH) + '-' + str(maxH)
        return True
    else:
        print 'Non Devo dormire, sono le ' + str(now) + ' e intervallo: ' + str(minH) + '-' + str(maxH)
        return False

def isTimeToSleep(wrapper):
    # Object time in python
    today = localtime()
    startSleep = strptime(wrapper.sleepModeDate, "%Y-%m-%d")

    # Numbers of day since 1 1 0000
    todayDay = today.tm_yday * today.tm_year
    startSleepDay = startSleep.tm_yday * startSleep.tm_year

    if int(wrapper.repeats)  == 0:
        return False

    if todayDay % int(wrapper.repeats) == startSleepDay % int(wrapper.repeats):
        print 'Devo dormire, oggi: ' + str(todayDay) + ' e il giorno sleep : ' +str(startSleepDay) + ' e repeat: ' + str(wrapper.repeats)
        return isHourToSleep(wrapper)
    else:
        print 'Non Devo dormire, oggi: ' + str(todayDay) + ' e il giorno sleep : ' +str(startSleepDay)+ ' e repeat: ' + str(wrapper.repeats)
        return False

def timeToSleep(wrapper):
    return 0

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
    if(operativeSystem == 'Linux' or operativeSystem == 'Mac OS X' or operativeSystem == 'OS/2'):
        try:
            # Open browser name list file
            filelist = open('browsers.list','r')
            list = filelist.readlines()
            # build grep list of browsers
            parameters = ' | grep'
            for b in list:
                parameters += ' -e ' + b.rstrip()
            filelist.close()

            import subprocess
            applist = subprocess.check_output('compgen -c' + parameters, shell=True, executable='/bin/bash')
            print 'list in environment.txt'
            return applist
        except:
            print 'error in detecting browsers'
            return 'error in detecting browsers'

    return 'Informations not available'



# Check Environment Informations
import os
import platform
print 'Detected Operative System: ' + platform.system() + ' - ' + platform.release()
envFile = open('environment.txt', 'w')
envFile.write('Operative System: ' + platform.system() + ' - ' + platform.release() + '\n')

# Check installed browsers
envFile.write('Installed Browsers Detected : ' + str( detectBrowsers(platform.system())) )
envFile.close()


# Read file
fileReader = ConfigurationFileReader()
fileReader.readConfigurationFile()

# Request builder
builder = RequestBuilder(fileReader.configDict, fileReader.defaultConfigDict)
builder.buildForABot()

# Start Thread
# urlsLen = len(fileReader.configDict[Constants.URLS])
for w in builder.workers :
    Thread(target=work, args=[w]).start()
