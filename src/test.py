import sys
import os
import platform
from loguru import logger


import config_mycal


from PySide6.QtCore import QSize, Qt ,QCoreApplication,Slot,Signal,QAbstractListModel
from PySide6.QtGui import QAction,QDoubleValidator
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


 #   def MyRecipes(self):
        """this will deal with the recipes"""
        
        #self.RecipeWindow = NewWindow(Title = "List of Recipes")
        #self.RecipeView = QListView()
        #self.RecipeModel = RecipeModel()
        #self.RecipeView.setModel(self.RecipeModel)

        # Create just a simple layout with a box with the recipe titles and a qlistview
        #The title box is just a scroll box
        # The first thing is to get an alphabetic list of the current recipes
        self.Combo=RecipeListCombo = QComboBox()
        #RecipeListCombo.addItems(self.GetRecipeList())
        RecipeListCombo.addItems(['bla','bla1','bla2'])

 
        #RecipeListCombo.currentIndexChanged.connect(self.getSelectedItem())
        RecipeListCombo.currentTextChanged.connect(self.getSelectedItem)
        # Now we get the selected value
        #selected_recipe =self.selected_text

        #logger.info("You have selected %s recipe" % self.selected_text)
        #self.RecipeWindow.setCentralWidget(RecipeListCombo)
        self.setCentralWidget(RecipeListCombo)

        #self.show()
 

        #return
    
    def getSelectedItem(self,s):
        self.selected_text = self.Combo.currentText()
        print(s,self.selected_text)

    def getSelectedItem1(self):
        index = self.Combo.currentIndex()
        if index >= 0:
            self.selected_text = self.Combo.currentText()
            logger.info("You have selected %s recipe" % self.selected_text)

        else:
            logger.warning(" No recipe selected")

        return 


app = QApplication(sys.argv)
window = NewWindow()
#window.MyRecipes()
window.show()
app.exec()
