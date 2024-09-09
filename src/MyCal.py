# Program to calculate calories and other information for 
# recipes. 
import sys
import platform
from loguru import logger


import config_mycal


from PySide6.QtCore import QSize, Qt 
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QVBoxLayout , QGridLayout 
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
)


class MainWindow(QMainWindow):
    def __init__(self, Title =  None , pos_x = 100 , pos_y = 500, size_x = 800 , size_y = 600):
        super().__init__()  # this will the allow to use this as a Subclass

        #with self and using QMainWindow, we can now acces everything through self
        # first we give it the Title


        # Read in the configuration
        self.SetupConfig()
 

        # some constants for json file
 

        # the logging system
        self.SetupLogger()
        self.log_level = self.CM.log_level


        # first get the password
        self.GetPwd()

        # connect to database
        self.ConnectDataBase()
 
        if Title != None:
            self.setWindowTitle(Title)
        else:
            self.setWindowTitle("QMainWindow")

       
        # now we set up geometry
        self.SetSize(size_x,size_y)
        self.SetPosition(pos_x , pos_y)


        self.AddMyMenu()

        # now do the layout
        self.MyLayout()

    def MyLayout(self):
        '''Here I do the layout of the window'''

        # here we create a button widget in the mddle of the mainwindow.
        mylayout = QGridLayout()
        mylayout.addWidget(QDoubleSpinBox(),0,1)
        mylayout.addWidget(QComboBox(),0,0)
        mylayout.addWidget(QDial(),1,0)
        mylayout.addWidget(QDateTimeEdit(),1,1)

        # connect to widget
        mywidget = QWidget()
        mywidget.setLayout(mylayout)
        self.setCentralWidget(mywidget)


    def SetPosition(self,pos_x,pos_y):
        self.move(pos_x,pos_y)

    def SetSize(self,size_x,size_y):
        #self.setBaseSize(size_x,size_y) only works on QWidget
        self.resize(size_x,size_y)


       
    def AddMyMenu(self):   
        '''Now we add a menu'''
        #menubar = QMenuBar(None)
        menubar = self.menuBar()
 
        file_menu = menubar.addMenu("File")
        db_menu = menubar.addMenu("Database")

        # database handling:
         #No menu will show without an action defined
        #Also Quit does not show up since this is already in the intrinsic Python menu.
        # Same for exit

    # here come a few actions, which will be called from the button qwidget
    # When you press a button, it will trigger one or everal events through slots
    # one thing which is important to note ist that one click on a button can have many different meanings
    # DON"T FORGET TO PUT, self IN QACTION

        #here we define the actions: File open section
        file_action = QAction("Open", self)
        file_action.setStatusTip("Opens a file")
        file_action.triggered.connect(self.OpenFile)
        file_menu.addAction(file_action)

     
        #file_menu.addAction("Quit")
   
    
    

        #saving the file
        save_action = QAction("Save", self)
        save_action.setShortcut("CMD+S")
        save_action.setStatusTip('save File')
        save_action.triggered.connect(self.SaveFile)
        file_menu.addAction(save_action)

        db_action_1 = QAction("List Table",self)
        db_action_1.setStatusTip('List database tables')
        db_action_1.triggered.connect(self.ShowTables)
        db_menu.addAction(db_action_1)
        db_action_2 = QAction("save",self)
        db_action_2.setStatusTip('List database tables')
        db_action_2.triggered.connect(self.ShowTables)
        db_menu.addAction(db_action_2)


        file_menu.addAction("MyExit")
        file_menu.addAction("None")
        



    def ConnectDataBase(self):
        ''' establish contact to database'''
        #instantiate the connection
        self.mycal_db  = QSqlDatabase.addDatabase("QPSQL")
        self.mycal_db.setHostName("localhost")
        self.mycal_db.setDatabaseName("newtest.sql")
        self.mycal_db.setUserName("klein")
        self.password = self.password.replace("\n","")
        self.mycal_db.setPassword(self.password)

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

    def GetPwd(self):
 
        with open(self.CM.srcdir+self.CM.cryptofile, 'r') as file:
            self.password = file.read().rstrip()



    def OpenFile(self):
        ''' Open file dialog'''

        self.FileName = QFileDialog.getOpenFileName(self)

    def SaveFile(self):
        name = QFileDialog.getSaveFileName(self,'Save File')
        myfile = open(name,'w')
        text = self.textEdit.toPlainText()
        myfile.write(text)
        myfile.close()




 
    def SetupConfig(self):
        mysystem = platform.system()

        if mysystem == 'Darwin':
            conf_dir = '/Users/klein/git/qt_exercises/config/'
        elif mysystem == 'Linux':
            conf_dir = '/home/klein/git/qt_exercises/config/'
        else:
            print(' This os is not supported %s' % mysystem)
            sys.exit(0)
        config_file = conf_dir + 'config_mycal.json'

        self.CM = CM = config_mycal.MyConfig(config_file)
        self.log_level = CM.log_level
        self.log_output = CM.log_output
        




    def SetupLogger(self):


        logger.remove(0)
        #now we add color to the terminal output
        logger.add(sys.stdout,
                colorize = True,format="<green>{time}</green>    {function}   {line}    {level}     <level>{message}</level>" ,
                level = self.log_level)



        fmt =  "{time} - {name}-   {function} -{line}- {level}    - {message}"
        logger.add(self.log_output, format = fmt , level = self.log_level,rotation="1 day")


        # set the colors of the different levels
        logger.level("INFO",color ='<black>')
        logger.level("WARNING",color='<green>')
        logger.level("ERROR",color='<red>')
        logger.level("DEBUG",color = '<blue>')
 
        return
    
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
       
        self.setCentralWidget(self.mybox)


        return

                       
            

    def ViewTable(self,table):

        model = QSqlTableModel(db = self.mycal_db) 
        model.setTable(table)
        model.select()

        table = QTableView()
        table.setModel(model)
        #self.setCentralWidget(table)


app = QApplication(sys.argv) 
window = MainWindow(Title = "GridLayout")
#window.SetSize(800,500)
#window.SetPosition(100,500)

window.setStyleSheet("background-color: white;")
#window.CreateCalendar()



window.show()
#window.ConnectDataBase()
#window.ViewTable('Recipes')
# now run the app
app.exec()