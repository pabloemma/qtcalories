# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'missing_ingredient_dialog.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_missing_ingredient_dialog(object):
    def setupUi(self, missing_ingredient_dialog):
        if not missing_ingredient_dialog.objectName():
            missing_ingredient_dialog.setObjectName(u"missing_ingredient_dialog")
        missing_ingredient_dialog.resize(400, 300)
        self.buttonBox = QDialogButtonBox(missing_ingredient_dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 200, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.setCenterButtons(True)
        self.MissingLab = QLabel(missing_ingredient_dialog)
        self.MissingLab.setObjectName(u"MissingLab")
        self.MissingLab.setGeometry(QRect(10, 30, 131, 21))
        font = QFont()
        font.setPointSize(15)
        self.MissingLab.setFont(font)
        self.IngredLine = QLineEdit(missing_ingredient_dialog)
        self.IngredLine.setObjectName(u"IngredLine")
        self.IngredLine.setGeometry(QRect(160, 30, 231, 21))
        self.EditButton = QPushButton(missing_ingredient_dialog)
        self.EditButton.setObjectName(u"EditButton")
        self.EditButton.setGeometry(QRect(110, 140, 141, 32))
        font1 = QFont()
        font1.setPointSize(16)
        self.EditButton.setFont(font1)

        self.retranslateUi(missing_ingredient_dialog)
        self.buttonBox.rejected.connect(missing_ingredient_dialog.reject)

        QMetaObject.connectSlotsByName(missing_ingredient_dialog)
    # setupUi

    def retranslateUi(self, missing_ingredient_dialog):
        missing_ingredient_dialog.setWindowTitle(QCoreApplication.translate("missing_ingredient_dialog", u"Dialog", None))
        self.MissingLab.setText(QCoreApplication.translate("missing_ingredient_dialog", u"Missing Ingredient", None))
        self.EditButton.setText(QCoreApplication.translate("missing_ingredient_dialog", u"Edit Ingredients", None))
    # retranslateUi

