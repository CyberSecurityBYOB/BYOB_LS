import Constants
from random import randint


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
        #we can move the random frequency directly on threads
        frequency = self.computeFrequency(int(self.configurationFileDictionary[Constants.MINFREQUENCY][0]),
                                          int(self.configurationFileDictionary[Constants.MAXFREQUENCY][0]))

        for index in xrange(0,len(self.configurationFileDictionary[Constants.URLS])):
            self.buildForAWorker(index, frequency)

    def _setSettingOrDefault(self, setting, default):
        return setting if setting!=Constants.UNKNOWN else default


    def buildForAWorker(self, index, frequency):
        worker = WorkerWrapper()
        worker.url = self._setSettingOrDefault(self.configurationFileDictionary[Constants.URLS][index], self.configurationFileDictionaryDefault[Constants.URLS][0])
        worker.frequency = frequency
        worker.contacts = int(self._setSettingOrDefault(self.configurationFileDictionary[Constants.CONTACTS][index], self.configurationFileDictionaryDefault[Constants.CONTACTS][0]))
        worker.proxy = self.configurationFileDictionary[Constants.PROXY][0]
        worker.userAgent = self._setSettingOrDefault(self.configurationFileDictionary[Constants.USERAGENT][index], self.configurationFileDictionaryDefault[Constants.USERAGENT][0])
        worker.sleepModeDate = self._setSettingOrDefault(self.configurationFileDictionary[Constants.SLEEPMODEDATE][index], self.configurationFileDictionaryDefault[Constants.SLEEPMODEDATE][0])

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
