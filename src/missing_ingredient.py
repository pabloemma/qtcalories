# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'missing_ingredient.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MissingIngredient(object):
    def setupUi(self, MissingIngredient):
        if not MissingIngredient.objectName():
            MissingIngredient.setObjectName(u"MissingIngredient")
        MissingIngredient.resize(420, 190)
        self.centralwidget = QWidget(MissingIngredient)
        self.centralwidget.setObjectName(u"centralwidget")
        self.MissIngLab = QLabel(self.centralwidget)
        self.MissIngLab.setObjectName(u"MissIngLab")
        self.MissIngLab.setGeometry(QRect(10, 10, 141, 31))
        font = QFont()
        font.setPointSize(16)
        self.MissIngLab.setFont(font)
        self.IngredLine = QLineEdit(self.centralwidget)
        self.IngredLine.setObjectName(u"IngredLine")
        self.IngredLine.setGeometry(QRect(150, 10, 261, 31))
        font1 = QFont()
        font1.setPointSize(15)
        self.IngredLine.setFont(font1)
        self.EditIngButton = QPushButton(self.centralwidget)
        self.EditIngButton.setObjectName(u"EditIngButton")
        self.EditIngButton.setGeometry(QRect(10, 60, 111, 32))
        self.CloseButton = QPushButton(self.centralwidget)
        self.CloseButton.setObjectName(u"CloseButton")
        self.CloseButton.setGeometry(QRect(160, 60, 141, 32))
        MissingIngredient.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MissingIngredient)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 420, 37))
        MissingIngredient.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MissingIngredient)
        self.statusbar.setObjectName(u"statusbar")
        MissingIngredient.setStatusBar(self.statusbar)

        self.retranslateUi(MissingIngredient)

        QMetaObject.connectSlotsByName(MissingIngredient)
    # setupUi

    def retranslateUi(self, MissingIngredient):
        MissingIngredient.setWindowTitle(QCoreApplication.translate("MissingIngredient", u"MainWindow", None))
        self.MissIngLab.setText(QCoreApplication.translate("MissingIngredient", u"Missing ingredient", None))
        self.EditIngButton.setText(QCoreApplication.translate("MissingIngredient", u"Edit Ingredients?", None))
        self.CloseButton.setText(QCoreApplication.translate("MissingIngredient", u"PushButton", None))
    # retranslateUi

