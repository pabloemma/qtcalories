# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'database_connect.ui'
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
        self.db_name = QLineEdit(Dialog)
        self.db_name.setObjectName(u"db_name")
        self.db_name.setGeometry(QRect(150, 10, 113, 21))
        self.db_label = QLabel(Dialog)
        self.db_label.setObjectName(u"db_label")
        self.db_label.setGeometry(QRect(40, 10, 58, 16))
        self.User_label = QLabel(Dialog)
        self.User_label.setObjectName(u"User_label")
        self.User_label.setGeometry(QRect(40, 50, 61, 21))
        self.user_edit = QLineEdit(Dialog)
        self.user_edit.setObjectName(u"user_edit")
        self.user_edit.setGeometry(QRect(150, 50, 113, 21))
        self.system_label = QLabel(Dialog)
        self.system_label.setObjectName(u"system_label")
        self.system_label.setGeometry(QRect(40, 95, 58, 21))
        self.system_edit = QLineEdit(Dialog)
        self.system_edit.setObjectName(u"system_edit")
        self.system_edit.setGeometry(QRect(150, 90, 113, 21))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.db_label.setText(QCoreApplication.translate("Dialog", u"DB_name", None))
        self.User_label.setText(QCoreApplication.translate("Dialog", u"DB_user", None))
        self.system_label.setText(QCoreApplication.translate("Dialog", u"DB_system", None))
    # retranslateUi

