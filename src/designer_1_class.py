import os
import sys


from PySide6 import QtCore,QtWidgets
from PySide6.QtUiTools import QUiLoader


loader = QUiLoader()
basedir = os.path.dirname('/Users/klein/git/qt_exercises/src/')


class designer_1(QtCore.QObject):

    def __init__(self):
        super().__init__()
        self.ui = loader.load(
              os.path.join(basedir, "first.ui"), None
          )
        #now we have an init available and we could pas titles etc
        self.ui.setWindowTitle("MyMain")
        self.ui.show()

app = QtWidgets.QApplication(sys.argv) 
ui = designer_1()
app.exec()






app = QtWidgets.QApplication(sys.argv)
window = loader.load(os.path.join(basedir, "mainwindow.ui"), None) 
window.show()
app.exec()
