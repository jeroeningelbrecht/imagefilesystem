import logger
from logger import Logger

class CommandMaker(object):
    def __init__(self,srcPath, destPath,paramDictionary):
        self.setParams(paramDictionary)
        self.setSrcPath(srcPath)
        self.setDestPath(destPath)
        
    def setParams(self, paramDictionary):
        self.paramDictionary = paramDictionary
    
    def setSrcPath(self, srcPath):
        self.srcPath = srcPath
    
    def setDestPath(self, destPath):
        self.destPath = destPath
    
    def getSrcPath(self):
        return self.srcPath
    
    def getDestPath(self):
        return self.destPath
    
    def getParamDict(self):
        return self.paramDictionary
    
    def makeCommand(self):
        return 0
    
    def executeCommand(self):
        return 0