import xml, os, shutil
from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import ContentHandler

import string

import logger
from logger import Logger

class Dirmaker(object):
    def __init__(self, pathConfigurationFile):
        self.path = pathConfigurationFile
        
        # Create a parser
        self.parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        self.parser.setFeature(feature_namespaces, 0)
        # Create the handler
        self.dh = self.FindDir()
        # Tell the parser to use our handler
        self.parser.setContentHandler(self.dh)
        # Parse the input
        self.parser.parse(self.path)
        
        self.pathTempDir = os.path.expanduser(self.dh.pathTempDir)
        self.dirList = self.dh.dirs
        
    def makeDirs(self, pathSourceDir):
        if os.path.isdir(self.pathTempDir+pathSourceDir):
            shutil.rmtree(self.pathTempDir+pathSourceDir)
        os.makedirs(self.pathTempDir+pathSourceDir)
        
        self.dirNames = []
        for dir in self.dirList:
            self.dirNames.append(dir[0])
        
        for root, dirs, files in os.walk(pathSourceDir, topdown=True):
            str = root.split(pathSourceDir)[1]
            for dir in self.dirNames:
                os.makedirs(self.pathTempDir+pathSourceDir + str +"/"+ dir)
    
    def getPathTempDir(self):
        return self.pathTempDir
    
    def getDirNames(self):
        return self.dirNames
    
    def getParams(self, nameDir):
        for dir in self.dirList:
            if dir[0] == nameDir:
                params = {'width':dir[1], 'height':dir[2], 'angle':dir[3]}
                break
        return params
        
    class FindDir(ContentHandler):
        def __init__(self):
            self.inWidthContent = 0
            self.inHeightContent = 0
            self.inRotationContent = 0
            
            self.dirs = []
            self.dir = []
            
            #initializing the vars in case the user left them out of the XML
            self.width = ''
            self.height = ''
            self.rotation = ''
    
        def normalize_whitespace(self,text):
            "Remove redundant whitespace from a string"
            return ' '.join(text.split())
    
        def startElement(self, name, attrs):
            if name == 'tempdir':
                self.pathTempDir = attrs.get('path', '')
                
            if name == 'dir': 
                self.dirName = attrs.get('name', '')
                
            elif name == 'width':
                self.inWidthContent = 1
                self.width = ''
            
            elif name == 'height':
                self.inHeightContent = 1
                self.height = ''
            
            elif name == 'rotationAngle':
                self.inRotationContent = 1
                self.rotation = ''                
                
        def characters(self, ch):
            if self.inWidthContent:
                self.width = self.width + ch
            elif self.inHeightContent:
                self.height = self.height + ch
            elif self.inRotationContent:
                self.rotation = self.rotation + ch
        
        def endElement(self, name):
            if name == 'dir':
                self.dir.extend([self.dirName, self.width, self.height, self.rotation])
                self.dirs.append(self.dir)
                self.dir=[]
                self.width = ''
                self.height = ''
                self.rotation = ''
            elif name == 'width':
                self.inWidthContent = 0 
                self.width = self.normalize_whitespace(self.width)
            elif name == 'height':
                self.inHeightContent = 0 
                self.height = self.normalize_whitespace(self.height)
            elif name == 'rotationAngle':
                self.inRotationContent = 0 
                self.rotation = self.normalize_whitespace(self.rotation)
                
