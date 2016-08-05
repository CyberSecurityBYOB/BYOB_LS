#! /usr/bin/env python

FILE_PATH = 'byob_config.txt'
DEFAULT_CONFIG = 'default_config.txt'


class ConfigurationFileReader:

    def __init__(self):
        self.configDict = {}
        self.defaultConfigDict = {}
        self.filePath = FILE_PATH
        self.defaultFilePath = DEFAULT_CONFIG

        # load default settings
        self.readDefaultConfigurationFile()

    def readConfigurationFile(self):
        with open(FILE_PATH, 'r') as f:
            for line in f:
                splitLine = line.split()
                self.configDict[splitLine[0]] = splitLine[1:]

    def readDefaultConfigurationFile(self):
        with open(DEFAULT_CONFIG, 'r') as f:
            for line in f:
                splitLine = line.split()
                self.defaultConfigDict[splitLine[0]] = splitLine[1:]

if __name__ == "__main__":
    fileReader = ConfigurationFileReader()
    fileReader.readConfigurationFile()
    for (key,value) in fileReader.configDict.iteritems() :
        print key,value
