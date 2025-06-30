# main clory program
# this will be the overall control of the calory program
# it creates a meun, reads in the configuration and
# drives the program


import config_mycal as CM       # get the configuration classs
import ControlDB_new as CDB         # get the ControlDB

from database_connect import Ui_db_dialog

import os
import sys
import platform
from loguru import logger

from PySide6.QtWidgets import (QApplication,
                               QFileDialog,
                               QDialog, 
                               QLabel,
                                QMainWindow, 
                                QMenu,
                                QPushButton,
                                QVBoxLayout,
                                QWidget)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtUiTools import QUiLoader
basedir = os.path.dirname(__file__)


loader = QUiLoader()
basedir = os.path.dirname(__file__)


class database_dialog(QDialog,Ui_db_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



class CalMain(QMainWindow):
    def __init__(self,config_file = None):
        super().__init__()

        self.setWindowTitle("Calory Control")
        myLabel = QLabel("calory program vs 1.0")
        myCloseButton = QPushButton("Close")
        myCloseButton.clicked.connect(self.close_app)
        layout= QVBoxLayout()
        layout.addWidget(myLabel)
        layout.addWidget(myCloseButton)


        widget = QWidget()
        widget.setLayout(layout)

 

        self.setCentralWidget(widget)
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

   # Create a " calculate portion" action
        portion_action = QAction( " Calculate Portion Calories", self)
        portion_action.setShortcut("Ctrl+P")
        portion_action.setStatusTip("calculate calories of portion")
        portion_action.triggered.connect(self.calculate_portion)
        file_menu.addAction(portion_action)


   # Create a " config" action
        config_action = QAction( " Config File", self)
        config_action.setShortcut("Ctrl+F")
        config_action.setStatusTip("change config file")
        config_action.triggered.connect(self.SetupConfig)
        file_menu.addAction(config_action)

   # Create a " connect db" action
        db_action = QAction( " Connect Database", self)
        db_action.setStatusTip("connect database ")
        db_action.triggered.connect(self.connect_db)
        file_menu.addAction(db_action)

        #instantiate configuration
        
        self.SetupConfig()

        self.SetupLogger()

        # now instantiate the heart of the calory
        self.CDB = CDB.ContrlDB_new("My Calories",
                                db_name=self.CM.db_name,
                                db_user = self.CM.db_user,
                                 db_system = self.CM.db_system ,
                                 db_pwd = self.CM.db_pwd,
                                 config_file = self.config_file
                                 )



        self.log_level = self.CM.log_level
        self.ingred_table = self.CM.ingred_table
        

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
        #self.config_file = None

 
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
        self.CDB.ViewTable(self.ingred_table,suppress_columns=self.CM.ingredients_suppress_columns,columnwidth=columnwidth)

    def control_recipes(self):
        self.CDB.MyRecipes_new()

    def add_ingredients(self):
        self.CDB.CreateIngredientsForm1()
        
    def close_app(self):
        logger.info("closing down")
        self.close()

    def calculate_portion(self):

        myrecipe1 = 'salad_ak'
        myportion1 = 100.
        self.CDB.calculate_portion_calory(myrecipe1,myportion1)

        pass

    def connect_db(self):

        # here we populate the database table
        self.DBD = database_dialog()  #instantiate the databse dialog
        # now populate the fields with the current values
        self.DBD.user_edit.setText(self.CM.db_user)
        #self.DBD.user_edit.returnPressed.connect(self.db_user_name_changed)
        self.DBD.user_edit.textChanged.connect(self.db_user_name_changed)
        self.DBD.name_edit.setText(self.CM.db_name)
        self.DBD.name_edit.textChanged.connect(self.db_db_name_changed)
        self.DBD.system_edit.setText(self.CM.db_system)
        self.DBD.system_edit.textChanged.connect(self.db_system_changed)

        self.DBD.adress_edit.setText(self.CM.db_address)
        self.DBD.adress_edit.textChanged.connect(self.db_adress_changed)

        self.DBD.password_edit.setText(self.CM.db_pwd)
        self.DBD.password_edit.textChanged.connect(self.db_pwd_changed)

        self.DBD.buttonBox.accepted.connect(self.db_dialog_accept)
        self.DBD.buttonBox.rejected.connect(self.db_dialog_reject)

        self.DBD.exec()  # now display the dialog (it is modal, so nothing else will have control)


        return
    
    def db_dialog_accept(self):
        self.CM.db_user = self.DBD.user_edit.text()
        self.CM.db_name = self.DBD.name_edit.text()
        self.CM.db_system = self.DBD.system_edit.text()
        self.CM.db_address = self.DBD.adress_edit.text()
        self.CM.db_pwd = self.DBD.password_edit.text()
    
    
        self.CDB = CDB.ContrlDB_new("My Calories",
                                db_name=self.CM.db_name,
                                db_user = self.CM.db_user,
                                 db_system = self.CM.db_system ,
                                 db_pwd = self.CM.db_pwd,
                                 config_file = self.config_file
                                 )
        self.CDB.ConnectDataBase()



        return

    def db_dialog_reject(self):
        self.DBD.close()
        return

    def db_user_name_changed(self):
        self.CM.db_user = self.DBD.user_edit.text()
        return
    
    def db_db_name_changed(self):
        self.CM.db_name = self.DBD.name_edit.text()
        return
    
    def db_system_changed(self):
        self.CM.db_system = self.DBD.system_edit.text()
        return
    
    def db_adress_changed(self):
        self.CM.db_address = self.DBD.adress_edit.text()
        return
    
    def db_pwd_changed(self):
        self.CM.db_pwd = self.DBD.password_edit.text()  
        return

if __name__ == "__main__":
    app = QApplication([])
    config_file = '/Users/klein/git/qt_exercises/config/config_mycal.json'
    window = CalMain(config_file = config_file )
    window.show()
    app.exec()