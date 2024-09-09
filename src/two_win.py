import sys



from PySide6.QtCore import QSize, Qt 
from PySide6.QtGui import QAction, QWindow
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

class MySecondWindow(QWidget):
    """" Create a second window"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        mylabel = QLabel("my second window")
        layout.addWidget(mylabel)
        self.setLayout(layout)



class MainWindow(QMainWindow):
    def __init__(self, Title =  None , pos_x = 100 , pos_y = 500, size_x = 800 , size_y = 600):
        super().__init__()  # this will the allow to use this as a Subclass

        #with self and using QMainWindow, we can now acces everything through self
        # first we give it the Title

        # first get the password
 
        if Title != None:
            self.setWindowTitle(Title)
        else:
            self.setWindowTitle("QMainWindow")

       
        # now we set up geometry
        self.SetSize(size_x,size_y)
        self.SetPosition(pos_x , pos_y)

        mywidget = QPushButton("mybox")
        self.setCentralWidget(mywidget)


        self.w = MySecondWindow()
        self.w.setWindowTitle("test2")
        self.w.show()


    def SetPosition(self,pos_x,pos_y):
        self.move(pos_x,pos_y)

    def SetSize(self,size_x,size_y):
        #self.setBaseSize(size_x,size_y) only works on QWidget
        self.resize(size_x,size_y)

    
        

app = QApplication(sys.argv) 
window = MainWindow(Title = "GridLayout")
#window.SetSize(800,500)
#window.SetPosition(100,500)

window.setStyleSheet("background-color: white;")
#window.CreateCalendar()



window.show()
app.exec()