# coding=utf-8
from weloop_daily.daily_main import daily_data0,swim_data
from weloop_sport.sport_main import sport_data
from coros_sport.coros_sport_main import *
from window_ui import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import sys
from PyQt4.Qt import *

reload(sys)
sys.setdefaultencoding('utf-8')


class main_UI(QtGui.QWidget, Ui_MainWindow):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()
    def __init__(self):
        super(main_UI, self).__init__()
        self.setupUi(self)
        palette = QtGui.QPalette()
        icon = QtGui.QPixmap("./img/background.png")
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(icon))  # 添加背景图片
        self.setPalette(palette)

    @pyqtSlot()
    def on_weloop_daily_data_clicked(self):
        self.weloop_daily0 = daily_data0()
        self.weloop_daily0.setWindowTitle(u"weloop日常数据")
        self.weloop_daily0.show()

    @pyqtSlot()
    def on_weloop_outdoor_clicked(self):
        self.weloop_outdoor0 = sport_data(0)
        self.weloop_outdoor0.setWindowTitle(u"weloop跑步数据")
        self.weloop_outdoor0.show()

    @pyqtSlot()
    def on_weloop_cycle_clicked(self):
        self.weloop_cycle0 = sport_data(1)
        self.weloop_cycle0.cadence.setChecked(False)
        self.weloop_cycle0.setWindowTitle(u"weloop骑行数据")
        self.weloop_cycle0.show()

    @pyqtSlot()
    def on_weloop_swim_clicked(self):
        self.weloop_swim=swim_data()
        self.weloop_swim.setWindowTitle(u"weloop游泳数据")
        self.weloop_swim.show()

    @pyqtSlot()
    def on_coros_Triathlon_clicked(self):
        self.coros_open_swim = coros_open_water_data(0)
        self.coros_open_swim.setWindowTitle(u"coros铁人三项--公开水域")
        self.coros_open_swim.commit.hide()
        self.coros_open_swim.open_water_next.show()
        self.coros_open_swim.show()


    @pyqtSlot()
    def on_coros_outdoor_clicked(self):
        self.coros_outdoor = coros_run_data(0)
        self.coros_outdoor.setWindowTitle(u"coros跑步数据")
        self.coros_outdoor.show()

    @pyqtSlot()
    def on_coros_cycle_clicked(self):
        self.coros_cycle = coros_cycle_data(0)
        self.coros_cycle.setWindowTitle(u"coros骑行数据")
        self.coros_cycle.show()

    @pyqtSlot()
    def on_coros_swim_clicked(self):
        self.coros_swim = coros_pool_swim_data(0)
        self.coros_swim.setWindowTitle(u"coros游泳数据")
        self.coros_swim.show()

    @pyqtSlot()
    def on_coros_open_swim_clicked(self):
        self.coros_open_swim = coros_open_water_data(0)
        self.coros_open_swim.setWindowTitle(u"coros公开水域")
        self.coros_open_swim.show()

#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main_UI()
    ui.setWindowTitle(u"设备数据仿真工具")
    ui.show()
    app.installEventFilter(ui)
    sys.exit(app.exec_())
