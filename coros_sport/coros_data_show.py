# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coros_data_show.ui'
#
# Created: Wed Jan 10 20:22:41 2018
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(851, 624)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "数据展示", None, QtGui.QApplication.UnicodeUTF8))
        # coros logo设计
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("img/coros_Logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)

        self.sport_data = QtGui.QTextEdit(Form)
        self.sport_data.setGeometry(QtCore.QRect(0, 50, 851, 191))
        self.sport_data.setObjectName(_fromUtf8("sport_data"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(380, 10, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setText(QtGui.QApplication.translate("Form", "运动数据", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.graphicsView = QtGui.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(0, 241, 851, 381))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

