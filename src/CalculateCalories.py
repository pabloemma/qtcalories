# this is the class dealing with calculating the different values for the
# ConrolDB system for calories. It cac calculate much more than just the calories, depending on the frames
# provided from ControlDB

import pandas as PD
import os
import sys

from loguru import logger



class CalculateCalories(object):
    def __init__(self,myDataFrame = None):
        
        #myDataFrame is a pandas dataframe passed by the instantiating program


        self.SetupLogger()




    def SetupLogger(self):


        logger.remove(0)
        #now we add color to the terminal output
        logger.add(sys.stdout,
                colorize = True,format="<green>{time}</green>    {function}   {line}    {level}     <level>{message}</level>" ,
                level = "INFO")



        fmt =  "{time} - {name}-   {function} -{line}- {level}    - {message}"
        logger.add('info.log', format = fmt , level = 'INFO',rotation="1 day")


        # set the colors of the different levels
        logger.level("INFO",color ='<black>')
        logger.level("WARNING",color='<green>')
        logger.level("ERROR",color='<red>')
        logger.level("DEBUG",color = '<blue>')
 
        return
    
    def calculate_value(self,item = None):

        pass 
