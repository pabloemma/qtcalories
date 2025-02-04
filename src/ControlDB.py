# this controls the database interactions in pyside6
import sys
import os
import platform
from loguru import logger


import config_mycal


from PySide6.QtCore import QSize, Qt ,QCoreApplication,Slot,Signal
from PySide6.QtGui import QAction,QDoubleValidator
from PySide6.QtWidgets import QWidget 
from PySide6.QtUiTools import QUiLoader

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
    QFormLayout,
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
    QVBoxLayout,
    QAbstractItemView,
    QGridLayout,
    QTextEdit
    
)

class NewWindow(QMainWindow):
        def __init__(self,Title =  None):
            super().__init__()
            layout = QVBoxLayout()

            self.label = QLabel("Another Window")
            if(Title == None):
                self.setWindowTitle("MyCal")
            else:
                self.setWindowTitle(Title)
        
            layout.addWidget(self.label)
            self.setLayout(layout)



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
        #self.CreateIngredientsForm()
        
    
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

        self.show()
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

    def CreateIngredientsForm1(self):
        """uses the form layout"""
    
       #always use self so window wll be persistent
        self.Inform = NewWindow(Title = "Add New Ingredient")
        self.Inform.setStyleSheet("background-color: yellow;")
     
        # setup geometry
        mysize=[400,300]
        myposit = [200,100]
    
        self.SizeWindow(self.Inform,myposit,mysize)

        # Create widgets
        self.name_label      = QLineEdit()
        self.name_label.setStyleSheet("background-color: white")
        # force valid entr
        double_validator = QDoubleValidator(0, 500.0, 2)
 
        self.calory_label    = QLineEdit()
        self.calory_label.setStyleSheet("background-color: white")
        self.calory_label.setValidator(double_validator)
        
        self.carb_label      = QLineEdit()
        self.carb_label.setStyleSheet("background-color: white")
        self.carb_label.setValidator(double_validator)
        self.fat_label       = QLineEdit()
        self.fat_label.setStyleSheet("background-color: white")
        self.fat_label.setValidator(double_validator)
        self.prot_label      = QLineEdit() 
        self.prot_label.setStyleSheet("background-color: white")
        self.prot_label.setValidator(double_validator)
 
        SaveButton = QPushButton("Save")
        SaveButton.setStyleSheet("background-color: white")
        CancelButton = QPushButton("Cancel")
        CancelButton.setStyleSheet("background-color: red")

 
        # Create layout
        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name_label)
        form_layout.addRow("Calories/100g", self.calory_label)
        form_layout.addRow("Fat", self.fat_label)
        form_layout.addRow("Carbohydrates", self.carb_label)
        form_layout.addRow("Protein", self.prot_label)
        form_layout.addRow(SaveButton)
        form_layout.addRow(CancelButton)

        mylayout = QVBoxLayout()
        mylayout.addLayout(form_layout)
        self.setLayout(mylayout)

        # Connect submit button
        SaveButton.clicked.connect(self.SaveIngredients)
        CancelButton.clicked.connect(lambda : self.Cancel(self.Inform))

        widget = QWidget()
        widget.setLayout(mylayout)
         




        self.Inform.setCentralWidget(widget)

        #for label in MyLabel:
        #    widget = QWidget()
        #    widget.setLayout(layout)
        #self.setCentralWidget(widget)


        # create the form

        self.Inform.show()
 




    def CreateIngredientsForm(self):
        """Hopefully creates the ingredients"""

        #always use self so window wll be persistent
        self.Inform = NewWindow(Title = "Add New Ingredient")
     
        # setup geometry
        mysize=[700,500]
        myposit = [200,100]
    
        self.SizeWindow(self.Inform,myposit,mysize)

        # We are laying out things on a grid 2 wide and 4 deep
        mylayout = QGridLayout()
        #do the labels
        mylabel = ['Name','Calories/100g','Fat','Carbohydrates','Protein']
        k=0
        for lab in mylabel:
            mylayout.addWidget(QLabel(lab),k,0)
            mylayout.addWidget(QLineEdit(),k,1)
            
            k+=1
        # finally add cancel and save button
        SaveButton = QPushButton("Save")
        CancelButton = QPushButton("Cancel")

        #Setup signal:
        SaveButton.clicked.connect(self.SaveIngredients)
        CancelButton.clicked.connect(lambda : self.Cancel(self.Inform))




        mylayout.addWidget(CancelButton,k,0)
        mylayout.addWidget(SaveButton,k,1)
 

        
 
        widget = QWidget()
        widget.setLayout(mylayout)
         




        self.Inform.setCentralWidget(widget)

        #for label in MyLabel:
        #    widget = QWidget()
        #    widget.setLayout(layout)
        #self.setCentralWidget(widget)


        # create the form

        self.Inform.show()
 

    def SizeWindow(self,window,myposit,mysize):
        """resizes the specified window ,where the parameters are two integer lists"""
        window.setGeometry(myposit[0],myposit[1],mysize[0],mysize[1])
        return
 

##########################################################################
    # section for signals and slots

    
    def Cancel(self,window):
        """ closes window without anything"""
        window.destroy()
        
 
 

    def SaveIngredients(self):
        """saving the ingredients"""
        Ing_name    = self.name_label.text()
        Ing_calory  = float(self.calory_label.text())
        Ing_carb    = float(self.carb_label.text())       
        Ing_fat     = float(self.fat_label.text())
        Ing_prot    = float(self.prot_label.text())

        #Check all fields are filled out
        if(Ing_calory !="" and Ing_carb !="" and Ing_fat!=""  and Ing_prot !=""):
            self.Inform.destroy()
        
    

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



#window.show()
window.ConnectDataBase()
window.ShowTables()
#window.ViewTable('Recipes',suppress_columns=suppress_columns,columnwidth=columnwidth)
window.CreateIngredientsForm1()

# now run the app
app.exec()