#!/usr/bin/env python

import os, stat, errno, shutil, sys, tempfile
import fuse
from fuse import Fuse
import threading

fuse.fuse_python_api = (0, 2)

class MyStat(fuse.Stat):
    def __init__(self):
        
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

class HelloFS(Fuse):
    
    def __init__(self,*args,**kwargs):
        fuse.Fuse.__init__(self,*args,**kwargs)
        self.src = sys.argv[1] #de bronmap
        self.dest = sys.argv[2] #dest map
        
        #other variables
        pathConfFile = os.path.abspath(sys.argv[0])
        confFile = os.path.dirname(pathConfFile)+"/configuration.txt"
        f = open(confFile, 'r')
        l = f.readlines()
        
        self.pathTmpDir = l[l.index("tmpdir\n")+1].strip()
        self.THUMB_width = l[l.index("THUMB_width\n")+1].strip()
        self.THUMB_height = l[l.index("THUMB_height\n")+1].strip()
        self.SMALL_width = l[l.index("SMALL_width\n")+1].strip()
        self.SMALL_height = l[l.index("SMALL_height\n")+1].strip()
        self.ROTATED_angle = l[l.index("ROTATED_angle\n")+1].strip()
        
        #making the temporary dirs
        if os.path.isdir(self.pathTmpDir):
            shutil.rmtree(self.pathTmpDir)
        os.mkdir(self.pathTmpDir)
        
        for root, dirs, files in os.walk(self.src, topdown=True):
            str = root.split(self.src)[1]
            for dir in ["/THUMB", "/SMALL", "/ROTATED"]:
                os.makedirs(self.pathTmpDir + str + dir)
        
    def getattr(self, path):
        
        if len(path.split("/THUMB")) > 1:
            pathSplit = path.split("/THUMB") 
            return self.returnLstat(pathSplit)
        
        elif len(path.split("/SMALL")) > 1:
            pathSplit = path.split("/SMALL")
            return self.returnLstat(pathSplit)

        elif len(path.split("/ROTATED")) > 1:
            pathSplit = path.split("/ROTATED") 
            return self.returnLstat(pathSplit)
            
        else:
            return os.lstat(self.pathTmpDir + path)

    def readdir(self, path, offset):
        dirents = ['.', '..']        
        
        if len(path.split("/THUMB")) > 1:
            pathSplit = path.split("/THUMB")
            files = os.listdir(self.src + pathSplit[0])
        elif len(path.split("/SMALL")) > 1:
            pathSplit = path.split("/SMALL")
            files = os.listdir(self.src + pathSplit[0])
        elif len(path.split("/ROTATED")) > 1:
            pathSplit = path.split("/ROTATED")
            files = os.listdir(self.src + pathSplit[0])
            
        else:
            files = os.listdir(self.pathTmpDir + path)
            
        for f in files:
            dirents.append(f)
        for r in  dirents:
            yield fuse.Direntry(r)
            
    def open(self, path, flags): ###controle of file al bestaat, zoniet: aanmaken!
        if not os.path.isfile(self.pathTmpDir + path):
            
            if len(path.split("/THUMB")) > 1:
                command = self.getResizeCommand(path.split("/THUMB"), path)
            
            elif len(path.split("/SMALL")) > 1 :
                command = self.getResizeCommand(path.split("/SMALL"), path)
                
            elif len(path.split("/ROTATED")) > 1 :
                pathSplit = path.split("/ROTATED")
                pth = self.src + pathSplit[0] + pathSplit[len(pathSplit)-1]
                command = "convert " +pth+ " -rotate " +self.ROTATED_angle + " " +self.pathTmpDir +path
            else:
                pass
            
            accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
            if (flags & accmode) != os.O_RDONLY:
                return -errno.EACCES
            os.popen(command, "r")
            
        else:
            pass
        
    def read(self, path, size, offset):
        imgFile = open(self.pathTmpDir + path, "rb")
        imgFile.seek(offset)
        imgBytes = imgFile.read(size)
        imgFile.close() 
        return imgBytes

    ###Logging###
    def wrt(self, str):
        f = open("/tmp/log.txt", 'a')
        f.write(str+"\n")
        f.close()
        
    def wrtList(self, list):
        f = open("/tmp/log.txt", 'a')
        for str in list:
            f.write(str+"\n")
        f.close()
        
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
    
    def getResizeCommand(self, pathSplit, path):
        pth = self.src + pathSplit[0] + pathSplit[len(pathSplit)-1]
        command = "convert " +pth+ " -resize " +self.THUMB_width+ "x" +self.THUMB_height+ " " +self.pathTmpDir +path
        return command
    
def main():
    usage="""
Userspace hello example

""" + Fuse.fusage
    server = HelloFS(version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')

    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
