import os, sys
from getopt import getopt, GetoptError     

'''
Created on Feb 17, 2010

@author: jingle
'''
class ArgumentHandler(object):
    def __init__(self):
        self.destination = None
        self.source = None
        self.configFile = None
        
        #set the configfile, the sourcepath and the destinationpath
        self.handleArguments(sys.argv[1:])
       
    def handleArguments(self, argv):
        try:
            opts, args = getopt(argv, "hc:d:m:s:", ["help", "config=","destination=","mountpoint=","source="])
        except GetoptError:
            self.usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h","--help"):
                self.usage()
                sys.exit()
            elif opt in ("-c","--config"):
                self.configFile = os.path.abspath(arg)
            elif opt in ("-d","--destination","-m","--mountpoint"):
                self.destination = os.path.abspath(arg) #destination folder
                #create the destination folder if it does not exist yet
                if not os.path.isdir(self.destination):
                    os.mkdir(self.destination);
            elif opt in ("-s", "--source"):
                self.source = os.path.abspath(arg) #sourcefolder
            else: self.usage()
                 
    def getDestination(self):
        """ 
        Get the destination path. This is the same as the mountpoint. Note that, if if didn't exist yet, it's created during the initialisation
        """   
        return self.destination
    
    def getSource(self):
        """
        Get the source path. This is the folder which contains the original images.
        """
        return self.source
    
    def getConfigFile(self):
        """
        Get the path of the configuration file.
        """
        return self.configFile
    
    def usage(self):
        print "python PATH_TO_imagefs.py -s/--source [sourcefolder] -d/--destination/-m/--mountpoint[destinationfolder/mountpoint] [-c/--config PATH_TO_configurationXML file]"