
class Logger(object):
    def __init__(self):
        self.f = open("/tmp/log.txt", 'a')
        
    def wrt(self,string):
        self.f.write(string+"\n")
        
    def wrtList(self, list):
        for str in list:
            self.f.write(str+"\n")
    
    def close(self):
        self.f.close()