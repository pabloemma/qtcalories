# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CalculatePortion.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.labRecipe = QLabel(Dialog)
        self.labRecipe.setObjectName(u"labRecipe")
        self.labRecipe.setGeometry(QRect(10, 20, 81, 31))
        font = QFont()
        font.setPointSize(17)
        self.labRecipe.setFont(font)
        self.lineRecipe = QLineEdit(Dialog)
        self.lineRecipe.setObjectName(u"lineRecipe")
        self.lineRecipe.setGeometry(QRect(100, 20, 281, 31))
        font1 = QFont()
        font1.setPointSize(18)
        self.lineRecipe.setFont(font1)
        self.labPortion = QLabel(Dialog)
        self.labPortion.setObjectName(u"labPortion")
        self.labPortion.setGeometry(QRect(10, 90, 211, 31))
        self.labPortion.setFont(font1)
        self.lineWeight = QLineEdit(Dialog)
        self.lineWeight.setObjectName(u"lineWeight")
        self.lineWeight.setGeometry(QRect(250, 90, 113, 31))
        self.lineWeight.setFont(font1)
        self.labResult = QLabel(Dialog)
        self.labResult.setObjectName(u"labResult")
        self.labResult.setGeometry(QRect(10, 160, 121, 41))
        font2 = QFont()
        font2.setPointSize(20)
        self.labResult.setFont(font2)
        self.linResult = QLineEdit(Dialog)
        self.linResult.setObjectName(u"linResult")
        self.linResult.setGeometry(QRect(170, 160, 161, 41))
        self.linResult.setFont(font2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.labRecipe.setText(QCoreApplication.translate("Dialog", u"Recipe", None))
        self.labPortion.setText(QCoreApplication.translate("Dialog", u"Portion Weight", None))
        self.labResult.setText(QCoreApplication.translate("Dialog", u"Your calories", None))
    # retranslateUi

