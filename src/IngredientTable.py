# IngedientTable deals with the swiss food nutrition info
# the first iteration is english
#It uses pandas and will eventaully be called from ControDB

import csv
from io import StringIO

from sqlalchemy import create_engine, MetaData
import psycopg2 
import pandas as pd
import numpy as np
import os
import sys
from loguru import logger

from pick_swiss_ingreds import Ui_Dialog

from PySide6.QtCore import (QSize, Qt ,QRect,
QCoreApplication,Slot,Signal,QAbstractListModel,QAbstractTableModel,QMetaObject,QModelIndex)
from PySide6.QtGui import QAction,QDoubleValidator,QFont

from PySide6.QtUiTools import QUiLoader

from PySide6.QtSql import QSqlDatabase , QSql,QSqlTableModel,QSqlQueryModel,QSqlQuery

from PySide6.QtWidgets import (
QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDialog,
    QDoubleSpinBox,
    QFileDialog,
    QFontComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListView,
    QMainWindow,
    QWidget,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QStatusBar,
    QTimeEdit,
    QTableView,
    QMenuBar,
    QVBoxLayout,
    QAbstractItemView,
    QGridLayout,
    QTextEdit

)

class IngredDialog(QDialog,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



# here we setup the model

class IngredModel(QAbstractTableModel):
    def __init__(self, ingredients):
        super().__init__()
        self.ingredients = ingredients

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self.ingredients.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self.ingredients.shape[0]

    def columnCount(self, index):
        return self.ingredients.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.ingredients.columns[section])

            if orientation == Qt.Vertical:
                return str(self.ingredients.index[section])




class IngredientTable(QMainWindow):
    def __init__(self,table_name = None,ingredients = None):
        super().__init__()

        self.setup_logger()



        db_file = '/Users/klein/git/wt_exercises/nutition_databases/swiss_food.csv'
        self.INTview = QTableView()
        if(table_name == None):
            self.read_table(db_file)
            ingredients = self.df
        
        else:
            #new to get the da and put it into pandas   
                conn_string = 'postgresql://klein:?Pa!blo?solveig@192.168.2.164:5432/recipe_ak'
                engine = create_engine(conn_string)
                conn = engine.connect()
                sql = "SELECT * FROM "+table_name+";"
                ingredients = self.df= pd.read_sql_query(sql, conn)
                print(self.df)


        self.IngredModel = IngredModel(ingredients)
        self.INTview.setModel(self.IngredModel)

        #if I click on a cell go to connect
        self.INTview.clicked.connect(self.print_cell)

        #Set geometry of table_view
        self.mod_table_display()

        self.setCentralWidget(self.INTview)
        self.setGeometry(20, 20, 1200, 400)

    def setup(self):
        """Only called when ingredienttable is called as standalone"""

    def find_pattern(self,word=None):
        """this routine goes through the names in the database
        and returns a list of values which will then go into a combo_box dialog to choose from
        the names are in cloumn 0
        returns the list of matches together with how many times it found a match
        count =1 for exactly one match.
        """
        self.pattern_count=0 # how many times the pattern was found

        self.myPatternFound = []
        temp = self.df['name'].to_list()
        # we check for the first three characters case insensitive
        for k in range(len(temp)):
            needle = "TEST"
            if word[0:4].casefold() in temp[k][0:4].casefold():
                self.myPatternFound.append(temp[k])
                self.pattern_count = self.pattern_count +1
        
        return  


    def get_ingredient(self):

        self.GI = IngredDialog()
        self.GI.setModal(True)
 
        #populate the values
        
        self.GI.comboPick.insertItems(0,self.myPatternFound)

        self.GI.comboPick.textHighlighted.connect(self.get_ingred_selection)
        self.GI.comboPick.currentTextChanged.connect(self.get_ingred_selection)
        self.GI.move(800,10)
 #       self.GI.setModal(True)
        #self.GI.show()
        self.GI.exec()
        return
    
    def get_ingred_selection(self,s):

        self.selected_ingredient = s
        logger.debug("you selected %s" % self.selected_ingredient)

        # get the values from the df
        myindex = self.df.loc[self.df['name'] == s].index[0]
        myvalues = self.df.iloc[myindex].to_list()
        self.ingredient_name = myvalues[0]
        self.energy = myvalues[1]
        self.fat = myvalues[2]
        self.carbohydrate = myvalues[3]
        self.sugar = myvalues[4]
        self.fiber = myvalues[5]
        self.protein = myvalues[6]
        self.salt = myvalues[7]


        
        return

    
 




             


    def mod_table_display(self):
        """modify how the table looks"""
        self.INTview.resizeColumnsToContents()

    def print_cell(self,index):

        #all data communication happes through self.IngredModel.ingredients
        row = index.row()
        column = index.column()
        data = index.data()

        logger.debug("you selected %s " %self.IngredModel.ingredients.iloc[index.row(), index.column()])

    def read_table(self,table = None):
        """reads the csv ingredients file"""

        self.df = pd.read_csv(table)



    def setup_logger(self):
 
        #logger.remove(0)
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

    def do_sql_table(self):
        """dont forget to put  for xxxx"""
        conn_string = 'postgresql://klein:xxxx@192.168.2.164:5432/recipe_ak'
        engine = create_engine(conn_string)
        conn = engine.connect()
        self.df.to_sql('swiss_food', con=conn, if_exists= "replace" , index = False)

        conn = psycopg2.connect(conn_string 
                        )
        conn.autocommit = True
        cursor = conn.cursor() 
  
        sql1 = '''select * from swiss_food;'''
        cursor.execute(sql1) 
        for i in cursor.fetchall(): 
            print(i) 
  
        # conn.commit() 
        conn.close() 


    def psql_insert_copy(table, conn, keys, data_iter):
    # gets a DBAPI connection that can provide a cursor
        dbapi_conn = conn.connection
        with dbapi_conn.cursor() as cur:
            s_buf = StringIO()
            writer = csv.writer(s_buf)
            writer.writerows(data_iter)
            s_buf.seek(0)

            columns = ', '.join('"{}"'.format(k) for k in keys)
            if table.schema:
                table_name = '{}.{}'.format(table.schema, table.name)
            else:
                table_name = table.name

            sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
                table_name, columns)
            cur.copy_expert(sql=sql, file=s_buf)



if __name__ == '__main__': 

    app = QApplication(sys.argv)





    table_name = 'swiss_food'
    
    InTa  = IngredientTable(table_name=table_name)
 #   InTa.do_sql_table()
    InTa.find_pattern(word='Almond')
    InTa.get_ingredient()
    InTa.show()


    app.exec()