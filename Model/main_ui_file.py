# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui',
# licensing of 'main.ui' applies.
#
# Created: Tue Nov  5 19:57:57 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(314, 102)
        self.Read_contents = QtWidgets.QPlainTextEdit(Form)
        self.Read_contents.setGeometry(QtCore.QRect(10, 10, 291, 81))
        self.Read_contents.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.Read_contents.setPlainText("")
        self.Read_contents.setObjectName("Read_contents")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))

