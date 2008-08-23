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
        self.borderColor = dict['borderColor']
        self.borderWidth = dict['borderWidth']
        self.borderHeight = dict['borderHeight']
        self.cropWidth = dict['cropWidth']
        self.cropHeight = dict['cropHeight']
        self.cropX = dict['cropX']
        self.cropY = dict['cropY']
        self.imageMagickCommand = dict['imageMagickCommand']
        
        if self.imageMagickCommand != '':
            toSplit = self.imageMagickCommand
            self.command = toSplit.split("%src")[0]+self.srcPath+toSplit.split("%src")[1].split("%dest")[0]+self.destPath
        else:
            self.command = "convert \"" +self.srcPath+ "\""
            self.resize = self.getResizeString()
            self.rotate = self.getRotationString()
            self.crop = self.getCropString()
            self.border = self.getBorderString()
            self.command += self.crop + self.resize + self.rotate + self.border + " \""+self.destPath+ "\""
        
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
    
    def getBorderString(self):
        string = ' '
        if self.borderColor != '':
            string += ' -bordercolor ' +self.borderColor
    
        if self.borderWidth != '' or self.borderHeight != '':
            string += ' -border '
            if self.borderWidth == "":
                string += "x" + self.borderHeight
            elif self.borderHeight == "":
                string += self.borderWidth + "x"
            else:
                string += self.borderWidth + "x" + self.borderHeight + " "
        return string
    
    def getCropString(self):
        string = ' '
        bool = 0
        if self.cropWidth != '' or self.cropHeight != '':
            string += ' -crop '
            bool = 1
            if self.cropWidth == "":
                string += "x" + self.cropHeight
            elif self.cropHeight == "":
                string += self.cropWidth + "x"
            else:
                string += self.cropWidth + "x" + self.cropHeight
        
        if self.cropX != '' or self.cropY != '':
            if not bool:
                string += ' -crop '
            if self.cropX == "":
                string += self.cropY
            elif self.cropY == "":
                string += self.cropX
            else:
                string += self.cropX + self.cropY + " "
        
        return string
