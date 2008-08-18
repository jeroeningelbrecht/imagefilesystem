#!/usr/bin/env python

import os, stat, errno, sys, shutil
import fuse
from fuse import Fuse

fuse.fuse_python_api = (0, 2)

hello_str = "Hey"

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
        self.files = []
        #shutil.copytree(self.src, self.dest)
        #self.getFiles(self.src)
        
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
        return 0
        
    def read(self, path, size, offset):
        self.wrt("haha")
        if path != "/":
            return -errno.ENOENT
        slen = len(hello_str)
        if offset < slen:
            if offset + size > slen:
                size = slen - offset
            buf = hello_str[offset:offset+size]
        else:
            buf = ''
        return buf
    
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
