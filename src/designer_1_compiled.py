# this is an example of inlcuing the first.ui file through a python conversion
# first you have to translate ui file to py
#with pyside6 first.ui -o first.py
# the advice however i to design all the windows in QT designer
import sys


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow
from first import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow): 
     def __init__(self):
          super().__init__()
          self.setupUi(self)
          self.show()


app = QApplication(sys.argv) 
w = MainWindow()
app.exec()
