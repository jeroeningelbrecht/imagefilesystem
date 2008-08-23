import logger
from logger import Logger

import CommandMaker
from CommandMaker import CommandMaker

import os

class MyImageMagickCommandMaker(CommandMaker):
    def __init__(self, srcPath, destPath, paramDictionary):
        CommandMaker.__init__(self, srcPath, destPath, paramDictionary)
        self.srcPath = srcPath
        self.destPath = destPath
        
    def makeCommand(self):
        dict = CommandMaker.getParamDict(self)
        self.width = dict['width']
        self.height = dict['height']
        self.angle = dict['angle']
        
        self.command = "convert \"" +self.srcPath+ "\""
        self.resize = self.getResizeString()
        
        self.rotate = self.getRotationString()
        self.command += self.resize + self.rotate+ " \""+self.destPath+ "\""
        
    def executeCommand(self):
        os.popen(self.command)

    def getResizeString(self):
        if self.width != "" or self.height != "":
            self.resize = " -resize "
            if self.width == "":
                self.resize += "x" + self.height
            elif self.height == "":
                self.resize += self.width + "x"
            else:
                self.resize += self.width + "x" + self.height + " "
        else:
            self.resize = " "
        return self.resize
    
    def getRotationString(self):
        if self.angle != "":
            self.rotate = " -rotate " + self.angle + " "
        else:
            self.rotate = " "
        return self.rotate
