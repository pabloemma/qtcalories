# main clory program
# this will be the overall control of the calory program
# it creates a meun, reads in the configuration and
# drives the program


import config_mycal as CM       # get the configuration classs
import ControlDB as CDB         # get the ControlDB

import os
import sys
import platform
from loguru import logger

from PySide6.QtWidgets import (QApplication,
                               QFileDialog, 
                                QMainWindow, 
                                QMenu,
                                QPushButton)
from PySide6.QtGui import QAction, QIcon

basedir = os.path.dirname(__file__)


class CalMain(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calory Control")


        #instantiate configuration
        self.SetupConfig()

        self.SetupLogger()

        # now instantiate the heart of the calory
        self.CDB = CDB.ContrlDB("My Calories",
                                db_name=self.CM.db_name,
                                db_user = self.CM.db_user,
                                 db_system = self.CM.db_system ,
                                 db_pwd = self.CM.db_pwd
                                 )



        self.log_level = self.CM.log_level

        #connect to database
        self.CDB.ConnectDataBase()
  
        menu = self.menuBar()

        file_menu = menu.addMenu("&Action")

        # Create a "List Recipes" action
        new_action = QAction( "List Recipes", self)
        new_action.setShortcut("Ctrl+L")
        new_action.setStatusTip("list recipes")
        new_action.triggered.connect(self.list_recipes)
        file_menu.addAction(new_action)



    def SetupConfig(self):
        mysystem = platform.system()

        # get the config filename
        # here we do a filedialog
        fileName , filter = QFileDialog.getOpenFileName(self,
        self.tr("Open Config file"), "~", self.tr("*.json"))
        print(fileName)


 
        self.CM = CM.MyConfig(fileName)
        self.log_level = self.CM.log_level
        self.log_output = self.CM.log_output

 
    def SetupLogger(self):


        logger.remove(0)
        #now we add color to the terminal output
        logger.add(sys.stdout,
                colorize = True,format="<green>{time}</green>    {function}   {line}    {level}     <level>{message}</level>" ,
                level = "DEBUG")



        fmt =  "{time} - {name}-   {function} -{line}- {level}    - {message}"
        logger.add('info.log', format = fmt , level = 'INFO',rotation="1 day")


        # set the colors of the different levels
        logger.level("INFO",color ='<black>')
        logger.level("WARNING",color='<green>')
        logger.level("ERROR",color='<red>')
        logger.level("DEBUG",color = '<blue>')
 
        return

 


    def list_recipes(self):
        """list all the recipes"""
        columnwidth = [40,200,200,200,200,200]
        self.CDB.ViewTable('recipes',suppress_columns=self.CM.recipes_suppress_columns,columnwidth=columnwidth)



 
    def quit_app(self):
        print("closing down")
        self.close()

    def print_app(self):
        print("shit")

    def new_document(self):
        print("more shit")

if __name__ == "__main__":
    app = QApplication([])
    window = CalMain()
    window.show()
    app.exec()