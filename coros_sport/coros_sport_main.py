# coding:utf-8
import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.Qt import *
from coros_run_set import Ui_Form as run_ui_form
from coros_cycle_set import Ui_Form as cycle_ui_form
from coros_pool_swim_set import Ui_Form as pool_swim_ui_form
from coros_open_water_set import Ui_Form as open_water_ui_form
from coros_data_show import Ui_Form as data_show_ui_form
from coros_functions import coros_function
from sport_common import *
reload(sys)
sys.setdefaultencoding('utf-8')

map_path="./build/handle.html"
map_path_none="./build/handle_none.html"
open_water_data=""
cycle_data=""
run_data=""
all_str=""

# GPS偏移处理
def add_gps(list1):
        for i in range(len(list1)):
            list1[i][0] = list1[i][0] + 0.004843
            list1[i][1] = list1[i][1] - 0.002995
        return list1

#经纬度数据写入html文件
class Lat_Lon(object):
    #list格式：[[[113.12122,23.12131,0],[113.12122,23.12131,0]]]
    def write_lat_lon(self, file_name, list=None, list1=None, list2=None, list3=None): 
        if len(list) == 1:
            list1 = list[0]
        elif len(list) == 2:
            list1 = list[0]
            list2 = list[1]
        elif len(list) == 3:
            list1 = list[0]
            list2 = list[1]
            list3 = list[2]

        file = open(file_name, 'r')
        lines = file.readlines()
        len_t = len(lines) - 1

        for i in range(len_t):
            # 地图中心点设置
            if "center" in lines[i]:
                data = lines[i].split(':')[1]
                lines[i] = lines[i].replace(data, str(list1[0]) + ",\n")
            if 'var lineArr' in lines[i]:
                data = lines[i].split('=')[1]
                lines[i] = lines[i].replace(data, str(list1) + "\n")
            if 'var lineArr1' in lines[i]:
                data = lines[i].split('=')[1]
                lines[i] = lines[i].replace(data, str(list2) + "\n")
            if 'var lineArr2' in lines[i]:
                data = lines[i].split('=')[1]
                lines[i] = lines[i].replace(data, str(list3) + "\n")
        file = open(file_name, 'w')
        file.writelines(lines)
        file.close()

#pyqt加载浏览器
class BrowserScreen(QtWebKit.QWebView):
    def __init__(self, file_name):
        QtWebKit.QWebView.__init__(self)
        self.resize(851, 381)
        self.setUrl(QUrl(file_name))

        
class coros_run_data(QtGui.QWidget, run_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()
    lon_lat_list=[]
    run_data=""
    def __init__(self,second_utc):
        super(coros_run_data, self).__init__()
        self.setupUi(self)  # 加载窗体
        self.finish.hide()
        self.gps_data = Lat_Lon()
        self.coros_func=coros_function()
        self.second_utc=second_utc
        self.data_dic={}

    #加载地图
    def run_map(self, file_name):
        sc = BrowserScreen(file_name)
        graphicscene = QGraphicsScene()
        graphicscene.addWidget(sc)
        self.run_ui.graphicsView.setScene(graphicscene)
        self.run_ui.graphicsView.show()

    def get_ui_data(self):
        #运动时间获取
        self.data_dic["Start_time"] = str(self.start_time.text())
        self.data_dic["Time_zone"] = int(str(self.time_zone.text()))
        self.data_dic["Sport_time_set"]=int(str(self.sport_time_set.text()))
        #总距离、单圈距离获取
        self.data_dic["distance0"]=int(self.distance.text())
        self.data_dic["around0"]=int(self.around.text())
        self.data_dic["kcal0"]=int(self.kcal.text())
        self.data_dic["avg_heart0"]=int(self.heart.text())
        self.data_dic["elevation0"]=int(self.elevation.text())
        self.data_dic["decline0"] = int(self.decline.text())
        self.data_dic["most_step0"] = int(self.most_step.text())
        self.data_dic["most_heart0"] = int(self.most_heart.text())
        self.data_dic["most_speed0"] = int(self.most_pace.text())
        self.data_dic["avg_speed0"] = int(self.avg_pace.text())
        #轨迹地区获取
        self.data_dic["locus_box_status"]=str(self.locus_box.currentText())

    @pyqtSlot()
    def on_commit_clicked(self):#确认按钮
        self.get_ui_data()
        self.__data,second_1,list_gps=get_data(0,self.coros_func,self.data_dic,self.second_utc,sport_type=0)
        #数据展示
        self.run_ui = data_show()
        self.run_ui.show()
        self.run_ui.sport_data.setText(self.__data)
        self.run_map(map_path)  # 加载轨迹地图

    @pyqtSlot()
    def on_finish_clicked(self):  # 确认按钮
        self.get_ui_data()
        self.ori_data_all, self.second_utc, self.list_gps= get_data(3,self.coros_func,self.data_dic,self.second_utc,sport_type=0)
        print self.ori_data_all
        run_data=coros_open_water_data.open_water_data+coros_cycle_data.cycle_data+self.ori_data_all

        # 数据展示
        self.run_ui = data_show()
        self.run_ui.show()
        self.run_ui.sport_data.setText(run_data)

        self.run_map(map_path)  # 加载轨迹地图
        self.close()

class coros_cycle_data(QtGui.QWidget, cycle_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()
    gps_str = ""
    cycle_data=""
    lon_lat_list = []

    def __init__(self,second_utc):
        super(coros_cycle_data, self).__init__()
        self.setupUi(self)  # 加载窗体
        self.cycle_next.hide()
        self.data_dic={}

        self.coros_func = coros_function()
        self.second_utc=second_utc
        self.gps_data = Lat_Lon()

    # 加载地图
    def run_map(self, file_name):
        sc = BrowserScreen(file_name)
        graphicscene = QGraphicsScene()
        graphicscene.addWidget(sc)
        self.cycle_ui.graphicsView.setScene(graphicscene)
        self.cycle_ui.graphicsView.show()

    def get_ui_data(self):
        # 运动时间获取
        self.data_dic["Start_time"] = str(self.start_time.text())
        self.data_dic["Time_zone"] = int(str(self.time_zone.text()))
        self.data_dic["Sport_time_set"] = int(str(self.sport_time_set.text()))
        # 总距离、单圈距离获取
        self.data_dic["distance0"] = int(self.distance.text())
        self.data_dic["around0"] = int(self.around.text())
        self.data_dic["kcal0"] = int(self.kcal.text())
        self.data_dic["avg_heart0"] = int(self.heart.text())
        self.data_dic["elevation0"] = int(self.elevation.text())
        self.data_dic["decline0"] = int(self.decline.text())
        self.data_dic["most_step0"] = int(self.most_step.text())
        self.data_dic["most_heart0"] = int(self.most_heart.text())
        self.data_dic["most_speed0"] = int(self.most_speed.text())
        self.data_dic["avg_speed0"] = int(self.avg_speed.text())
        # 轨迹地区获取
        self.data_dic["locus_box_status"] = str(self.locus_box.currentText())

    @pyqtSlot()
    def on_commit_clicked(self):  # 确认按钮
        # 获取运动界面相关数据
        self.get_ui_data()
        self.__data,second_1,list_gps = get_data(0,self.coros_func,self.data_dic,self.second_utc,sport_type=4)
        # 数据展示
        self.cycle_ui = data_show()
        self.cycle_ui.show()
        self.cycle_ui.sport_data.setText(self.__data)

        self.run_map(map_path)  # 加载轨迹地图

    @pyqtSlot()
    def on_cycle_next_clicked(self):  #
        self.get_ui_data()
        self.ori_data_all, self.second_1, self.list_gps= get_data(2,self.coros_func,self.data_dic,self.second_utc,sport_type=4)
        coros_cycle_data.cycle_data =self.ori_data_all
        print self.ori_data_all
        self.coros_run1 = coros_run_data(self.second_1+5)
        self.coros_run1.setWindowTitle(u"coros铁人三项--跑步数据")
        self.coros_run1.show()
        self.coros_run1.commit.hide()
        self.coros_run1.finish.show()
        self.close()


class coros_pool_swim_data(QtGui.QWidget, pool_swim_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()

    def __init__(self,second_utc):
        super(coros_pool_swim_data, self).__init__()
        self.setupUi(self)  # 加载窗体
        self.str=""
        self.coros_func = coros_function()
        self.data_dic={}
        self.second_utc=second_utc

    def get_ui_data(self):
        self.data_dic["Start_time"] = str(self.start_time.text())  # 开始时间
        self.data_dic["Time_zone"] = int(self.time_zone.text())  # 时区
        self.data_dic["Sport_time_set"] = int(self.sport_time_set.text())  # 游泳时常设置

        self.data_dic["around0"] = int(self.dis_len.text())  # 泳池长度
        self.data_dic["Lap_count"] = int(self.lap_count.text())  # 游泳圈数设置
        self.data_dic["distance0"] = self.data_dic["around0"] * self.data_dic["Lap_count"]
        self.data_dic["Stroke_count"] = int(self.stroke_count.text())  # 划水次数设置(默认每趟一致)
        self.data_dic["Swim_type"] = int(self.swim_style.text())  # 泳姿设置

        self.data_dic["Kcal"] = int(self.kcal.text()) * 1000  # 卡路里单位:cal
        self.data_dic["Most_pace"] = int(self.most_pace.text()) * 60
        self.data_dic["Avg_pace"] = int(self.avg_pace.text()) * 60  # 配速单位:s
        self.data_dic["Most_str_rate"] = int(self.most_str_rate.text())
        self.data_dic["Avg_str_rate"] = int(self.avg_str_rate.text())
        self.data_dic["Most_swolf"] = int(self.most_str_rate.text())
        self.data_dic["Avg_swolf"] = int(self.avg_swolf.text())

    @pyqtSlot()
    def on_commit_clicked(self):  # 确认按钮
        # 获取运动界面相关数据
        self.get_ui_data()
        self.__data, second_utc, ori_list =get_data(0,self.coros_func,self.data_dic,self.second_utc,sport_type=3)
        # 数据展示
        self.data_set.setText(self.__data)


class coros_open_water_data(QtGui.QWidget, open_water_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()
    gps_str = ""
    open_water_data = ""
    lon_lat_list = []

    def __init__(self,second_utc):
        super(coros_open_water_data, self).__init__()
        self.setupUi(self)  # 加载窗体
        self.open_water_next.hide()
        self.coros_func = coros_function()
        self.data_dic={}
        self.second_utc=second_utc

    # 加载地图
    def run_map(self, file_name):
        sc = BrowserScreen(file_name)
        graphicscene = QGraphicsScene()
        graphicscene.addWidget(sc)
        self.open_water_ui.graphicsView.setScene(graphicscene)
        self.open_water_ui.graphicsView.show()

    def get_ui_data(self):
        self.data_dic["Start_time"] = str(self.start_time.text())  # 开始时间
        self.data_dic["Time_zone"] = int(self.time_zone.text())  # 时区
        self.data_dic["Sport_time_set"] = int(self.sport_time_set.text())  # 游泳时常设置

        self.data_dic["around0"] = int(self.dis_len.text())  # 泳池长度
        self.data_dic["Lap_count"] = int(self.lap_count.text())  # 游泳圈数设置
        self.data_dic["distance0"]=self.data_dic["around0"]*self.data_dic["Lap_count"]
        self.data_dic["Stroke_count"] = int(self.stroke_count.text())  # 划水次数设置(默认每趟一致)
        self.data_dic["Swim_type"] = int(self.swim_style.text())  # 泳姿设置

        self.data_dic["Kcal"] = int(self.kcal.text()) * 1000  # 卡路里单位:cal
        self.data_dic["Most_pace"] = int(self.most_pace.text()) * 60
        self.data_dic["Avg_pace"] = int(self.avg_pace.text()) * 60  # 配速单位:s
        self.data_dic["Most_str_rate"] = int(self.most_str_rate.text())
        self.data_dic["Avg_str_rate"] = int(self.avg_str_rate.text())
        self.data_dic["Most_swolf"] = int(self.most_str_rate.text())
        self.data_dic["Avg_swolf"] = int(self.avg_swolf.text())

    @pyqtSlot()
    def on_commit_clicked(self):  # 确认按钮
        # 获取运动界面相关数据
        self.get_ui_data()
        self.__data, self.second_utc, list_gps =get_data(0,self.coros_func,self.data_dic,self.second_utc,sport_type=2)
        # 数据展示
        self.open_water_ui = data_show()
        self.open_water_ui.show()
        self.open_water_ui.sport_data.setText(self.__data)
        self.run_map(map_path)  # 加载轨迹地图

    @pyqtSlot()
    def on_open_water_next_clicked(self):  # 铁三下一项操作按钮
        self.get_ui_data()
        self.ori_data_all, self.second_utc, self.list_gps=get_data(1,self.coros_func,self.data_dic,self.second_utc,sport_type=2)
        coros_open_water_data.open_water_data=self.ori_data_all
        print self.ori_data_all
        self.coros_cycle1=coros_cycle_data(self.second_utc+5)
        self.coros_cycle1.setWindowTitle(u"coros铁人三项--骑行数据")
        self.coros_cycle1.show()
        self.coros_cycle1.commit.hide()
        self.coros_cycle1.cycle_next.show()
        self.close()

#运动数据、日常标签数据展示
class data_show(QtGui.QWidget, data_show_ui_form):
    _translate = QtCore.QCoreApplication.translate
    closeWidget = pyqtSignal()

    def __init__(self):
        super(data_show, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = coros_run_data(0)

    ui.setWindowTitle(u"运动数据")
    ui.show()
    app.installEventFilter(ui)
    sys.exit(app.exec_())
