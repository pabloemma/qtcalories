import os
import sys


from PySide6 import QtWidgets
from PySide6.QtUiTools import QUiLoader
basedir = os.path.dirname('/Users/klein/git/qt_exercises/src/')

loader = QUiLoader()
# note this doe not have an init , so in order to manipulate windows, 
#like giving it a title
#we have to use a function

def mainwindow_setup(w):
    w.setWindowTitle("main window")

app = QtWidgets.QApplication(sys.argv)
window = loader.load(os.path.join(basedir, "first.ui"), None) 
mainwindow_setup(window)
window.show()
app.exec()

