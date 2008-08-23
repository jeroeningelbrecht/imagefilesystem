#!/usr/bin/env python

import os, stat, errno, shutil, sys
import fuse
from fuse import Fuse
import Dirmaker
from Dirmaker import Dirmaker
import logger
from logger import Logger
import MyImageMagickCommandMaker
from MyImageMagickCommandMaker import MyImageMagickCommandMaker

fuse.fuse_python_api = (0, 2)

class ImageFS(Fuse):
    
    def __init__(self, *args,**kwargs):
        fuse.Fuse.__init__(self,*args,**kwargs)
        self.src = os.path.abspath(sys.argv[1]) #de bronmap
        self.dest = os.path.abspath(sys.argv[2]) #dest map
        
        #there should be another way to get the value of the config option, but I haven't found it
        self.configFile = self.searchConfigFile(sys.argv)
        self.dirmaker = Dirmaker(self.configFile)        
        #making the temporary dirs
        self.dirmaker.removePreviousTree(self.src)
        self.dirmaker.makeDirs(self.src)
        self.pathTempDir = self.dirmaker.getPathTempDir()
        
    def getattr(self, path):
        self.dirmaker.makeDirs(self.src)
        if os.path.isdir(self.pathTempDir+self.src+ path) and not os.path.isdir(self.src+path):
            shutil.rmtree(self.pathTempDir+self.src+ path)
            
        for dirName in self.dirmaker.getDirNames():
            if len(path.split("/"+dirName)) > 1:
                if os.path.isfile(self.pathTempDir+self.src+ path):
                    return os.lstat(self.pathTempDir+self.src+path)
                else:
                    pathSplit = path.split("/"+dirName)
                    return self.returnLstat(pathSplit)
        return os.lstat(self.pathTempDir+self.src+path)

    def readdir(self, path, offset):
        self.bool = 0
        dirents = ['.', '..']        
        for dirName in self.dirmaker.getDirNames():
            if len(path.split("/"+dirName)) > 1:
                pathSplit = path.split("/"+dirName)
                files = os.listdir(self.src + pathSplit[0])
                self.bool = 1
                break

        if not self.bool:
            files = os.listdir(self.pathTempDir+self.src+ path)
        self.bool = 0    
        
        for f in files:
            dirents.append(f)

        for r in  dirents:
            yield fuse.Direntry(str(r))
    
    def open(self, path, flags): ###controle of file al bestaat, zoniet: aanmaken!
        if not os.path.isfile(self.pathTempDir+self.src+ path):
            for dirName in self.dirmaker.getDirNames():
                if len(path.split("/"+dirName)) > 1:
                    paramDict = self.dirmaker.getParams(dirName)
                    pathSplit = path.split("/"+dirName)
                    srcPath = self.src + pathSplit[0] + pathSplit[len(pathSplit)-1]
                    destPath = self.pathTempDir+self.src+path
                    
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
        imgFile = open(self.pathTempDir+self.src+ path, "rb")
        imgFile.seek(offset)
        imgBytes = imgFile.read(size)
        imgFile.close() 
        return imgBytes
        
    ## returning lstat info
    def returnLstat(self, pathSplit):
        if pathSplit[len(pathSplit)-1].strip() == '': 
                return os.lstat(self.src + pathSplit[0])
        else:
            p = self.src + pathSplit[0] + pathSplit[len(pathSplit)-1]
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
    usage="""
Userspace hello example

""" + Fuse.fusage
    
    server = ImageFS(version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')
    server.parser.add_option(mountopt="config", metavar="PATH", default='/',
                             help="configuration file from under PATH [default: %default]")
    server.parse(values=server, errex=1)
    server.main()

if __name__ == '__main__':
    main()
