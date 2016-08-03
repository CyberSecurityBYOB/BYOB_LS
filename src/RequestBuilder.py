import Constants
from random import randint


class RequestBuilder:

    def __init__(self, dictionary):
        self.configurationFileDictionary = dictionary
        self.workers = []

        # Check compatibility
        if (not self.configurationFileIsSupported()):
            print 'Configuration file not supported: expected ' + str(Constants.SUPPORTEDVERSION) + ', found ' + self.configurationFileDictionary[Constants.VERSION][0]
            import thread
            thread.exit()

    def configurationFileIsSupported(self):
        return self.configurationFileDictionary[Constants.VERSION][0] == Constants.SUPPORTEDVERSION

    def buildForABot(self):
        frequency = self.computeFrequency(int(self.configurationFileDictionary[Constants.MINFREQUENCY][0]),
                                          int(self.configurationFileDictionary[Constants.MAXFREQUENCY][0]))

        for url in self.configurationFileDictionary[Constants.URLS]:
            self.buildForAWorker(url, frequency)

    def buildForAWorker(self, url, frequency):
        worker = WorkerWrapper()
        worker.url = url
        worker.frequency = frequency
        worker.contacts = int(self.configurationFileDictionary[Constants.CONTACTS][0])
        worker.proxy = self.configurationFileDictionary[Constants.PROXY][0]
        worker.userAgent = self.configurationFileDictionary[Constants.USERAGENT][0]
        worker.sleepModeDate = self.configurationFileDictionary[Constants.SLEEPMODEDATE][0]

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
