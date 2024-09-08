# with this class I am trying to set up the first qt window
import sys



from PySide6.QtCore import QSize, Qt 
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QVBoxLayout , QGridLayout 
from PySide6.QtWidgets import QWidget 
from PySide6.QtSql import QSqlDatabase 




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
)


class MainWindow(QMainWindow):
    def __init__(self, Title =  None , pos_x = 100 , pos_y = 500, size_x = 800 , size_y = 600):
        super().__init__()  # this will the allow to use this as a Subclass

        #with self and using QMainWindow, we can now acces everything through self
        # first we give it the Title

        # first get the password
        self.GetPwd()
 
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
        mylayout.addWidget(QPushButton(),0,0)
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
        #menubar = QMenuBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        #No menu will show without an action defined
        #Also Quit does not show up since this is already in the intrinsic Python menu.
        # Same for exit

    # here come a few actions, which will be called from the button qwidget
    # When you press a button, it will trigger one or everal events through slots
    # one thing which is important to note ist that one click on a button can have many different meanings


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


        file_menu.addAction("MyExit")
        file_menu.addAction("None")
        

    def OpenFile(self):
        ''' Open file dialog'''

        self.FileName = QFileDialog.getOpenFileName(self)

    def SaveFile(self):
        name = QFileDialog.getSaveFileName(self,'Save File')
        myfile = open(name,'w')
        text = self.textEdit.toPlainText()
        myfile.write(text)
        myfile.close()


    def ConnectDataBase(self):
        ''' establish contact to database'''
        #instantiate the connection
        mydb = QSqlDatabase.addDatabase("QPSQL")
        mydb.setHostName("localhost")
        mydb.setDatabaseName("newtest.sql")
        mydb.setUserName("klein")
        self.password = self.password.replace("\n","")
        mydb.setPassword(self.password)

        result = mydb.open()
        if(result):
            print('connection succsessful')
        else:
            print('connection failed')

    def GetPwd(self):
        #for line in open('/Users/klein/git/qt_exercises/src/pw.txt',encoding="utf8"):
        #for line in open('/Users/klein/git/qt_exercises/src/pw.txt'):
        #    print(line)
        #    self.password = line

        with open('/Users/klein/git/qt_exercises/src/pw.txt', 'r') as file:
            self.password = file.read().rstrip()


app = QApplication(sys.argv) 
window = MainWindow(Title = "GridLayout")
#window.SetSize(800,500)
#window.SetPosition(100,500)

window.setStyleSheet("background-color: white;")
#window.CreateCalendar()



window.show()
window.ConnectDataBase()

# now run the app
app.exec()