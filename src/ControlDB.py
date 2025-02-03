# this controls the database interactions in pyside6
import sys
import os
import platform
from loguru import logger


import config_mycal


from PySide6.QtCore import QSize, Qt ,QCoreApplication
from PySide6.QtGui import QAction
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
)

class ContrlDB(object):

    def __init__(self,db_name=None,db_user=None,db_system=None,db_pwd = None):
        super().__init__()
        self.db_name = db_name
        self.db_user = db_user
        self.db_system = db_system
        self.db_pwd = db_pwd
    
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



