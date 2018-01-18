#coding:utf-8
from daily_data_ui import Ui_Form as daily_ui
from weloop_sport.swim_ui import Ui_Form as swim_ui
from daily_data_verity import Ui_data_verify
from PyQt4.Qt import *
from PyQt4 import QtCore,QtGui
import sys
from functions_daily import function as func_daily
from weloop_function_struct import mode_name
import utc_time
from weloop_sport_main import read_daily
reload(sys)
sys.setdefaultencoding('utf-8')

class daily_data0(QtGui.QWidget, daily_ui):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()
    daily_data=""
    def __init__(self):
        super(daily_data0, self).__init__()
        self.setupUi(self)  # 加载窗体
        palette = QtGui.QPalette()
        icon = QtGui.QPixmap("./img/sub_background.png")
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(icon))  # 添加背景图片
        self.setPalette(palette)

        self.func_daily=func_daily()
        self.utc_time=utc_time.utc_time()

    def Massage(self):
        QtGui.QMessageBox.warning(self, u"警告", u"每分钟步数超过255或能量值超过127,请重新设置", QMessageBox.Ok | QMessageBox.Cancel)

    #获取日常设置UI页数据
    def get_ui_data(self):
        data=""
        time_all=0
        #开始时间、时区
        start_time = str(self.start_time.text())
        time_zone = str(self.time_zone.text())
        #日常标签模式下拉框
        status_1 = str(self.status_1.currentText())
        status_2 = str(self.status_2.currentText())
        status_3 = str(self.status_3.currentText())
        status_4 = str(self.status_4.currentText())
        #日常标签时间设置
        status_time1 = str(self.status_time1.text())
        status_time2 = str(self.status_time2.text())
        status_time3 = str(self.status_time3.text())
        status_time4 = str(self.status_time4.text())
        #能量值设置
        energe_1 = int(self.energe_1.text())
        energe_2 = int(self.energe_2.text())
        energe_3 = int(self.energe_3.text())
        energe_4 = int(self.energe_4.text())
        #步数设置
        step_1 = int(self.step_1.text())
        step_2 = int(self.step_2.text())
        step_3 = int(self.step_3.text())
        step_4 = int(self.step_4.text())

        if energe_1>127 or energe_2>127 or energe_3>127 or energe_4>127 or \
            step_1 > 255 or step_2 > 255 or  step_3 > 255 or  step_4 > 255:
            self.Massage()

        #r_sec为十进制时间戳
        head, r_sec=self.func_daily.start_time(start_time,int(time_zone))
        data=data+head
        if status_1!="请选择":
            status_1_str=self.func_daily.tip_mode(mode_name[status_1],status_time1,energe_1,step_1)
            data = data +status_1_str
            time_all+=int(status_time1)
        if status_2!="请选择":
            status_2_str = self.func_daily.tip_mode(mode_name[status_2], status_time2, energe_2, step_2)
            data = data + status_2_str
            time_all += int(status_time2)
        if status_3!="请选择":
            status_3_str = self.func_daily.tip_mode(mode_name[status_3], status_time3, energe_3, step_3)
            data = data + status_3_str
            time_all += int(status_time3)
        if status_4!="请选择":
            status_4_str = self.func_daily.tip_mode(mode_name[status_4], status_time4, energe_4, step_4)
            data = data + status_4_str
            time_all += int(status_time4)
        #标签结束时间设置
        end_time =self.utc_time.seconds_to_utc(int(r_sec+time_all*60)).show(True)
        return data,end_time

    @pyqtSlot()
    def on_commit_clicked(self):  # 确认按钮
        daily_data0.data, end_time = self.get_ui_data()
        self.data_show.setText(daily_data0.data)
        self.end_time.setText(end_time)

    @pyqtSlot()
    def on_verity_clicked(self):  #验证按钮
        daily_data0.data, end_time = self.get_ui_data()
        self.data_show.setText(daily_data0.data)
        self.end_time.setText(end_time)
        
        #验证UI标签页显示
        self.ui = daily_data_verify()
        self.ui.show()
        self.verify_daily_data()
    
    #标签验证UI设置
    def verify_daily_data(self):
        try:
            result={}  #清空日常数据字典
            result =(read_daily(daily_data0.data,"1")) #解析日常数据
            self.ui.tableWidget.setRowCount(len(result) + 10) #设置tab行数
            j = 0
            for i in range(len(result)):
                key_list0 = result[i].keys()  #获取解析数据的key
                if result[i].has_key("heart"):
                    h_hrt = QTableWidgetItem(str(result[j]["heart"]))
                    l_energy = QTableWidgetItem(str(result[j]["energy"]))
                    h_step = QTableWidgetItem(str(result[j]["step"]))
                    mode = QTableWidgetItem(str(result[j]["mode"]).decode("UTF-8")) #处理中文显示问题
                    format_date = QTableWidgetItem(str(result[j]["start_time"]))

                    #写入tab页
                    self.ui.tableWidget.setItem(j, 0, h_hrt)
                    self.ui.tableWidget.setItem(j, 1, l_energy)
                    self.ui.tableWidget.setItem(j, 2, h_step)
                    self.ui.tableWidget.setItem(j, 3, mode)
                    self.ui.tableWidget.setItem(j, 4, format_date)
                    j += 1
                #处理概要数据标签及时间标签(合并)
                if len(key_list0) < 5 or not result[i].has_key("heart"):
                    ll = 0
                    result_data = ""
                    self.ui.tableWidget.setSpan(j, ll, 1, 5)  #合并标签
                    for k in range(len(key_list0)):
                        result_data = result_data + " | " + str(key_list0[k]) + "：" + str(
                            result[j][key_list0[k]]).decode("UTF-8")
                    str1 = QTableWidgetItem(result_data)
                    str1.setBackgroundColor(QColor(0, 191, 255))
                    self.ui.tableWidget.setItem(j, 0, str1)
                    j += 1

        except Exception as e:
            print e
   
#日常标签验证UI界面
class daily_data_verify(QtGui.QWidget, Ui_data_verify):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()

    def __init__(self):
        super(daily_data_verify, self).__init__()
        self.setupUi(self)



#游泳数据
class swim_data(QtGui.QWidget, swim_ui):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()

    def __init__(self):
        super(swim_data, self).__init__()
        self.setupUi(self)  # 加载窗体
        self.daily_func=func_daily()
    
    #获取游泳设置UI界面数据
    def get_ui_data(self):
        self.Start_time=str(self.start_time.text()) #开始时间
        self.Time_zone=int(self.time_zone.text())   #时区
        self.Sport_time_set=int(self.sport_time_set.text()) #游泳时常设置
        self.Pool_len=int(self.poor_len.text())             #泳池长度
        self.Lap_count=int(self.lap_count.text())           #游泳圈数设置
        self.Stroke_count=int(self.stroke_count.text())     #划水次数设置(默认每趟一致)
        self.Swim_type=int(self.swim_style.text())          #泳姿设置
        self.Pace=int(self.pace.text())*60  #配速单位:s
        self.Kcal=int(self.kcal.text())*1000 #卡路里单位:cal
        self.energy=15  #能量值默认设置15
        self.step=0     #游泳期间不计步

    @pyqtSlot()
    def on_commit_clicked(self): #确定按钮
        self.get_data()
        self.swim_data_show.setText(self.swim_data)

    @pyqtSlot()
    def on_verify_clicked(self): #验证按钮
        
        #获取UI设置数据
        self.get_data()
        self.swim_ui = daily_data_verify()
        self.swim_ui.show()
        self.verify_daily_data()
    
    def get_data(self):
        self.get_ui_data()
        #second为十进制时间戳
        head, second = self.daily_func.start_time(self.Start_time, self.Time_zone)
        data_str = self.daily_func.swim_tip_data(second, self.Sport_time_set, self.Lap_count, self.Pace,self.Stroke_count, self.Kcal, self.Swim_type, self.Pool_len,self.energy, self.step)
        self.swim_data=head+data_str  #游泳数据
        
    #标签验证UI
    def verify_daily_data(self):
        try:

            result =read_daily(self.swim_data,"1")
            self.swim_ui.tableWidget.setRowCount(len(result) + 10)
            j = 0
            for i in range(len(result)):
                key_list0 = result[i].keys()
                if result[i].has_key("heart"):
                    h_hrt = QTableWidgetItem(str(result[j]["heart"]))
                    l_energy = QTableWidgetItem(str(result[j]["energy"]))
                    h_step = QTableWidgetItem(str(result[j]["step"]))
                    mode = QTableWidgetItem(str(result[j]["mode"]).decode("UTF-8"))
                    format_date = QTableWidgetItem(str(result[j]["start_time"]))

                    self.swim_ui.tableWidget.setItem(j, 0, h_hrt)
                    self.swim_ui.tableWidget.setItem(j, 1, l_energy)
                    self.swim_ui.tableWidget.setItem(j, 2, h_step)
                    self.swim_ui.tableWidget.setItem(j, 3, mode)
                    self.swim_ui.tableWidget.setItem(j, 4, format_date)
                    j += 1
                    
                if len(key_list0) < 5 or not result[i].has_key("heart"):
                    ll = 0
                    result_data = ""
                    self.swim_ui.tableWidget.setSpan(j, ll, 1, 5)
                    for k in range(len(key_list0)):
                        result_data = result_data + " | " + str(key_list0[k]) + "：" + str(
                            result[j][key_list0[k]]).decode("UTF-8")
                    str1 = QTableWidgetItem(result_data)
                    str1.setBackgroundColor(QColor(0, 191, 255))
                    self.swim_ui.tableWidget.setItem(j, 0, str1)
                    j += 1

        except Exception as e:
            print e
  
  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = daily_data0()
    ui.setWindowTitle(u"原始数据仿真工具")
    ui.show()
    app.installEventFilter(ui)
    sys.exit(app.exec_())