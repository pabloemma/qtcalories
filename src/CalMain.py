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
                               QLabel,
                                QMainWindow, 
                                QMenu,
                                QPushButton)
from PySide6.QtGui import QAction, QIcon

basedir = os.path.dirname(__file__)


class CalMain(QMainWindow):
    def __init__(self,config_file = None):
        super().__init__()

        self.setWindowTitle("Calory Control")
        myLabel = QLabel("calory program vs 1.0")
        self.setCentralWidget(myLabel)
        self.show()

        self.config_file = config_file

        #setup menu
        menu = self.menuBar()

        file_menu = menu.addMenu("&Action")

        # Create a "List Recipes" action
        list_action = QAction( "List Recipes", self)
        list_action.setShortcut("Ctrl+L")
        list_action.setStatusTip("list recipes")
        list_action.triggered.connect(self.list_recipes)
        file_menu.addAction(list_action)

       # Create a "List Ingredients" action
        list_i_action = QAction( "List Ingredients", self)
        list_i_action.setShortcut("Ctrl+I")
        list_i_action.setStatusTip("list Ingredients")
        list_i_action.triggered.connect(self.list_ingredients)
        file_menu.addAction(list_i_action)

        # Create a " Recipe control" action
        recipe_action = QAction( " Recipes", self)
        recipe_action.setShortcut("Ctrl+R")
        recipe_action.setStatusTip("control recipes")
        recipe_action.triggered.connect(self.control_recipes)
        file_menu.addAction(recipe_action)

       # Create a " add ingredients" action
        ingredients_action = QAction( " Add Ingredients", self)
        ingredients_action.setShortcut("Ctrl+A")
        ingredients_action.setStatusTip("add ingredients")
        ingredients_action.triggered.connect(self.add_ingredients)
        file_menu.addAction(ingredients_action)

   # Create a " config" action
        config_action = QAction( " Config File", self)
        config_action.setShortcut("Ctrl+F")
        config_action.setStatusTip("change config file")
        config_action.triggered.connect(self.SetupConfig)
        file_menu.addAction(config_action)


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
  



    def SetupConfig(self):
        mysystem = platform.system()

        # get the config filename
        # here we do a filedialog
        if(self.config_file == None or not os.path.isfile(self.config_file)):
            self.config_file , filter = QFileDialog.getOpenFileName(self,
                                self.tr("Open Config file"), "~", self.tr("*.json"))
           
            
        logger.info("config file %s" % self.config_file)


 
        self.CM = CM.MyConfig(self.config_file)
        self.log_level = self.CM.log_level
        self.log_output = self.CM.log_output
        #reset self.config_file, so we can change it through the menu
        self.config_file = None

 
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

    def list_ingredients(self):
        """list all the recipes"""
        columnwidth = [200,100,100,100,100,100]
        self.CDB.ViewTable('ingredients',suppress_columns=self.CM.ingredients_suppress_columns,columnwidth=columnwidth)

    def control_recipes(self):
        self.CDB.MyRecipes_new()

    def add_ingredients(self):
        self.CDB.CreateIngredientsForm1()
        
    def quit_app(self):
        print("closing down")
        self.close()

    def print_app(self):
        print("shit")

    def new_document(self):
        print("more shit")

if __name__ == "__main__":
    app = QApplication([])
    config_file = '/Users/klein/git/qt_exercises/config/config_mycal.json'
    window = CalMain(config_file = config_file )
    window.show()
    app.exec()