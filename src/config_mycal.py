"""Class to configure the test_speed program
Using json (sigh)"""


import json
import os
import sys
import platform
import socket
import inspect

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class MyConfig():

    def __init__(self,config_file):
        """ config_file contains all the infor for speedtest program"""

 
       
        
        # Open config file
        print('Directory Name:     ', os.path.dirname(__file__))
       

        if os.path.exists(config_file) :
            self.ReadJson(config_file)
        else:
            print(" Config file does not exist, exiting     ", config_file)
            sys.exit(0)

    def ReadJson(self,file_path):

        print("reading config file ", file_path)    
        with open(file_path, "r") as f:
            myconf = json.load(f)

            self.DecodeVariables(myconf)

    def DecodeVariables(self,jsondict):
        """decodes the json dictionary in to variables"""

        #bold face begin and end
        bfb = '\033[1m'
        bfe = '\033[0m'
        TX = color
        #these are depending on the operating system
        mysystem = platform.system()
        self.srcdir = jsondict[mysystem]['srcdir']
        self.datadir = jsondict[mysystem]['datadir']
        self.logdir = jsondict[mysystem]['logdir']
        self.doc_dir =jsondict[mysystem]['doc_dir']

        self.debug = jsondict["Control"]["debug"]
        self.cryptofile = jsondict["Control"]["cryptofile"]
        # the next two vaiables are only used if we run in "both" mode
            #test if first key is working
 
        self.conf_dir = jsondict[mysystem]['conf_dir']

   
        #Possible loglevels
        # DEBUG
        # INFO
        # WARNING
        # ERROR
        # CRITICAL
        
        #Output choices
        # screen
        # outfile
        # both

        if "loglevel" in jsondict["logging"].keys() :
            self.log_level = jsondict["logging"]["loglevel"] 
        else:
            self.log_level = "INFO"

        
        self.log_output = jsondict["logging"]["output"] 
 
        if "log_conf_file" in jsondict["logging"].keys() :
            self.log_conf_file = self.conf_dir+jsondict["logging"]["log_conf_file"] 
        else:
            frame = inspect.currentframe()
            prefix = TX.BOLD +TX.RED+'|'+frame.f_code.co_name+'>'+'no logger config file'+TX.END
            print(prefix)
            sys.exit(0)
             
        #here we get the logging varaibles:
                

        print('\n\n ***************** configuration**************\n')
        print(' We are running on platform ' , mysystem, '\n')

        print('Sourcedir            ',self.srcdir)
        print('Datadir              ',self.datadir)
 
        print('***************************** end of configuration***************\n\n')





if __name__ == '__main__':
    mysystem = platform.system()

    if mysystem == 'Darwin':
        conf_dir = '/Users/klein/git/qt_exercises/config/'
    elif mysystem == 'Linux':
        conf_dir = '/home/klein/git/qt_exercises/config/'
    else:
        print(' Thios os is not supported %s' % mysystem)
    config_file = conf_dir + 'config_mycal.json'
    MyC = MyConfig(config_file)
