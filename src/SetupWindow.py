# with this class I am trying to set up the first qt window
import sys



from PySide6.QtCore import QSize, Qt 
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
      QApplication,
      QMainWindow,
      QPushButton,
      QCalendarWidget,
      QDoubleSpinBox,
      QMenuBar,
      QFileDialog)


class MainWindow(QMainWindow):
    def __init__(self, Title =  None , pos_x = 100 , pos_y = 500, size_x = 800 , size_y = 600):
        super().__init__()  # this will the allow to use this as a Subclass

        #with self and using QMainWindow, we can now acces everything through self
        # first we give it the Title
        if Title != None:
            self.setWindowTitle(Title)
        else:
            self.setWindowTitle("QMainWindow")

       
        # now we set up geometry
        self.SetSize(size_x,size_y)
        self.SetPosition(pos_x , pos_y)

        # create the calendar
        #self.CreateCalendar()

        self.AddMyMenu()



        # here we create a button widget in the mddle of the mainwindow.

        mybutton = QPushButton("press me and see what is happening")
        # put the button in the middle of the main window
        self.setCentralWidget(mybutton)

        # now here we et up that checked is true.
        mybutton.setCheckable(True)
        mybutton.clicked.connect(self.TheButtonWasChecked)
        mybutton.clicked.connect(self.TheButtonWasClicked)


    def SetPosition(self,pos_x,pos_y):
        self.move(pos_x,pos_y)

    def SetSize(self,size_x,size_y):
        #self.setBaseSize(size_x,size_y) only works on QWidget
        self.resize(size_x,size_y)

    def CreateCalendar(self):
        '''we are putting a calendar into the main window'''
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)

        # and now we set it into the main window
        self.setCentralWidget(calendar)

    # the actions based on button checked
    def TheButtonWasChecked(self):
        print("the button was checked")

    def TheButtonWasClicked(self):
        self.DoubleSpin = QDoubleSpinBox()
        self.setCentralWidget(self.DoubleSpin)
        self.DoubleSpin.setSingleStep(10.)
        self.DoubleSpin.valueChanged.connect(self.spinvaluechange)

    def spinvaluechange(self):
        print("the new value is",self.DoubleSpin.value())
       
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





app = QApplication(sys.argv) 
window = MainWindow(Title = "my first test")
#window.SetSize(800,500)
#window.SetPosition(100,500)

window.setStyleSheet("background-color: white;")
#window.CreateCalendar()



window.show()

# now run the app
app.exec()