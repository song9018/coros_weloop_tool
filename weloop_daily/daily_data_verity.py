# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_input.ui'
#
# Created: Fri Apr 21 18:46:08 2017
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

"""
解决窗体编码问题
"""
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

"""
日志下载设备ID输入框设计
"""

class Ui_data_verify(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(815, 470)
        Form.setMinimumSize(QtCore.QSize(815, 470))
        Form.setMaximumSize(QtCore.QSize(815, 470))
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "日常数据解析", None, QtGui.QApplication.UnicodeUTF8))

        # weloop logo设计
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("img/weloop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)

        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 810, 470))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section{background:DarkSeaGreen;}")  # 设置表头背景色
        self.tableWidget.verticalHeader().setStyleSheet("QHeaderView::section{background:DarkSeaGreen;}")  # 设置列头背景色
        self.tableWidget.setStyleSheet("selection-background-color:Gray;")  # 选中背景色
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)  # 整行被选中
        self.tableWidget.setColumnWidth(0, 160)
        self.tableWidget.setColumnWidth(1, 160)
        self.tableWidget.setColumnWidth(2, 160)
        self.tableWidget.setColumnWidth(3, 160)
        self.tableWidget.setColumnWidth(4, 160)

        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("Form", "heart", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("Form", "energy", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("Form", "step", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("Form", "mode", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("Form", "start_time", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(4, item)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass
