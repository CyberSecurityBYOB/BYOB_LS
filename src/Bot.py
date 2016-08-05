#! /usr/bin/env python
import Constants
from ConfigurationFileReader import ConfigurationFileReader
from urllib2 import Request, URLError, urlopen, install_opener, build_opener, ProxyHandler
from time import sleep, strftime, localtime, strptime, ctime
from threading import Thread
from RequestBuilder import RequestBuilder
import ntplib

SEPARATOR = '#############################################################'


def work(wrapper):

    # Prepare request
    # Valid URL url = 'http://www.google.com'
    # Unreachable URL url = 'http://www.asjdsajdsakjdsaksadjkasd.com'
    # Invalid URL url = 'dsakjshdakjadshksdahjksad'
    # headers = {'User-Agent' : 'Mozilla 5.10'}
    # request = urllib2.Request(url, None, headers)

    # Print configuration of the botnet in log File

    endLife = wrapper.contacts if wrapper.contacts!=0 else float('inf')
    i = 0

    while (i < endLife) :

        # Check if the  thread must sleep
        while isTimeToSleep(wrapper):
            print wrapper.url + ': Sleeping...'
            sleep(timeToSleep(wrapper))
            print wrapper.url + '...Awake'

        print wrapper.url + ' Lets do it!'

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
                print wrapper.url + ' Error code : ' , e.code
                logString += 'Error code : ' + str(e.code) + '\n'
            if hasattr(e, 'reason') :
                print wrapper.url + ' Error reason : ' , e.reason
                logString += 'Error reason : ' + str(e.reason) + '\n'
        except ValueError, v:
            print wrapper.url + ' This URL is invalid'
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


            sleep(wrapper.frequency)

            i += 1

    print 'Work Done, Bye!'

def timeNTP(server):
    try:
        c = ntplib.NTPClient()
        response = c.request(server, version=3)

        print ' Time from network : ' + str(strftime("%a, %d %b %Y %H:%M:%S",localtime(response.tx_time)))
        time = localtime(response.tx_time)
    except:
        print ' Network Time not available, using system time'
        time = localtime()
    finally:
        return time

def isHourToSleep(wrapper):
    minH = wrapper.sleepModeMinHour
    maxH = wrapper.sleepModeMaxHour

    # No need to sleep
    if minH == maxH:
        return False

    if wrapper.networkTimeServer != Constants.UNKNOWN:
        now = timeNTP(wrapper.networkTimeServer).tm_hour
    else:
        now = localtime().tm_hour

    if now >= minH and now < maxH:
        print wrapper.url + ' Devo dormire, sono le ' + str(now) + ' e intervallo: ' + str(minH) + '-' + str(maxH)
        return True
    else:
        print wrapper.url + ' Non Devo dormire, sono le ' + str(now) + ' e intervallo: ' + str(minH) + '-' + str(maxH)
        return False

def isTimeToSleep(wrapper):
    # Get system time or network time
    today = timeNTP(wrapper.networkTimeServer) if wrapper.networkTimeServer != Constants.UNKNOWN else localtime()

    # Get start sleep mode date, if unknown choose day of thread start
    startSleep = wrapper.sleepModeDate

    # Numbers of day since 1 1 0000
    todayDay =  today.tm_year * 360 + today.tm_yday
    startSleepDay =  360 *  startSleep.tm_year + startSleep.tm_yday

    if todayDay < startSleepDay:
        return False

    if int(wrapper.repeats)  == 0:
        return False

    if todayDay % int(wrapper.repeats) == startSleepDay % int(wrapper.repeats):
        print wrapper.url + ' Devo dormire, oggi: ' + str(todayDay) + ' e il giorno sleep : ' +str(startSleepDay) + ' e repeat: ' + str(wrapper.repeats)
        return isHourToSleep(wrapper)
    else:
        print wrapper.url + ' Non Devo dormire, oggi: ' + str(todayDay) + ' e il giorno sleep : ' +str(startSleepDay)+ ' e repeat: ' + str(wrapper.repeats)
        return False


def timeToSleep(wrapper):
    if wrapper.networkTimeServer != Constants.UNKNOWN:
        now = timeNTP(wrapper.networkTimeServer).tm_hour
        return int(wrapper.sleepModeMaxHour - now) * 60 * 60
    else:
        return int(wrapper.sleepModeMaxHour - localtime().tm_hour) * 60 * 60


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
