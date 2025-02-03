# this controls the database interactions in pyside6
import sys
import os
import platform
from loguru import logger


import config_mycal


from PySide6.QtCore import QSize, Qt ,QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget 

from PySide6.QtSql import QSqlDatabase , QSql,QSqlTableModel

from PySide6.QtWidgets import (
QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFileDialog,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QTableView,
    QMenuBar,
    QAbstractItemView
)

class ContrlDB(QMainWindow):

    def __init__(self,Title=None,db_name=None,db_user=None,db_system=None,db_pwd = None):
        super().__init__()
        self.db_name = db_name
        self.db_user = db_user
        self.db_system = db_system
        if db_pwd == None:
        
            temp = '/Users/klein/git/qt_exercises/config/pw.txt'
            if os.path.exists(temp):
                with open(temp, 'r') as file:
                    password = file.read().rstrip()
                    self.db_pwd = password
            else:
                self.db_pwd = db_pwd

        self.SetupLogger()
    
    def ConnectDataBase(self):
        ''' establish contact to database'''


        #instantiate the connection
        self.mycal_db  = QSqlDatabase.addDatabase(self.db_system)
        self.mycal_db.setHostName("localhost")
        self.mycal_db.setDatabaseName(self.db_name)
        self.mycal_db.setUserName(self.db_user)
        self.mycal_db.setPassword(self.db_pwd)
        

 #       self.mycal_db.setPassword(self.CM.pwd)

        result = self.mycal_db.open()
        if(result):
            logger.info('connection succsessful')
            # here we get the connection name
            # will be needed when we want to close the connection
            self.connection_name = self.mycal_db.connectionName()
            logger.info(' database connection name %s' % self.connection_name)
            #self.ShowTables()
        else:
            logger.error('connection failed, exciting')
            sys.exit(0)


    def ShowTables(self):
        '''prints all the tables in the databe'''
        self.table_list = self.mycal_db.tables(type=QSql.Tables)
        for k in range(0,len(self.table_list)):
            print(self.table_list[k])

        #Create list box
        self.mybox = QComboBox()
        #Insert at index 0 the whole list
        self.mybox.insertItems(0,self.table_list)
        # create independent window
       
        #self.setCentralWidget(self.mybox)


        return

    def ViewTable(self,table,suppress_columns=[],editmode=True,columnwidth=[]):
        self.table_view = QTableView()

        self.model = QSqlTableModel(db = self.mycal_db) 

 

        self.table_view.setModel(self.model)
        #prevent editing
        if(not editmode):
            self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.model.setTable(table)

        # get rid of columns
        columns_to_remove = suppress_columns
        for cn in columns_to_remove:
            idx = self.model.fieldIndex(cn) 
            self.model.removeColumns(idx, 1)


        self.model.select()
        # change column width
        for k in range(0,len(columnwidth)):
            self.table_view.setColumnWidth(k, columnwidth[k])
 
        self.setMinimumSize(QSize(2024, 600)) 
        
        self.setCentralWidget(self.table_view)

        self.SetPosition(10,10)

        #self.setCentralWidget(table)

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

    def SetPosition(self,pos_x,pos_y):
        self.move(pos_x,pos_y)


app = QApplication(sys.argv) 

Title=None
db_name='recipe_ak'
db_user='klein'
db_system='QPSQL'
db_pwd = None

suppress_columns = ['Sugar',
                    'Portions',
                    'Description',
                    'Saturated_fat',
                    'Fiber',
                    'Salt',
                    'Sodium',
                    'Ingredients',
                    'Time',
                    'Images',
                    'vegetarian']
columnwidth = [40,200,200,200,200,200]

window = ContrlDB(Title = "ControlDB",
                  db_name=db_name,
                  db_user=db_user,
                  db_system=db_system)
#window.SetSize(800,500)
#window.SetPosition(100,500)

window.setStyleSheet("background-color: white;")
#window.CreateCalendar()



window.show()
window.ConnectDataBase()
window.ShowTables()
window.ViewTable('Recipes',suppress_columns=suppress_columns,columnwidth=columnwidth)
# now run the app
app.exec()