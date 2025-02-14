import sys
from missing_ingredient import Ui_MissingIngredient

import pandas as PD # to pack the recipe information into a pandas dataframe


from PySide6.QtCore import (QSize, Qt ,QRect,
QCoreApplication,Slot,Signal,QAbstractListModel,QAbstractTableModel,QMetaObject,QModelIndex)
from PySide6.QtGui import QAction,QDoubleValidator,QFont
from PySide6.QtWidgets import QWidget 
from PySide6.QtUiTools import QUiLoader

from PySide6.QtSql import QSqlDatabase , QSql,QSqlTableModel,QSqlQueryModel,QSqlQuery

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
    QHBoxLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QListView,
    QMainWindow,
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


class MyMissIngWindow(QMainWindow,Ui_MissingIngredient):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class test((QMainWindow)):
    def __init__(self):
        super().__init__()
 
    def MyMissingIngredients(self):
        """ form if ingredient is missing"""
        self.MMI = MyMissIngWindow()
        self.MMI.move(10,50)
        self.MMI.show()
        self.MMI.IngredLine.setText('shit')
        #self.MMI.EditIngButton.clicked.connect(self.show_ingred_form())
        #self.MMI.CloseButton.clicked.connect(self.Cancel(self.MMI))


app = QApplication(sys.argv)

window = test()
window.MyMissingIngredients()
#window.SetSize(800,500)
#window.move(10,50)

window.setStyleSheet("background-color: white;")
#window.CreateCalendar()



#window.show()

# now run the app
app.exec()