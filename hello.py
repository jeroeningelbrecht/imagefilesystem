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
        self.width = l[l.index("width\n")+1].strip()
        self.height = l[l.index("height\n")+1].strip()
        
        #making the temporary dirs
        if os.path.isdir(self.pathTmpDir):
            shutil.rmtree(self.pathTmpDir)
        os.mkdir(self.pathTmpDir)
        
        for root, dirs, files in os.walk(self.src, topdown=True):
            str = root.split(self.src)[1]
            os.makedirs(self.pathTmpDir + str + "/THUMB")
        
        
    def wrt(self, str):
        f = open("/tmp/log.txt", 'a')
        f.write(str+"\n")
        f.close()
        
    def getattr(self, path):
        #st = MyStat()
        #if path == '/':
        #    st.st_mode = stat.S_IFDIR | 0755
        #    st.st_nlink = 2
        #else:            
        #    st.st_mode = stat.S_IFREG | 0777
        #    st.st_nlink = 1
        #    st.st_size = 1024
        #return st
        
        return os.lstat(self.pathTmpDir + path)

    def readdir(self, path, offset):
        dirents = ['.', '..']
        files = os.listdir(self.pathTmpDir + path)
        for f in files:
            dirents.append(f)
        for r in  dirents:
            yield fuse.Direntry(r)
        
            
    def open(self, path, flags):
        
        pth = self.src + path #/home/jeroen/Desktop/test + /python.png
        comm = "convert " +pth+ " -resize " +self.width+ "x" +self.height+ " /tmp" +path
        
        if not os.path.isfile(pth):
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES
        
        
        #os.popen(comm, "r")
        
    def read(self, path, size, offset):
        imgFile = open("/tmp" + path, "rb")
        imgFile.seek(offset)        
        imgBytes = imgFile.read(size)
        return imgBytes
    
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
