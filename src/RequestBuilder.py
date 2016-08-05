import Constants
from random import randint
from time import strptime


class RequestBuilder:

    def __init__(self, dictionary, default_config):
        self.configurationFileDictionary = dictionary
        self.configurationFileDictionaryDefault = default_config
        self.workers = []

        # Check compatibility
        if (not self.configurationFileIsSupported()):
            print 'Configuration file not supported: expected ' + str(Constants.SUPPORTEDVERSION) + ', found ' + self.configurationFileDictionary[Constants.VERSION][0]
            import thread
            thread.exit()

    def configurationFileIsSupported(self):
        return self.configurationFileDictionary[Constants.VERSION][0] == Constants.SUPPORTEDVERSION

    def buildForABot(self):
        for index in xrange(0,len(self.configurationFileDictionary[Constants.URLS])):
            frequency = self.computeFrequency(int(self._setSettingOrDefault(self.configurationFileDictionary[Constants.MINFREQUENCY][index],self.configurationFileDictionaryDefault[Constants.MINFREQUENCY][0])),
                                  int(self._setSettingOrDefault(self.configurationFileDictionary[Constants.MAXFREQUENCY][index],self.configurationFileDictionaryDefault[Constants.MAXFREQUENCY][0])))

            self.buildForAWorker(index, frequency)

    def _setSettingOrDefault(self, setting, default):
        return setting if setting!=Constants.UNKNOWN else default


    def buildForAWorker(self, index, frequency):
        worker = WorkerWrapper()
        worker.url = self._setSettingOrDefault(self.configurationFileDictionary[Constants.URLS][index], self.configurationFileDictionaryDefault[Constants.URLS][0])
        worker.frequency = frequency
        worker.contacts = int(self._setSettingOrDefault(self.configurationFileDictionary[Constants.CONTACTS][index], self.configurationFileDictionaryDefault[Constants.CONTACTS][0]))
        worker.proxy = self._setSettingOrDefault(self.configurationFileDictionary[Constants.PROXY][index], self.configurationFileDictionaryDefault[Constants.PROXY][0])
        worker.userAgent = self._setSettingOrDefault(self.configurationFileDictionary[Constants.USERAGENT][index], self.configurationFileDictionaryDefault[Constants.USERAGENT][0])
        worker.sleepModeDate = strptime(self._setSettingOrDefault(self.configurationFileDictionary[Constants.SLEEPMODEDATE][index], self.configurationFileDictionaryDefault[Constants.SLEEPMODEDATE][0]), "%Y-%m-%d")
        worker.sleepModeMaxHour = int(self._setSettingOrDefault(self.configurationFileDictionary[Constants.SLEEPMODEMAXHOUR][index], self.configurationFileDictionaryDefault[Constants.SLEEPMODEMAXHOUR][0]))
        worker.sleepModeMinHour = int(self._setSettingOrDefault(self.configurationFileDictionary[Constants.SLEEPMODEMINHOUR][index], self.configurationFileDictionaryDefault[Constants.SLEEPMODEMINHOUR][0]))
        worker.networkTimeServer = self._setSettingOrDefault(self.configurationFileDictionary[Constants.NETWORKTIMESERVER][index],self.configurationFileDictionaryDefault[Constants.NETWORKTIMESERVER][0])

        worker.repeats = self._setSettingOrDefault(self.configurationFileDictionary[Constants.REPEATS][index], self.configurationFileDictionaryDefault[Constants.REPEATS][0])

        self.workers.append(worker)

    def computeFrequency(self,minFrequency,maxFrequency):
        if minFrequency == maxFrequency :
            return minFrequency
        else :
            return randint(minFrequency,maxFrequency)


class WorkerWrapper :

    def __init__(self):
        self.url = ''
        self.contacts = 0
        self.proxy = ''
        self.userAgent = ''
        self.frequency = 0
        self.sleepModeDate = ''
        self.sleepModeMaxHour = 0
        self.sleepModeMinHour = 0
        self.repeats = 0
        self.networkTimeServer = ''

    def __str__(self):
        return 'Settings:\nUrl : ' + self.url + '\nMax Contacts : ' + str(self.contacts) +'\nProxy : ' + self.proxy +'\nUserAgent : ' + self.userAgent +'\nFrequency : ' + str(self.frequency) +'\nSleep Mode : ' + str(self.sleepModeDate.tm_yday) + ' from//to : ' + str(self.sleepModeMinHour) + '//' + str(self.sleepModeMaxHour) + ' repeats : ' + str(self.repeats) + '\nNTP Server : '+ self.networkTimeServer +'\nEnd Of Settings.\n'
