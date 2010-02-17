#!/usr/bin/env python

import os, stat, errno, shutil, sys
import fuse
from fuse import Fuse
from Dirmaker import Dirmaker
from MyImageMagickCommandMaker import MyImageMagickCommandMaker
from ArgumentHandler import ArgumentHandler

fuse.fuse_python_api = (0, 2)

class ImageFS(Fuse):
    
    
    def __init__(self, argumentHandler, *args,**kwargs):
        fuse.Fuse.__init__(self,*args,**kwargs)
        self.argumentHandler = argumentHandler
    
        self.source = self.argumentHandler.getSource()
        self.configFile = self.argumentHandler.getConfigFile()
    
        self.dirmaker = Dirmaker(self.configFile)        
        #making the temporary dirs
        self.dirmaker.removePreviousTree(self.source)
        self.dirmaker.makeDirs(self.source)
        self.pathTempDir = self.dirmaker.getPathTempDir()
        
    def getattr(self, path):
        self.dirmaker.makeDirs(self.source)
        
        if path.split("/")[len(path.split("/"))-1] not in self.dirmaker.getDirNames():
            if os.path.isdir(self.pathTempDir+self.source+ path) and not os.path.isdir(self.source+path):
                shutil.rmtree(self.pathTempDir+self.source+path)
                    
        
        for dirName in self.dirmaker.getDirNames():
            if len(path.split("/"+dirName)) > 1:
                if os.path.isfile(self.pathTempDir+self.source+ path):
                    return os.lstat(self.pathTempDir+self.source+path)
                else:
                    pathSplit = path.split("/"+dirName)
                    return self.returnLstat(pathSplit)
        return os.lstat(self.pathTempDir+self.source+path)

    def readdir(self, path, offset):
        self.bool = 0
        dirents = ['.', '..']        
        for dirName in self.dirmaker.getDirNames(): 
            if len(path.split("/"+dirName)) > 1:
                pathSplit = path.split("/"+dirName)
                tempFiles = os.listdir(self.source + pathSplit[0])
                files = []
                for f in tempFiles:
                    if os.path.isfile(self.source + pathSplit[0]+"/"+f):
                        files.append(f)
                self.bool = 1
                break

        if not self.bool:
            files = os.listdir(self.pathTempDir+self.source+ path)
        self.bool = 0    
        
        for f in files:
                dirents.append(f)

        for r in  dirents:
            yield fuse.Direntry(str(r))
    
    def open(self, path, flags): ###controle of file al bestaat, zoniet: aanmaken!
        if not os.path.isfile(self.pathTempDir+self.source+ path):
            for dirName in self.dirmaker.getDirNames():
                if len(path.split("/"+dirName)) > 1:
                    paramDict = self.dirmaker.getParams(dirName)
                    pathSplit = path.split("/"+dirName)
                    srcPath = self.source + pathSplit[0] + pathSplit[len(pathSplit)-1]
                    destPath = self.pathTempDir+self.source+path
                    
                    commmaker = MyImageMagickCommandMaker(srcPath, destPath, paramDict)
                    commmaker.makeCommand()
                    break
            
            accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
            if (flags & accmode) != os.O_RDONLY:
                return -errno.EACCES
            commmaker.executeCommand()
            
        else:
            pass
        
    def read(self, path, size, offset):
        imgFile = open(self.pathTempDir+self.source+ path, "rb")
        imgFile.seek(offset)
        imgBytes = imgFile.read(size)
        imgFile.close() 
        return imgBytes
        
    ## returning lstat info
    def returnLstat(self, pathSplit):
        if pathSplit[len(pathSplit)-1].strip() == '': 
                return os.lstat(self.source + pathSplit[0])
        else:
            p = self.source + pathSplit[0] + pathSplit[len(pathSplit)-1]
            if os.path.isfile(p):
                return os.lstat(p)
            else:
                pass
    
    def searchConfigFile(self, argv):
        for arg in argv:
            if len(arg.split("config=")) > 1:
                return os.path.abspath(arg.split("config=")[1])
                break
       
     
def main():
    
    argumentHandler = ArgumentHandler()
    sys.argv = ["imagefs.py"]
    
    #make sure the destination folder is at argv[1] since fuse.py will use this as the mountpoint
    #it's actually not that important what's at sys.argv[0]
    sys.argv.append(argumentHandler.getDestination())
    
    server = ImageFS(argumentHandler, version="%prog " + fuse.__version__, dash_s_do='setsingle')
    server.parser.add_option(mountopt="config", metavar="PATH", default='/',
                             help="configuration file from under PATH [default: %default]")
    server.parse(values=server, errex=1)
    server.main()

if __name__ == '__main__':
    main()


#TODO vanhieruit een nieuwe klasse maken zodat ik die enkel het mountpunt moet meegeven