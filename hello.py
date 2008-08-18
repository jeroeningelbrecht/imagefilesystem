#!/usr/bin/env python

import os, stat, errno, sys, shutil
import fuse
from fuse import Fuse

fuse.fuse_python_api = (0, 2)

#####VARS####
width = "100"
height = "100"

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
    
    def __init__(self,*ar,**kwar):
    
        fuse.Fuse.__init__(self,*ar,**kwar)
        
        self.src = sys.argv[1] #de bronmap
        self.dest = sys.argv[2] #dest map
        
    def wrt(self, str):
        f = open("/tmp/log.txt", 'a')
        f.write(str+"\n")
        
    def getattr(self, path):
        st = MyStat()
        if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        else:
            st.st_mode = stat.S_IFREG | 0444
            st.st_nlink = 1
            st.st_size = 1024
        return st

    def readdir(self, path, offset):
        if path == '/':
            dirents = ['.', '..']
            files = os.listdir(self.src)
            for f in files:
                dirents.append(f)
            for r in  dirents:
                yield fuse.Direntry(r)
        else:
            pass
        
            
    def open(self, path, flags):
        pth = self.src + path #/home/jeroen/Desktop/test + /python.png
        comm = "convert " +pth+ " -resize " +width+ "x" +height+ " /tmp" +path
        self.wrt(comm)
        if not os.path.isfile(pth):
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES
        
        os.popen(comm + "& display /tmp" +path, "r")

    def read(self, path, size, offset):
        return 0
    
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
