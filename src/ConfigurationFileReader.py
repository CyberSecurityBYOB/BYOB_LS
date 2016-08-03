#! /usr/bin/env python

FILE_PATH = 'byob_config.txt'


class ConfigurationFileReader:

    def __init__(self):
        self.configDict = {}
        self.filePath = FILE_PATH

    def readConfigurationFile(self):
        with open(FILE_PATH, 'r') as f:
            for line in f:
                splitLine = line.split()
                self.configDict[splitLine[0]] = splitLine[1:]

if __name__ == "__main__":
    fileReader = ConfigurationFileReader()
    fileReader.readConfigurationFile()
    for (key,value) in fileReader.configDict.iteritems() :
        print key,value
