# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'missing_ingredient_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

class Ui_MyMissingIngredientForm(object):
    def setupUi(self, MyMissingIngredientForm):
        if not MyMissingIngredientForm.objectName():
            MyMissingIngredientForm.setObjectName(u"MyMissingIngredientForm")
        MyMissingIngredientForm.resize(400, 300)
        self.MissingLab = QLabel(MyMissingIngredientForm)
        self.MissingLab.setObjectName(u"MissingLab")
        self.MissingLab.setGeometry(QRect(30, 10, 331, 31))

        self.retranslateUi(MyMissingIngredientForm)

        QMetaObject.connectSlotsByName(MyMissingIngredientForm)
    # setupUi

    def retranslateUi(self, MyMissingIngredientForm):
        MyMissingIngredientForm.setWindowTitle(QCoreApplication.translate("MyMissingIngredientForm", u"Form", None))
        self.MissingLab.setText(QCoreApplication.translate("MyMissingIngredientForm", u"Missing Ingredient", None))
    # retranslateUi

