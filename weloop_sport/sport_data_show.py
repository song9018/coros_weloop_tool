# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sport_data_show.ui'
#
# Created: Mon Dec 25 14:51:03 2017
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Sport_Data_Show(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(545, 332)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "原始数据展示", None, QtGui.QApplication.UnicodeUTF8))
        #weloop logo设计
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("img/weloop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)

        self.sport_data = QtGui.QTextEdit(Form)
        self.sport_data.setGeometry(QtCore.QRect(0, 30, 541, 121))
        self.sport_data.setObjectName(_fromUtf8("sport_data"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(220, 10, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setText(QtGui.QApplication.translate("Form", "运动数据", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.daily_data = QtGui.QTextEdit(Form)
        self.daily_data.setGeometry(QtCore.QRect(0, 200, 541, 131))
        self.daily_data.setObjectName(_fromUtf8("daily_data"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(220, 170, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setText(QtGui.QApplication.translate("Form", "标签数据", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

