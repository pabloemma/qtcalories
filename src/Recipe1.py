# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Recipe1.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTableView,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.SaveRecipe = QPushButton(self.centralwidget)
        self.SaveRecipe.setObjectName(u"SaveRecipe")
        self.SaveRecipe.setGeometry(QRect(320, 410, 100, 32))
        self.NewRecipe = QPushButton(self.centralwidget)
        self.NewRecipe.setObjectName(u"NewRecipe")
        self.NewRecipe.setGeometry(QRect(430, 410, 100, 32))
        self.RecipeListCombo = QComboBox(self.centralwidget)
        self.RecipeListCombo.setObjectName(u"RecipeListCombo")
        self.RecipeListCombo.setGeometry(QRect(550, 410, 151, 32))
        self.RecipeListCombo.setEditable(True)
        self.RecipeListCombo.setMaxVisibleItems(20)
        self.CaloryLabel = QLabel(self.centralwidget)
        self.CaloryLabel.setObjectName(u"CaloryLabel")
        self.CaloryLabel.setGeometry(QRect(30, 60, 101, 31))
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.CaloryLabel.setFont(font)
        self.TotCal = QLineEdit(self.centralwidget)
        self.TotCal.setObjectName(u"TotCal")
        self.TotCal.setGeometry(QRect(180, 60, 113, 31))
        self.Cal100 = QLabel(self.centralwidget)
        self.Cal100.setObjectName(u"Cal100")
        self.Cal100.setGeometry(QRect(30, 120, 121, 31))
        self.Cal100.setFont(font)
        self.cal100_out = QLineEdit(self.centralwidget)
        self.cal100_out.setObjectName(u"cal100_out")
        self.cal100_out.setGeometry(QRect(180, 120, 113, 31))
        self.protein = QLabel(self.centralwidget)
        self.protein.setObjectName(u"protein")
        self.protein.setGeometry(QRect(30, 170, 121, 31))
        self.protein.setFont(font)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(180, 170, 113, 31))
        self.CancelButton = QPushButton(self.centralwidget)
        self.CancelButton.setObjectName(u"CancelButton")
        self.CancelButton.setGeometry(QRect(390, 470, 231, 61))
        font1 = QFont()
        font1.setPointSize(18)
        self.CancelButton.setFont(font1)
        self.CancelButton.setAutoFillBackground(False)
        self.IngredientsLabel = QLabel(self.centralwidget)
        self.IngredientsLabel.setObjectName(u"IngredientsLabel")
        self.IngredientsLabel.setGeometry(QRect(407, 19, 211, 31))
        font2 = QFont()
        font2.setPointSize(23)
        self.IngredientsLabel.setFont(font2)
        self.IngredientsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.RecipeTableView = QTableView(self.centralwidget)
        self.RecipeTableView.setObjectName(u"RecipeTableView")
        self.RecipeTableView.setGeometry(QRect(320, 60, 391, 341))
        self.RecipeTableView.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.AddRowButton = QPushButton(self.centralwidget)
        self.AddRowButton.setObjectName(u"AddRowButton")
        self.AddRowButton.setGeometry(QRect(320, 440, 371, 32))
        palette = QPalette()
        brush = QBrush(QColor(240, 57, 49, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        self.AddRowButton.setPalette(palette)
        font3 = QFont()
        font3.setPointSize(21)
        font3.setBold(False)
        self.AddRowButton.setFont(font3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 37))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.SaveRecipe.setText(QCoreApplication.translate("MainWindow", u"Save Recipes", None))
        self.NewRecipe.setText(QCoreApplication.translate("MainWindow", u"New Recipe", None))
        self.CaloryLabel.setText(QCoreApplication.translate("MainWindow", u"Total Calories", None))
        self.Cal100.setText(QCoreApplication.translate("MainWindow", u"Calories per gram", None))
        self.protein.setText(QCoreApplication.translate("MainWindow", u"Protein per gram", None))
        self.CancelButton.setText(QCoreApplication.translate("MainWindow", u"Cancel", None))
        self.IngredientsLabel.setText(QCoreApplication.translate("MainWindow", u"Ingredients", None))
#if QT_CONFIG(tooltip)
        self.AddRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Add row to table", None))
#endif // QT_CONFIG(tooltip)
        self.AddRowButton.setText(QCoreApplication.translate("MainWindow", u"AddRow", None))
    # retranslateUi

